use atomicwrites::{AllowOverwrite, AtomicFile};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};

const CONFIG_NAME: &str = "scoville-plan-viewer.xml";

#[derive(Debug, Clone, Default, Deserialize, Serialize, PartialEq, Eq)]
pub struct ProjectRegistry {
    #[serde(default = "format_version")]
    version: u8,
    #[serde(default)]
    pub selected: String,
    #[serde(default)]
    pub projects: Vec<SavedProject>,
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq)]
pub struct SavedProject {
    pub id: String,
    pub name: String,
    pub path: String,
}

#[derive(Deserialize, Serialize)]
#[serde(rename = "projects")]
struct XmlRegistry {
    #[serde(rename = "@version")]
    version: u8,
    #[serde(rename = "@selected", default)]
    selected: String,
    #[serde(rename = "project", default)]
    projects: Vec<XmlProject>,
}

#[derive(Deserialize, Serialize)]
struct XmlProject {
    #[serde(rename = "@id")]
    id: String,
    #[serde(rename = "@name")]
    name: String,
    #[serde(rename = "@path")]
    path: String,
}

impl From<XmlRegistry> for ProjectRegistry {
    fn from(value: XmlRegistry) -> Self {
        Self {
            version: value.version,
            selected: value.selected,
            projects: value
                .projects
                .into_iter()
                .map(|project| SavedProject {
                    id: project.id,
                    name: project.name,
                    path: project.path,
                })
                .collect(),
        }
    }
}

impl From<&ProjectRegistry> for XmlRegistry {
    fn from(value: &ProjectRegistry) -> Self {
        Self {
            version: value.version,
            selected: value.selected.clone(),
            projects: value
                .projects
                .iter()
                .map(|project| XmlProject {
                    id: project.id.clone(),
                    name: project.name.clone(),
                    path: project.path.clone(),
                })
                .collect(),
        }
    }
}

fn format_version() -> u8 {
    1
}

fn config_path() -> Result<PathBuf, String> {
    let executable = std::env::current_exe()
        .map_err(|error| format!("Cannot locate the application executable: {error}"))?;
    portable_directory(&executable)
        .map(|directory| directory.join(CONFIG_NAME))
        .ok_or_else(|| "Cannot locate the portable application directory.".to_owned())
}

fn portable_directory(executable: &Path) -> Option<PathBuf> {
    #[cfg(target_os = "macos")]
    {
        // Put the file beside App.app, not inside the signed application bundle.
        executable.ancestors().nth(4).map(Path::to_path_buf)
    }
    #[cfg(target_os = "linux")]
    {
        std::env::var_os("APPIMAGE")
            .map(PathBuf::from)
            .filter(|path| path.is_absolute())
            .and_then(|path| path.parent().map(Path::to_path_buf))
            .or_else(|| executable.parent().map(Path::to_path_buf))
    }
    #[cfg(not(any(target_os = "macos", target_os = "linux")))]
    {
        executable.parent().map(Path::to_path_buf)
    }
}

fn read_registry(path: &Path) -> Result<ProjectRegistry, String> {
    if !path.exists() {
        return Ok(ProjectRegistry {
            version: format_version(),
            ..ProjectRegistry::default()
        });
    }

    let source = fs::read_to_string(path)
        .map_err(|error| format!("Cannot read {}: {error}", path.display()))?;
    let registry: ProjectRegistry = quick_xml::de::from_str::<XmlRegistry>(&source)
        .map_err(|error| format!("Cannot parse {}: {error}", path.display()))?
        .into();
    validate_registry(&registry)?;
    Ok(registry)
}

fn write_registry(path: &Path, registry: &ProjectRegistry) -> Result<(), String> {
    validate_registry(registry)?;
    let xml = quick_xml::se::to_string(&XmlRegistry::from(registry))
        .map_err(|error| format!("Cannot serialize the project list: {error}"))?;
    let document = format!("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n{xml}\n");
    AtomicFile::new(path, AllowOverwrite)
        .write(|file| file.write_all(document.as_bytes()))
        .map_err(|error| format!("Cannot write {}: {error}", path.display()))
}

fn validate_registry(registry: &ProjectRegistry) -> Result<(), String> {
    if registry.version != format_version() {
        return Err(format!(
            "Unsupported project list version {}. Expected version 1.",
            registry.version
        ));
    }

    let mut ids = HashSet::new();
    for project in &registry.projects {
        if project.id.trim().is_empty()
            || project.name.trim().is_empty()
            || project.path.trim().is_empty()
        {
            return Err("Every saved project needs an id, name, and path.".to_owned());
        }
        if !ids.insert(project.id.as_str()) {
            return Err(format!("Duplicate saved project id: {}", project.id));
        }
    }

    if !registry.selected.is_empty()
        && registry.selected != "__overview__"
        && !ids.contains(registry.selected.as_str())
    {
        return Err("The selected project is not present in the project list.".to_owned());
    }
    Ok(())
}

#[tauri::command]
pub fn load_project_registry() -> Result<ProjectRegistry, String> {
    read_registry(&config_path()?)
}

#[tauri::command]
pub fn save_project_registry(mut registry: ProjectRegistry) -> Result<(), String> {
    registry.version = format_version();
    write_registry(&config_path()?, &registry)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trips_paths_with_xml_characters() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join(CONFIG_NAME);
        let expected = ProjectRegistry {
            version: 1,
            selected: "one".to_owned(),
            projects: vec![SavedProject {
                id: "one".to_owned(),
                name: "Plan & decisions".to_owned(),
                path: r#"C:\Work\A & B\"#.to_owned(),
            }],
        };

        write_registry(&path, &expected).unwrap();
        assert_eq!(read_registry(&path).unwrap(), expected);
    }

    #[test]
    fn starts_empty_when_the_portable_config_is_missing() {
        let directory = tempfile::tempdir().unwrap();
        let registry = read_registry(&directory.path().join(CONFIG_NAME)).unwrap();
        assert_eq!(registry.version, 1);
        assert!(registry.projects.is_empty());
    }

    #[test]
    fn preserves_plain_json_fields_across_the_xml_boundary() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join(CONFIG_NAME);
        let input = serde_json::json!({
            "version": 1,
            "selected": "one",
            "projects": [{
                "id": "one",
                "name": "Portable plan",
                "path": "Z:\\Plans\\one"
            }]
        });
        let registry: ProjectRegistry = serde_json::from_value(input.clone()).unwrap();

        write_registry(&path, &registry).unwrap();
        let output = serde_json::to_value(read_registry(&path).unwrap()).unwrap();

        assert_eq!(output, input);
        assert!(output.get("@version").is_none());
    }
}
