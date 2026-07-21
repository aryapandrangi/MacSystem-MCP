# MacSystem-Mcp: macOS FastMCP Workstation Control & Automation Server

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Server-green)](https://github.com/jlowin/fastmcp)
[![Tools Count](https://img.shields.io/badge/Tools-87%20Registered-orange)](#features--tool-categories-87-tools)

`MacSystem-Mcp` is a high-performance **Python FastMCP server** exposing **87 native macOS system tools**, workstation control automations, keyboard/mouse input simulators, filesystem utilities, Finder managers, process managers, audio controls, timers, notifications, and application integrations (Apple Notes, Calendar, Contacts, Mail, iMessage, Safari, and Terminal) as Model Context Protocol (MCP) tools.

---

## Quick Start Configuration

Add `macsystem-mcp` to your `claude_desktop_config.json` (or Cursor / Windsurf MCP configuration):

```json
{
  "mcpServers": {
    "macsystem-mcp": {
      "command": "uvx",
      "args": ["macsystem-mcp"]
    }
  }
}
```

Or for local development:

```json
{
  "mcpServers": {
    "macsystem-mcp": {
      "command": "/path/to/MacSystem-Mcp/.venv/bin/macsystem-mcp",
      "args": []
    }
  }
}
```

---

## Local Python Installation & Setup

### Prerequisites
- macOS 12+ (Monterey, Ventura, Sonoma, Sequoia)
- Python 3.10+ installed

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/aryapandrangi/MacSystem-Mcp.git
cd MacSystem-Mcp

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Running the FastMCP Server

### 1. Visual Web UI Inspector (Human Testing)
Launch the interactive web browser inspector interface at `http://localhost:5173`:

```bash
source .venv/bin/activate
fastmcp dev inspector mac_server.py
```
*Opens an interactive visual browser dashboard where you can click any of the 87 tools, enter parameters, and execute them live!*

### 2. Standalone MCP Server (STDIO Mode)
Run the server process listening on standard input/output for LLM clients:

```bash
source .venv/bin/activate
python3 mac_server.py
```

---

## Automated Testing & Spoken Voice Reports

To run the automated test suite across all 87 tools with spoken audio voice notifications:

```bash
source .venv/bin/activate
python3 tests/test_mac_mcp.py
```

### Key Testing Features:
- **Spoken Audio Voice Notifications**: Announces *"Testing started"* at start and spoken summary at end (*"81 tools passed, 0 tools failed..."*).
- **Timestamped Reports**: Generates detailed Markdown & JSON test reports under `tests/reports/report_YYYY-MM-DD_HH-MM-SS/`.
- **Strict Guardrails**: Finder tag operations and filesystem modifications are strictly locked to `/tmp/` and will **never** modify or tag user files.

---

## Features & Tool Categories (87 Tools)

1. **System & Power**: Volume output (`set_volume`, `get_volume`), dark mode (`toggle_dark_mode`), system stats (`get_system_stats`), Wi-Fi power (`wifi_control`), text-to-speech (`say_speech`), display lock (`lock_screen`), power controls (`system_power`), date/time info (`get_date_time`).
2. **Window & Workspace Management**: Active window detection (`get_active_window`), app listing (`list_applications`, `list_apps`), focus app/window (`focus_app`, `focus_window`), position & dimension controls (`move_window`, `resize_window`), Mission Control desktop space switching (`set_space`).
3. **Input & Human Automation**: Keystrokes & shortcuts (`keystroke_action`, `key_press`, `type_text`), mouse cursor positioning & drag & scroll (`mouse_move`, `mouse_click`, `mouse_drag`, `mouse_scroll`), macOS Shortcuts execution with 15s timeout protection (`shortcut_list`, `shortcut_run`), wait delays (`wait_ms`).
4. **Filesystem Operations**: File CRUD (`fs_read`, `fs_read_many`, `fs_write`, `fs_edit`), PDF document creation (`fs_write_pdf`), list & stat metadata (`fs_list`, `fs_stat`), copy & move (`fs_copy`, `fs_move`), directory creation (`fs_mkdir`), permanent delete (`fs_delete`), directory watcher (`fs_watch_once`), macOS extended attributes (`fs_xattr_get`, `fs_xattr_set`).
5. **Finder & Workspace**: Reveal in Finder (`reveal_in_finder`), selected item getter (`get_finder_selection`), color tagging (`set_finder_tags`), QuickLook preview (`quick_look`), Trash operations (`move_to_trash`, `empty_trash`), Spotlight search CLI (`spotlight_search`).
6. **Process Management**: Synchronous shell command execution (`process_run`), background process launcher (`process_start`), stream stdout/stderr output (`process_read_output`), send stdin input (`process_write_input`), process termination & process list (`process_terminate`, `process_list`, `process_kill`).
7. **Media & Audio**: Media playback play/pause/next/previous (`media_control`).
8. **Timers & Reminders**: macOS Reminders app management (`reminders_action`), native Clock app timer control (`timer_action`).
9. **AppleScript & UI**: Native AppleScript engine (`run_applescript`), screencapture (`take_screenshot`, `capture_screen`), accessibility hierarchy inspector (`get_accessibility_tree`), system & display info (`get_system_info`, `get_screen_info`), clipboard read/write (`clipboard_action`, `clipboard_read`, `clipboard_write`), macOS banner notifications (`notify`), modal prompts (`prompt_user`).
10. **App Integrations**: Mail (`mail`, `mail_send_draft`), Calendar (`calendar`, `calendar_create`), Contacts (`contacts_search`), iMessage (`messages`), Safari (`safari`), Notes (`notes`, `notes_create`), Terminal/iTerm2 (`terminal`), iPhone Mirroring info (`iphone_mirror_info`), Image analysis (`analyze_image`), Local OKF Knowledge Catalog (`get_knowledge_document`, `update_knowledge_document`).

---

## License

MIT License. Free to use, modify, and distribute for personal and commercial applications.
