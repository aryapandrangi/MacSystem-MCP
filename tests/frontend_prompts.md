# Frontend Chat Test Prompts (87 Tools)

Use these natural language prompts to test each tool via the Frontend Chat interface:

## 1. System Controls
- `set_volume`: "Set system volume to 60%"
- `get_volume`: "What is the current system volume?"
- `toggle_dark_mode`: "Turn on dark mode on my Mac"
- `system_power`: "Put my Mac to sleep"
- `lock_screen`: "Lock my Mac screen"
- `say_speech`: "Say out loud 'Hello, welcome to Jarvis Personal Assistant'"
- `get_system_stats`: "Show me CPU usage, RAM, disk space, and battery stats"
- `wifi_control`: "Check the current Wi-Fi status on my Mac"
- `get_date_time`: "What is the current local date, time, and timezone?"

## 2. App & Window Management
- `get_active_window`: "Which application window is currently active?"
- `list_applications`: "List all running applications on my Mac"
- `open_application`: "Open Finder on my Mac"
- `close_application`: "Quit Calculator application"
- `open_url`: "Open https://github.com in my default web browser"
- `list_apps`: "Show all active GUI applications"
- `list_windows`: "List all visible window titles"
- `focus_app`: "Focus on Finder"
- `focus_window`: "Focus on the window named Finder"
- `move_window`: "Move the front window to coordinates (100, 100)"
- `resize_window`: "Resize the active window to 800 width and 600 height"
- `set_space`: "Switch to Mission Control Desktop space 1"

## 3. Input & Automation
- `keystroke_action`: "Press Command+Space shortcut to open Spotlight"
- `mouse_move`: "Move mouse cursor to coordinates (500, 400)"
- `mouse_click`: "Click mouse button at coordinates (500, 400)"
- `mouse_drag`: "Drag mouse from (100, 100) to (300, 300)"
- `mouse_scroll`: "Scroll down 5 units"
- `key_press`: "Press the Return key"
- `type_text`: "Type 'Hello world' on keyboard"
- `shortcut_list`: "List all configured macOS Shortcuts"
- `shortcut_run`: "Run macOS Shortcut named 'Daily Briefing'"
- `wait_ms`: "Wait for 500 milliseconds"

## 4. Filesystem Operations
- `fs_read`: "Read content of file ~/Desktop/sample.txt"
- `fs_read_many`: "Read contents of ~/Desktop/file1.txt and ~/Desktop/file2.txt"
- `fs_write`: "Create a file at ~/Desktop/notes.txt with content 'Meeting Notes'"
- `fs_edit`: "In file ~/Desktop/notes.txt replace 'Meeting' with 'Project'"
- `fs_write_pdf`: "Create a PDF file at ~/Desktop/doc.pdf with text 'Quarterly Report'"
- `fs_list`: "List all files in directory ~/Desktop"
- `fs_stat`: "Show file statistics for ~/Desktop/notes.txt"
- `fs_copy`: "Copy ~/Desktop/notes.txt to ~/Desktop/notes_backup.txt"
- `fs_move`: "Rename ~/Desktop/notes_backup.txt to ~/Desktop/notes_v2.txt"
- `fs_mkdir`: "Create a directory ~/Desktop/NewFolder"
- `fs_delete`: "Delete file ~/Desktop/notes_v2.txt"
- `fs_watch_once`: "Watch directory ~/Desktop for modifications for 3 seconds"
- `fs_xattr_get`: "Get extended attribute com.apple.metadata on ~/Desktop/doc.pdf"
- `fs_xattr_set`: "Set extended attribute com.test.tag to 'custom' on ~/Desktop/doc.pdf"

## 5. Finder & Workspace
- `reveal_in_finder`: "Reveal file ~/Desktop/doc.pdf in Finder"
- `get_finder_selection`: "Get selected items in Finder"
- `set_finder_tags`: "Set Blue color tag on file ~/Desktop/doc.pdf"
- `quick_look`: "Open QuickLook preview for ~/Desktop/doc.pdf"
- `move_to_trash`: "Move ~/Desktop/doc.pdf to Trash"
- `spotlight_search`: "Search Spotlight for files matching 'PersonalAssistant'"
- `empty_trash`: "Empty the macOS Trash"

## 6. Process Management
- `process_run`: "Run shell command 'uptime'"
- `process_start`: "Start background command 'ping google.com'"
- `process_read_output`: "Read output of background process PID 1234"
- `process_write_input`: "Send input 'y' to background process PID 1234"
- `process_terminate`: "Gracefully terminate process PID 1234"
- `process_list`: "List all running processes"
- `process_kill`: "Force kill process PID 1234"

## 7. Media & Audio
- `media_control`: "Toggle media play/pause"

## 8. Timers & Reminders
- `reminders_action`: "List all my macOS Reminders"
- `timer_action`: "Set a timer for 5 minutes labeled 'Pizza'"

## 9. AppleScript
- `run_applescript`: "Run AppleScript 'return (system info)'"

## 10. Screenshot & UI
- `take_screenshot`: "Take a screenshot and save it to ~/Desktop/screen.png"
- `capture_screen`: "Capture screen to ~/Desktop/capture.png"
- `get_accessibility_tree`: "Get accessibility tree for active window"
- `get_system_info`: "Get macOS hardware and OS build info"
- `get_screen_info`: "Get display resolution and screen dimensions"
- `clipboard_action`: "Read text from clipboard"
- `clipboard_read`: "Read clipboard contents"
- `clipboard_write`: "Copy text 'Personal Assistant Code' to clipboard"
- `notify`: "Display a notification titled 'Task Done' with message 'Build completed successfully'"
- `prompt_user`: "Display an interactive dialog prompt asking 'Do you want to proceed?'"

## 11. App Integrations
- `mail`: "Read recent emails in my Mail inbox"
- `calendar`: "List upcoming events in my Calendar"
- `messages`: "Show recent iMessage chat conversations"
- `safari`: "List all open tabs in Safari"
- `notes`: "Search Apple Notes for 'ideas'"
- `terminal`: "List open sessions in Terminal"
- `calendar_create`: "Create a calendar event titled 'Team Sync' tomorrow at 2 PM"
- `contacts_search`: "Search contacts for 'John'"
- `notes_create`: "Create a note in Apple Notes titled 'Shopping List' with content 'Milk, Eggs, Coffee'"
- `mail_send_draft`: "Compose a draft email to 'alex@example.com' with subject 'Project Update'"
- `iphone_mirror_info`: "Check if iPhone Mirroring is running"
- `analyze_image`: "Analyze image file ~/Desktop/screen.png"
- `get_knowledge_document`: "Get knowledge document 'architecture'"
- `update_knowledge_document`: "Update knowledge document 'architecture' with content 'System Overview'"
