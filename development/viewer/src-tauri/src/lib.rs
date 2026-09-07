mod config;
mod reader;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            reader::scan_project,
            config::load_project_registry,
            config::save_project_registry
        ])
        .run(tauri::generate_context!())
        .expect("error while running Scoville Plan Viewer");
}
