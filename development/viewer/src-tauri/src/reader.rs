use serde::Serialize;
use std::collections::{BTreeMap, HashMap};
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

const MAX_RECORD_BYTES: u64 = 2 * 1024 * 1024;
const PLAN_STATUSES: &[&str] = &["draft", "active", "completed", "cancelled"];
const WORK_STATUSES: &[&str] = &["todo", "in_progress", "paused", "done", "cancelled"];
const DECISION_STATUSES: &[&str] = &[
    "proposed",
    "accepted",
    "rejected",
    "deprecated",
    "superseded",
];

#[derive(Debug, Serialize)]
pub struct ProjectSnapshot {
    root: String,
    name: String,
    active_plan: Option<String>,
    plans: Vec<Plan>,
    decisions: Vec<Decision>,
    loaded_at: u64,
}

#[derive(Debug, Serialize)]
pub struct Plan {
    id: String,
    title: String,
    status: String,
    created: String,
    updated: String,
    current_item: Option<String>,
    goal: String,
    non_goals: String,
    work_items: Vec<WorkItem>,
    source_path: String,
}

#[derive(Debug, Serialize)]
pub struct WorkItem {
    id: String,
    title: String,
    status: String,
    depends_on: Vec<String>,
    blocked_by: Vec<String>,
    decisions: Vec<String>,
    outcome: String,
    acceptance: String,
    steps: Vec<String>,
    evidence: Vec<String>,
    next_action: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct Decision {
    id: String,
    title: String,
    status: String,
    created: String,
    accepted: Option<String>,
    scope: String,
    supersedes: Option<String>,
    superseded_by: Option<String>,
    decision: String,
    problem: String,
    consequences: String,
    revisit_when: String,
    source_path: String,
}

#[tauri::command]
pub fn scan_project(root: String) -> Result<ProjectSnapshot, String> {
    read_project(Path::new(&root))
}

fn read_project(root: &Path) -> Result<ProjectSnapshot, String> {
    let canonical_root = root.canonicalize().map_err(|_| {
        "The selected project folder does not exist or cannot be accessed.".to_string()
    })?;
    if !canonical_root.is_dir() {
        return Err("Choose a project folder, not a file.".to_string());
    }

    let index_path = contained_path(
        &canonical_root,
        &canonical_root.join("PROJECT_INDEX.md"),
        true,
    )?;
    let plans_dir = contained_path(&canonical_root, &canonical_root.join("docs/plans"), false)?;
    let decisions_dir = contained_path(
        &canonical_root,
        &canonical_root.join("docs/decisions"),
        false,
    )?;

    let index_text = read_record(&index_path)?;
    let (index, _) = parse_frontmatter(&index_text, "PROJECT_INDEX.md")?;
    require_format_version(&index, "PROJECT_INDEX.md")?;
    let active_plan = optional_value(&index, "active_plan");

    let mut plans = read_markdown_files(&canonical_root, &plans_dir)?
        .into_iter()
        .map(|(path, relative, text)| parse_plan(&path, relative, &text))
        .collect::<Result<Vec<_>, _>>()?;
    plans.sort_by(|left, right| left.id.cmp(&right.id));

    let mut decisions = read_markdown_files(&canonical_root, &decisions_dir)?
        .into_iter()
        .map(|(path, relative, text)| parse_decision(&path, relative, &text))
        .collect::<Result<Vec<_>, _>>()?;
    decisions.sort_by(|left, right| left.id.cmp(&right.id));

    reject_duplicate_ids(plans.iter().map(|plan| plan.id.as_str()), "Plan")?;
    reject_duplicate_ids(
        decisions.iter().map(|decision| decision.id.as_str()),
        "Decision",
    )?;
    let decision_ids = decisions
        .iter()
        .map(|decision| decision.id.as_str())
        .collect::<Vec<_>>();
    for plan in &plans {
        for item in &plan.work_items {
            for decision in &item.decisions {
                if !decision_ids.contains(&decision.as_str()) {
                    return Err(format!(
                        "{} {} references missing Decision {}.",
                        plan.id, item.id, decision
                    ));
                }
            }
        }
    }
    for decision in &decisions {
        for related in [
            decision.supersedes.as_ref(),
            decision.superseded_by.as_ref(),
        ]
        .into_iter()
        .flatten()
        {
            if !decision_ids.contains(&related.as_str()) {
                return Err(format!(
                    "{} references missing Decision {}.",
                    decision.id, related
                ));
            }
        }
    }

    if let Some(active_id) = &active_plan {
        let plan = plans
            .iter()
            .find(|plan| &plan.id == active_id)
            .ok_or_else(|| format!("PROJECT_INDEX.md references missing Plan {active_id}."))?;
        if plan.status != "active" {
            return Err(format!(
                "PROJECT_INDEX.md references {active_id}, but that Plan is not active."
            ));
        }
    }

    let active_count = plans.iter().filter(|plan| plan.status == "active").count();
    if (active_plan.is_some() && active_count != 1) || (active_plan.is_none() && active_count != 0)
    {
        return Err("The active Plan state does not agree with PROJECT_INDEX.md.".to_string());
    }

    let name = canonical_root
        .file_name()
        .and_then(|value| value.to_str())
        .unwrap_or("Scoville Plan project")
        .to_string();

    Ok(ProjectSnapshot {
        root: canonical_root.to_string_lossy().into_owned(),
        name,
        active_plan,
        plans,
        decisions,
        loaded_at: SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64,
    })
}

fn contained_path(root: &Path, candidate: &Path, expect_file: bool) -> Result<PathBuf, String> {
    let canonical = candidate
        .canonicalize()
        .map_err(|_| format!("Required path is missing: {}", candidate.display()))?;
    if !canonical.starts_with(root) {
        return Err(format!(
            "Required path leaves the selected project: {}",
            candidate.display()
        ));
    }
    if expect_file && !canonical.is_file() {
        return Err(format!("Required file is invalid: {}", candidate.display()));
    }
    if !expect_file && !canonical.is_dir() {
        return Err(format!(
            "Required folder is invalid: {}",
            candidate.display()
        ));
    }
    Ok(canonical)
}

fn read_markdown_files(
    root: &Path,
    directory: &Path,
) -> Result<Vec<(PathBuf, String, String)>, String> {
    let mut records = Vec::new();
    for entry in fs::read_dir(directory)
        .map_err(|error| format!("Cannot read {}: {error}", directory.display()))?
    {
        let entry = entry.map_err(|error| format!("Cannot read a project record: {error}"))?;
        let path = entry.path();
        if path.extension().and_then(|value| value.to_str()) != Some("md") {
            continue;
        }
        let canonical = contained_path(root, &path, true)?;
        let relative = canonical
            .strip_prefix(root)
            .map_err(|_| "A project record is outside the selected root.".to_string())?
            .to_string_lossy()
            .replace('\\', "/");
        records.push((canonical.clone(), relative, read_record(&canonical)?));
    }
    records.sort_by(|left, right| left.1.cmp(&right.1));
    Ok(records)
}

fn read_record(path: &Path) -> Result<String, String> {
    let metadata = fs::metadata(path)
        .map_err(|error| format!("Cannot inspect {}: {error}", path.display()))?;
    if metadata.len() > MAX_RECORD_BYTES {
        return Err(format!(
            "Record exceeds the 2 MiB read limit: {}",
            path.display()
        ));
    }
    fs::read_to_string(path)
        .map_err(|error| format!("Cannot read {} as UTF-8: {error}", path.display()))
}

fn parse_frontmatter<'a>(
    text: &'a str,
    source: &str,
) -> Result<(HashMap<String, String>, &'a str), String> {
    let normalized = text.strip_prefix('\u{feff}').unwrap_or(text);
    let mut lines = normalized.split_inclusive('\n');
    let first = lines.next().unwrap_or_default();
    if first.trim_end_matches(['\r', '\n']) != "---" {
        return Err(format!("{source} has no valid frontmatter."));
    }
    let mut values = HashMap::new();
    let mut offset = first.len();
    let mut found_end = false;
    for line in lines {
        let clean = line.trim_end_matches(['\r', '\n']);
        offset += line.len();
        if clean == "---" {
            found_end = true;
            break;
        }
        let (key, value) = clean
            .split_once(':')
            .ok_or_else(|| format!("{source} contains an invalid frontmatter line."))?;
        let key = key.trim().to_string();
        if values
            .insert(key.clone(), value.trim().to_string())
            .is_some()
        {
            return Err(format!("{source} repeats frontmatter key {key}."));
        }
    }
    if !found_end {
        return Err(format!("{source} has unterminated frontmatter."));
    }
    Ok((values, &normalized[offset..]))
}

fn require_format_version(values: &HashMap<String, String>, source: &str) -> Result<(), String> {
    match values.get("format_version").map(String::as_str) {
        Some("1") => Ok(()),
        Some(value) => Err(format!("{source} uses unsupported format_version {value}.")),
        None => Err(format!("{source} does not declare format_version.")),
    }
}

fn required_value(
    values: &HashMap<String, String>,
    key: &str,
    source: &str,
) -> Result<String, String> {
    values
        .get(key)
        .filter(|value| !value.is_empty())
        .cloned()
        .ok_or_else(|| format!("{source} is missing {key}."))
}

fn optional_value(values: &HashMap<String, String>, key: &str) -> Option<String> {
    values
        .get(key)
        .filter(|value| !value.is_empty() && value.as_str() != "null")
        .cloned()
}

fn parse_plan(_path: &Path, source_path: String, text: &str) -> Result<Plan, String> {
    let (frontmatter, body) = parse_frontmatter(text, &source_path)?;
    require_format_version(&frontmatter, &source_path)?;
    let sections = split_h2_sections(body);
    let title = parse_title(body, &source_path)?;
    let goal = section_text(&sections, "Goal", &source_path)?;
    let non_goals = section_text(&sections, "Non-goals", &source_path)?;
    let work_source = sections
        .get("Work items")
        .ok_or_else(|| format!("{source_path} is missing Work items."))?;
    let work_items = parse_work_items(work_source, &source_path)?;
    let current_item = optional_value(&frontmatter, "current_item");
    if let Some(current) = &current_item {
        if !work_items.iter().any(|item| &item.id == current) {
            return Err(format!(
                "{source_path} references missing current item {current}."
            ));
        }
    }
    let status = required_value(&frontmatter, "status", &source_path)?;
    if !PLAN_STATUSES.contains(&status.as_str()) {
        return Err(format!(
            "{source_path} uses unsupported Plan status {status}."
        ));
    }
    if status == "active" && current_item.is_none() {
        return Err(format!("{source_path} is active but has no current_item."));
    }
    reject_duplicate_ids(work_items.iter().map(|item| item.id.as_str()), "Work Item")?;
    if status != "active" && current_item.is_some() {
        return Err(format!(
            "{source_path} is not active but retains current_item."
        ));
    }
    if let Some(current) = &current_item {
        let item = work_items
            .iter()
            .find(|item| &item.id == current)
            .expect("current_item existence was checked");
        if ["done", "cancelled"].contains(&item.status.as_str()) {
            return Err(format!(
                "{source_path} selects terminal Work Item {current} as current."
            ));
        }
    }
    let in_progress = work_items
        .iter()
        .filter(|item| item.status == "in_progress")
        .collect::<Vec<_>>();
    if in_progress.len() > 1
        || in_progress
            .first()
            .is_some_and(|item| Some(&item.id) != current_item.as_ref())
    {
        return Err(format!(
            "{source_path} has an in-progress Work Item that is not its sole current item."
        ));
    }
    if status == "completed"
        && work_items
            .iter()
            .any(|item| !["done", "cancelled"].contains(&item.status.as_str()))
    {
        return Err(format!(
            "{source_path} is terminal but retains non-terminal Work Items."
        ));
    }
    Ok(Plan {
        id: required_value(&frontmatter, "id", &source_path)?,
        title,
        status,
        created: required_value(&frontmatter, "created", &source_path)?,
        updated: required_value(&frontmatter, "updated", &source_path)?,
        current_item,
        goal,
        non_goals,
        work_items,
        source_path,
    })
}

fn parse_decision(_path: &Path, source_path: String, text: &str) -> Result<Decision, String> {
    let (frontmatter, body) = parse_frontmatter(text, &source_path)?;
    require_format_version(&frontmatter, &source_path)?;
    let sections = split_h2_sections(body);
    let status = required_value(&frontmatter, "status", &source_path)?;
    if !DECISION_STATUSES.contains(&status.as_str()) {
        return Err(format!(
            "{source_path} uses unsupported Decision status {status}."
        ));
    }
    Ok(Decision {
        id: required_value(&frontmatter, "id", &source_path)?,
        title: parse_title(body, &source_path)?,
        status,
        created: required_value(&frontmatter, "created", &source_path)?,
        accepted: optional_value(&frontmatter, "accepted"),
        scope: required_value(&frontmatter, "scope", &source_path)?,
        supersedes: optional_value(&frontmatter, "supersedes"),
        superseded_by: optional_value(&frontmatter, "superseded_by"),
        decision: section_text(&sections, "Decision", &source_path)?,
        problem: section_text(&sections, "Problem", &source_path)?,
        consequences: section_text(&sections, "Consequences", &source_path)?,
        revisit_when: section_text(&sections, "Revisit when", &source_path)?,
        source_path,
    })
}

fn parse_title(body: &str, source: &str) -> Result<String, String> {
    body.lines()
        .find_map(|line| line.strip_prefix("# "))
        .map(str::trim)
        .filter(|title| !title.is_empty())
        .map(str::to_string)
        .ok_or_else(|| format!("{source} has no H1 title."))
}

fn split_h2_sections(body: &str) -> BTreeMap<String, String> {
    let mut sections = BTreeMap::new();
    let mut current: Option<String> = None;
    let mut lines = Vec::new();
    for line in body.lines() {
        if let Some(heading) = line.strip_prefix("## ") {
            if let Some(name) = current.take() {
                sections.insert(name, lines.join("\n").trim().to_string());
            }
            current = Some(heading.trim().to_string());
            lines.clear();
        } else if current.is_some() {
            lines.push(line);
        }
    }
    if let Some(name) = current {
        sections.insert(name, lines.join("\n").trim().to_string());
    }
    sections
}

fn section_text(
    sections: &BTreeMap<String, String>,
    name: &str,
    source: &str,
) -> Result<String, String> {
    sections
        .get(name)
        .filter(|value| !value.is_empty())
        .cloned()
        .ok_or_else(|| format!("{source} is missing non-empty section {name}."))
}

fn parse_work_items(source: &str, path: &str) -> Result<Vec<WorkItem>, String> {
    let mut blocks: Vec<(String, Vec<String>)> = Vec::new();
    for line in source.lines() {
        if let Some(heading) = line.strip_prefix("### ") {
            blocks.push((heading.trim().to_string(), Vec::new()));
        } else if let Some((_, lines)) = blocks.last_mut() {
            lines.push(line.to_string());
        }
    }
    if blocks.is_empty() {
        return Err(format!("{path} has no Work Items."));
    }
    blocks
        .into_iter()
        .map(|(heading, lines)| parse_work_item(&heading, &lines, path))
        .collect()
}

fn parse_work_item(heading: &str, lines: &[String], path: &str) -> Result<WorkItem, String> {
    let (id, title) = heading
        .split_once(' ')
        .ok_or_else(|| format!("{path} has an invalid Work Item heading."))?;
    let mut fields = HashMap::new();
    let mut steps = Vec::new();
    let mut in_steps = false;
    for line in lines
        .iter()
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
    {
        if line == "Steps:" {
            in_steps = true;
            continue;
        }
        if in_steps
            && line
                .chars()
                .next()
                .is_some_and(|value| value.is_ascii_digit())
        {
            let (_, step) = line
                .split_once('.')
                .ok_or_else(|| format!("{path} has an invalid Step."))?;
            steps.push(step.trim().to_string());
            continue;
        }
        in_steps = false;
        let (key, value) = line
            .split_once(':')
            .ok_or_else(|| format!("{path} contains an invalid field in {id}."))?;
        if fields
            .insert(key.trim().to_string(), value.trim().to_string())
            .is_some()
        {
            return Err(format!("{path} repeats field {key} in {id}."));
        }
    }
    let required = |key: &str| {
        fields
            .get(key)
            .filter(|value| !value.is_empty())
            .cloned()
            .ok_or_else(|| format!("{path} is missing {key} in {id}."))
    };
    let status = required("Status")?;
    if !WORK_STATUSES.contains(&status.as_str()) {
        return Err(format!(
            "{path} uses unsupported Work Item status {status} in {id}."
        ));
    }
    let next_action = fields
        .get("Next action")
        .filter(|value| !value.is_empty())
        .cloned();
    if ["done", "cancelled"].contains(&status.as_str()) && next_action.is_some() {
        return Err(format!(
            "{path} retains Next action on terminal Work Item {id}."
        ));
    }
    if ["todo", "in_progress", "paused"].contains(&status.as_str()) && next_action.is_none() {
        return Err(format!(
            "{path} is missing Next action on non-terminal Work Item {id}."
        ));
    }
    Ok(WorkItem {
        id: id.to_string(),
        title: title.trim().to_string(),
        status,
        depends_on: parse_inline_list(&required("Depends on")?, path)?,
        blocked_by: parse_inline_list(&required("Blocked by")?, path)?,
        decisions: parse_inline_list(&required("Decisions")?, path)?,
        outcome: required("Outcome")?,
        acceptance: required("Acceptance")?,
        steps,
        evidence: parse_inline_list(&required("Evidence")?, path)?,
        next_action,
    })
}

fn reject_duplicate_ids<'a>(ids: impl Iterator<Item = &'a str>, kind: &str) -> Result<(), String> {
    let mut seen = std::collections::HashSet::new();
    for id in ids {
        if !seen.insert(id) {
            return Err(format!("Duplicate {kind} ID {id}."));
        }
    }
    Ok(())
}

fn parse_inline_list(value: &str, source: &str) -> Result<Vec<String>, String> {
    let inner = value
        .strip_prefix('[')
        .and_then(|value| value.strip_suffix(']'))
        .ok_or_else(|| format!("{source} contains an invalid inline list."))?;
    if inner.trim().is_empty() {
        return Ok(Vec::new());
    }
    Ok(inner
        .split(',')
        .map(str::trim)
        .map(str::to_string)
        .collect())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::TempDir;

    fn write(path: &Path, content: &str) {
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        let mut file = fs::File::create(path).unwrap();
        file.write_all(content.as_bytes()).unwrap();
    }

    fn valid_project(active: bool) -> TempDir {
        let temp = tempfile::tempdir().unwrap();
        write(
            &temp.path().join("PROJECT_INDEX.md"),
            if active {
                "---\nformat_version: 1\nactive_plan: PLAN-0001\n---\n"
            } else {
                "---\nformat_version: 1\nactive_plan: null\n---\n"
            },
        );
        let status = if active { "active" } else { "completed" };
        let current = if active { "current_item: W-002\n" } else { "" };
        let second_status = if active { "in_progress" } else { "done" };
        let second_evidence = if active { "[]" } else { "[Observed complete]" };
        let next = if active {
            "Next action: Inspect the rendered project.\n"
        } else {
            ""
        };
        write(
            &temp.path().join("docs/plans/0001-demo.md"),
            &format!("---\nformat_version: 1\nid: PLAN-0001\nstatus: {status}\ncreated: 2026-09-07: this colon stays in the value\nupdated: 2026-09-07\n{current}---\n\n# Demo plan\n\n## Goal\n\nShow the project.\n\n## Non-goals\n\nDo not edit it.\n\n## Work items\n\n### W-001 Read records\n\nStatus: done\nDepends on: []\nBlocked by: []\nDecisions: [ADR-0001]\nOutcome: Records are available.\nAcceptance: The fixture loads.\nEvidence: [Fixture passed]\n\n### W-002 Show status\n\nStatus: {second_status}\nDepends on: [W-001]\nBlocked by: []\nDecisions: [ADR-0001]\nOutcome: Status is visible.\nAcceptance: The rendered view preserves status.\nSteps:\n1. Build the view.\n2. Inspect the view.\nEvidence: {second_evidence}\n{next}"),
        );
        write(
            &temp.path().join("docs/decisions/0001-reader.md"),
            "---\nformat_version: 1\nid: ADR-0001\nstatus: accepted\ncreated: 2026-09-01\naccepted: 2026-09-02\nscope: reader/files\n---\n\n# Read files directly\n\n## Decision\n\nRead canonical files directly.\n\n## Problem\n\nThe viewer needs current state.\n\n## Drivers\n\nLocal state.\n\n## Considered alternatives\n\nA database was rejected.\n\n## Consequences\n\nFiles remain authoritative.\n\n## Confirmation\n\nCompare loaded state.\n\n## Revisit when\n\nThe native format changes.\n",
        );
        temp
    }

    #[test]
    fn reads_active_project_and_preserves_order_and_links() {
        let project = valid_project(true);
        let snapshot = read_project(project.path()).unwrap();
        assert_eq!(snapshot.active_plan.as_deref(), Some("PLAN-0001"));
        assert_eq!(snapshot.plans[0].current_item.as_deref(), Some("W-002"));
        assert_eq!(
            snapshot.plans[0]
                .work_items
                .iter()
                .map(|item| item.id.as_str())
                .collect::<Vec<_>>(),
            ["W-001", "W-002"]
        );
        assert_eq!(snapshot.plans[0].work_items[1].status, "in_progress");
        assert_eq!(snapshot.plans[0].work_items[1].decisions, ["ADR-0001"]);
        assert_eq!(snapshot.decisions[0].status, "accepted");
    }

    #[test]
    fn reads_idle_project_without_inventing_current_work() {
        let project = valid_project(false);
        let snapshot = read_project(project.path()).unwrap();
        assert!(snapshot.active_plan.is_none());
        assert!(snapshot.plans[0].current_item.is_none());
        assert_eq!(snapshot.plans[0].work_items[1].status, "done");
    }

    #[test]
    fn rejects_unsupported_format() {
        let project = valid_project(true);
        write(
            &project.path().join("PROJECT_INDEX.md"),
            "---\nformat_version: 2\nactive_plan: PLAN-0001\n---\n",
        );
        let error = read_project(project.path()).unwrap_err();
        assert!(error.contains("unsupported format_version 2"));
    }

    #[test]
    fn rejects_missing_canonical_paths() {
        let project = tempfile::tempdir().unwrap();
        write(
            &project.path().join("PROJECT_INDEX.md"),
            "---\nformat_version: 1\nactive_plan: null\n---\n",
        );
        let error = read_project(project.path()).unwrap_err();
        assert!(error.contains("Required path is missing"));
    }

    #[test]
    fn reads_supersession_in_both_directions() {
        let project = valid_project(true);
        write(
            &project.path().join("docs/decisions/0002-new-reader.md"),
            "---\nformat_version: 1\nid: ADR-0002\nstatus: accepted\ncreated: 2026-09-03\naccepted: 2026-09-03\nscope: reader/files\nsupersedes: ADR-0001\n---\n\n# Use the new reader\n\n## Decision\n\nUse the new reader.\n\n## Problem\n\nThe old reader is limited.\n\n## Drivers\n\nClarity.\n\n## Considered alternatives\n\nKeep the old reader.\n\n## Consequences\n\nThe new reader is current.\n\n## Confirmation\n\nInspect it.\n\n## Revisit when\n\nThe format changes.\n",
        );
        let old_path = project.path().join("docs/decisions/0001-reader.md");
        let old = fs::read_to_string(&old_path)
            .unwrap()
            .replace("status: accepted", "status: superseded")
            .replace(
                "scope: reader/files",
                "scope: reader/files\nsuperseded_by: ADR-0002",
            );
        write(&old_path, &old);
        let snapshot = read_project(project.path()).unwrap();
        assert_eq!(
            snapshot.decisions[0].superseded_by.as_deref(),
            Some("ADR-0002")
        );
        assert_eq!(
            snapshot.decisions[1].supersedes.as_deref(),
            Some("ADR-0001")
        );
    }

    #[test]
    fn rejects_unknown_status_before_it_reaches_the_view_model() {
        let project = valid_project(true);
        let path = project.path().join("docs/plans/0001-demo.md");
        let content = fs::read_to_string(&path)
            .unwrap()
            .replace("Status: in_progress", "Status: almost_done");
        write(&path, &content);
        let error = read_project(project.path()).unwrap_err();
        assert!(error.contains("unsupported Work Item status almost_done"));
    }

    #[test]
    fn rejects_truncated_frontmatter_without_panicking() {
        let error = parse_frontmatter("---", "truncated.md").unwrap_err();
        assert!(error.contains("unterminated frontmatter"));
    }

    #[test]
    fn rejects_duplicate_work_item_ids() {
        let project = valid_project(true);
        let path = project.path().join("docs/plans/0001-demo.md");
        let content = fs::read_to_string(&path)
            .unwrap()
            .replace("current_item: W-002", "current_item: W-001")
            .replace("### W-002 Show status", "### W-001 Show status");
        write(&path, &content);

        let error = read_project(project.path()).unwrap_err();
        assert!(error.contains("Duplicate Work Item ID W-001"));
    }

    #[test]
    fn rejects_in_progress_work_that_is_not_current() {
        let project = valid_project(true);
        let path = project.path().join("docs/plans/0001-demo.md");
        let content = fs::read_to_string(&path)
            .unwrap()
            .replace("current_item: W-002", "current_item: W-001")
            .replacen("Status: done", "Status: paused", 1)
            .replace(
                "Evidence: [Fixture passed]",
                "Evidence: []\nNext action: Resume reading.",
            );
        write(&path, &content);

        let error = read_project(project.path()).unwrap_err();
        assert!(error.contains("not its sole current item"));
    }

    #[test]
    fn reads_cancelled_history_with_unfinished_work() {
        let project = valid_project(false);
        let path = project.path().join("docs/plans/0001-demo.md");
        let content = fs::read_to_string(&path)
            .unwrap()
            .replace("status: completed", "status: cancelled")
            .replace(
                "Status: done\nDepends on: [W-001]",
                "Status: todo\nDepends on: [W-001]",
            )
            .replace(
                "Evidence: [Observed complete]",
                "Evidence: []\nNext action: Resume only if this Plan is reactivated.",
            );
        write(&path, &content);

        let snapshot = read_project(project.path()).unwrap();
        assert_eq!(snapshot.plans[0].status, "cancelled");
        assert_eq!(snapshot.plans[0].work_items[1].status, "todo");
    }

    #[test]
    fn rejects_a_canonical_record_outside_the_project_root() {
        let project = tempfile::tempdir().unwrap();
        let outside = tempfile::NamedTempFile::new().unwrap();
        let error = contained_path(project.path(), outside.path(), true).unwrap_err();
        assert!(error.contains("leaves the selected project"));
    }

}
