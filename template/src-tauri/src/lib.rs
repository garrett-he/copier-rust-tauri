#[tauri::command]
fn greet(name: &str) -> String {
    if name.is_empty() {
        String::from("Hello, stranger! You've been greeted from Rust!")
    } else {
        format!("Hello, {}! You've been greeted from Rust!", name)
    }
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet_command() {
        let result = greet("TestUser");
        assert_eq!(result, "Hello, TestUser! You've been greeted from Rust!");
    }

    #[test]
    fn test_greet_command_empty() {
        let result = greet("");
        assert_eq!(result, "Hello, stranger! You've been greeted from Rust!");
    }
}
