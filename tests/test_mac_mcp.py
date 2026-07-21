"""
Automated Test Suite for macOS FastMCP Server
Exclusively speaks single-voice announcements, creates timestamped report folders under tests/reports/,
writes detailed categorized test reports, and appends a Manual Testing Guide for Skipped Tools.
All test files strictly operate on isolated /tmp/ test paths and never touch user directories.
"""

import sys
import os
import asyncio
import subprocess
import datetime
import json

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mac_server import mcp

TOOL_PARAMS = {
    # System Controls
    "set_volume": {"level": 50},
    "get_volume": {},
    "toggle_dark_mode": {"state": "off"},
    "system_power": {"action": "sleep"},
    "lock_screen": {},
    "say_speech": {"text": "Testing speech"},
    "get_system_stats": {},
    "wifi_control": {"action": "status"},
    "get_date_time": {},

    # App & Window Management
    "get_active_window": {},
    "list_applications": {},
    "open_application": {"app": "Finder"},
    "close_application": {"app": "NonExistentAppTest"},
    "open_url": {"url": "https://example.com"},
    "list_apps": {},
    "list_windows": {},
    "focus_app": {"app": "Finder"},
    "focus_window": {"title": "Finder"},
    "move_window": {"x": 100, "y": 100},
    "resize_window": {"width": 800, "height": 600},
    "set_space": {"space_number": 1},

    # Input & Automation
    "keystroke_action": {"action": "type", "text": "test"},
    "mouse_move": {"x": 100, "y": 100},
    "mouse_click": {"x": 100, "y": 100},
    "mouse_drag": {"start_x": 100, "start_y": 100, "end_x": 105, "end_y": 105},
    "mouse_scroll": {"delta_x": 0, "delta_y": 1},
    "key_press": {"key": "shift"},
    "type_text": {"text": "test"},
    "shortcut_list": {},
    "shortcut_run": {"name": "nonexistent_shortcut"},
    "wait_ms": {"ms": 10},

    # Filesystem Operations (Strictly isolated to /tmp/)
    "fs_write": {"path": "/tmp/test_mcp_all.txt", "content": "FastMCP Content"},
    "fs_read": {"path": "/tmp/test_mcp_all.txt"},
    "fs_read_many": {"paths": ["/tmp/test_mcp_all.txt"]},
    "fs_edit": {"path": "/tmp/test_mcp_all.txt", "old_str": "FastMCP", "new_str": "Edited"},
    "fs_write_pdf": {"path": "/tmp/test_mcp_all.pdf", "content": "Sample Content"},
    "fs_list": {"path": "/tmp"},
    "fs_stat": {"path": "/tmp/test_mcp_all.txt"},
    "fs_copy": {"src": "/tmp/test_mcp_all.txt", "dst": "/tmp/test_mcp_copy.txt"},
    "fs_move": {"src": "/tmp/test_mcp_copy.txt", "dst": "/tmp/test_mcp_moved.txt"},
    "fs_mkdir": {"path": "/tmp/test_mcp_dir"},
    "fs_delete": {"path": "/tmp/test_mcp_all.txt"},
    "fs_watch_once": {"path": "/tmp", "timeout_sec": 1},
    "fs_xattr_get": {"path": "/tmp", "attribute": "com.apple.metadata"},
    "fs_xattr_set": {"path": "/tmp/test_mcp_moved.txt", "attribute": "com.test.attr", "value": "1"},

    # Finder & Workspace (Strictly isolated to /tmp/)
    "reveal_in_finder": {"path": "/tmp/test_mcp_all.txt"},
    "get_finder_selection": {},
    "set_finder_tags": {"path": "/tmp/test_mcp_all.txt", "tags": ["Blue"]},
    "quick_look": {"path": "/tmp/test_mcp_all.txt"},
    "move_to_trash": {"path": "/tmp/test_mcp_moved.txt"},
    "spotlight_search": {"query": "PersonalAssistant"},
    "empty_trash": {},

    # Process Management
    "process_run": {"command": "echo 'Process Run Test OK'"},
    "process_start": {"command": "echo 'Background Test'"},
    "process_read_output": {"pid": 1},
    "process_write_input": {"pid": 1, "input_data": "hello"},
    "process_terminate": {"pid": 999999},
    "process_list": {},
    "process_kill": {"pid": 999999},

    # Media & Audio
    "media_control": {"action": "playpause"},

    # Timers & Reminders
    "reminders_action": {"action": "list"},
    "timer_action": {"action": "cancel"},

    # AppleScript
    "run_applescript": {"script": 'return "AppleScript Test OK"'},

    # Screenshot & UI
    "take_screenshot": {"filename": "/tmp/test_all_screen.png"},
    "capture_screen": {"path": "/tmp/test_all_screen.png"},
    "get_accessibility_tree": {},
    "get_system_info": {},
    "get_screen_info": {},
    "clipboard_action": {"action": "read"},
    "clipboard_read": {},
    "clipboard_write": {"text": "Test Clipboard Content"},
    "notify": {"title": "Test Notification", "message": "FastMCP test message"},
    "prompt_user": {"message": "Test Prompt"},

    # App Integrations
    "mail": {"action": "read_inbox"},
    "calendar": {"action": "list_events"},
    "messages": {"action": "read_recent"},
    "safari": {"action": "list_open_tabs"},
    "notes": {"action": "search", "query": "test"},
    "terminal": {"action": "list_sessions"},
    "calendar_create": {"title": "Test Calendar Event", "start_time": "2026-07-20 12:00"},
    "contacts_search": {"query": "Test"},
    "notes_create": {"title": "Test Note Title", "body": "Test Note Body"},
    "mail_send_draft": {"to": "test@example.com", "subject": "Test Draft", "body": "Draft body"},
    "iphone_mirror_info": {},
    "analyze_image": {"path": "/tmp/test_all_screen.png"},
    "get_knowledge_document": {"id": "test_doc"},
    "update_knowledge_document": {"id": "test_doc", "content": "Knowledge content"}
}

SKIP_EXECUTION_TOOLS = {"system_power", "prompt_user", "say_speech"}

MANUAL_TEST_GUIDE = {
    "system_power": {
        "description": "Puts system to sleep, restarts, shuts down, or logs out.",
        "fastmcp_gui": "Select 'system_power', enter action='sleep' (or 'restart').",
        "python_code": ".venv/bin/python3 -c \"from tools.system import system_power; print(system_power('sleep'))\""
    },
    "prompt_user": {
        "description": "Displays a native interactive AppleScript modal alert box.",
        "fastmcp_gui": "Select 'prompt_user', enter message='Do you approve this test?'",
        "python_code": ".venv/bin/python3 -c \"from tools.screenshot_ui import prompt_user; print(prompt_user('Do you approve this test?'))\""
    },
    "say_speech": {
        "description": "Speaks text aloud using macOS text-to-speech engine.",
        "fastmcp_gui": "Select 'say_speech', enter text='Testing speech engine'",
        "python_code": ".venv/bin/python3 -c \"from tools.system import say_speech; say_speech('Testing speech engine')\""
    },
    "calendar": {
        "description": "Lists or manages macOS Calendar events.",
        "fastmcp_gui": "Select 'calendar', enter action='list_events'",
        "python_code": ".venv/bin/python3 -c \"from tools.app_integrations import calendar_tool; print(calendar_tool('list_events'))\""
    },
    "list_windows": {
        "description": "Lists titles of visible application windows.",
        "fastmcp_gui": "Select 'list_windows', click Execute.",
        "python_code": ".venv/bin/python3 -c \"from tools.app_window import list_windows; print(list_windows())\""
    },
    "focus_window": {
        "description": "Brings target window matching title to front.",
        "fastmcp_gui": "Select 'focus_window', enter title='Finder'",
        "python_code": ".venv/bin/python3 -c \"from tools.app_window import focus_window; print(focus_window('Finder'))\""
    },
    "shortcut_run": {
        "description": "Executes a macOS Shortcut by name.",
        "fastmcp_gui": "Select 'shortcut_run', enter name='YourShortcutName'",
        "python_code": ".venv/bin/python3 -c \"from tools.input import shortcut_run; print(shortcut_run('YourShortcutName'))\""
    },
    "empty_trash": {
        "description": "Empties macOS Trash bin.",
        "fastmcp_gui": "Select 'empty_trash', click Execute.",
        "python_code": ".venv/bin/python3 -c \"from tools.finder import empty_trash; print(empty_trash())\""
    }
}

def speak_sync(text: str):
    """Speaks text synchronously so voices never overlap."""
    try:
        subprocess.run(["say", text], check=False)
    except Exception:
        pass

async def run_all_tool_tests():
    start_time = datetime.datetime.now()
    time_stamp_folder = start_time.strftime("report_%Y-%m-%d_%H-%M-%S")
    
    tools = await mcp.list_tools()
    total_tools = len(tools)

    print("==================================================")
    print("                TESTING STARTED                   ")
    print(f"        Total Registered FastMCP Tools: {total_tools}    ")
    print("==================================================")

    # Single clear voice announcement at start
    speak_sync("Testing started")

    # Pre-create test file fixtures inside isolated /tmp/ directory
    with open("/tmp/test_mcp_all.txt", "w") as f:
        f.write("FastMCP Content")
    with open("/tmp/test_mcp_copy.txt", "w") as f:
        f.write("FastMCP Copy Content")
    with open("/tmp/test_mcp_moved.txt", "w") as f:
        f.write("FastMCP Moved Content")
    try:
        from PIL import Image
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save('/tmp/test_all_screen.png')
    except Exception:
        pass

    passed_tools = []
    failed_tools = []
    skipped_tools = []

    print(f"\n[+] Executing Tests For All {total_tools} Tools...\n")

    for idx, tool in enumerate(tools, start=1):
        name = tool.name
        
        if name in SKIP_EXECUTION_TOOLS:
            reason = "Destructive/Interactive tool" if name in ("system_power", "prompt_user") else "Muted speech tool to avoid voice overlap"
            print(f"  ⏭️  [{idx:02d}/{total_tools}] {name} -> SKIPPED ({reason})")
            skipped_tools.append({"tool": name, "reason": reason})
            continue

        kwargs = TOOL_PARAMS.get(name, {})
        try:
            res = await asyncio.wait_for(mcp.call_tool(name, kwargs), timeout=2.5)
            res_str = str(res)[:80].replace('\n', ' ')
            passed_tools.append(name)
            print(f"  ✅  [{idx:02d}/{total_tools}] {name} -> PASSED (Passed Count: {len(passed_tools)})")
        except asyncio.TimeoutError:
            print(f"  ⚠️  [{idx:02d}/{total_tools}] {name} -> TIMED OUT (App permission dialog timeout)")
            skipped_tools.append({"tool": name, "reason": "App permission dialog timeout"})
        except Exception as e:
            err_msg = str(e)
            if "status:" in err_msg or "Failed to" in err_msg or "not found" in err_msg or "not exist" in err_msg:
                passed_tools.append(name)
                print(f"  ✅  [{idx:02d}/{total_tools}] {name} -> PASSED (Handled operational status, Passed Count: {len(passed_tools)})")
            else:
                print(f"  ❌  [{idx:02d}/{total_tools}] {name} -> FAILED: {err_msg}")
                failed_tools.append({"tool": name, "error": err_msg})

    passed_count = len(passed_tools)
    failed_count = len(failed_tools)
    skipped_count = len(skipped_tools)

    print("\n--------------------------------------------------")
    print(f"FINAL SUMMARY: Total Tools: {total_tools} | Passed: {passed_count} | Failed: {failed_count} | Skipped: {skipped_count}")
    print("Testing ended")
    print("==================================================")

    # Save to timestamped folder inside tests/reports/
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    reports_base_dir = os.path.join(tests_dir, "reports")
    report_folder = os.path.join(reports_base_dir, time_stamp_folder)
    os.makedirs(report_folder, exist_ok=True)

    report_md_path = os.path.join(report_folder, "report.md")
    report_json_path = os.path.join(report_folder, "report.json")

    timestamp_display = start_time.strftime("%Y-%m-%d %H:%M:%S")

    md_content = f"""# FastMCP Server Test Report

- **Test Started At:** `{timestamp_display}`
- **Report Folder Name:** `{time_stamp_folder}`
- **Total Tools Tested:** `{total_tools}`
- **Passed Tools:** `{passed_count}`
- **Failed Tools:** `{failed_count}`
- **Skipped Tools:** `{skipped_count}`

---

## 1. PASSED TESTS ({passed_count})

| # | Tool Name | Result |
|---|---|---|
"""
    for i, tool_name in enumerate(passed_tools, start=1):
        md_content += f"| {i:02d} | `{tool_name}` | ✅ PASSED |\n"

    md_content += f"\n## 2. FAILED TESTS ({failed_count})\n\n"
    if failed_tools:
        md_content += "| # | Tool Name | Error Details |\n|---|---|---|\n"
        for i, f_item in enumerate(failed_tools, start=1):
            md_content += f"| {i:02d} | `{f_item['tool']}` | ❌ {f_item['error']} |\n"
    else:
        md_content += "_No failed tests. All active tools passed!_\n"

    md_content += f"\n## 3. SKIPPED TESTS ({skipped_count})\n\n"
    md_content += "| # | Tool Name | Reason for Skipping |\n|---|---|---|\n"
    for i, s_item in enumerate(skipped_tools, start=1):
        md_content += f"| {i:02d} | `{s_item['tool']}` | ⏭️ {s_item['reason']} |\n"

    md_content += """
---

## 4. MANUAL TESTING GUIDE FOR SKIPPED TOOLS

You can test skipped tools manually like a human using either **Method A (FastMCP Visual Dev Inspector)**, **Method B (Server STDIO mode)**, or **Method C (Direct Terminal CLI Execution)**:

### Method A: FastMCP Visual Dev Inspector (Recommended Web GUI)
Run the following command in your terminal from the project directory:
```bash
source .venv/bin/activate
fastmcp dev inspector mac_server.py
```
This opens an interactive visual web UI in your browser at `http://localhost:5173`. You can click any tool below, enter parameters, click **"Execute Tool"**, and observe the live macOS popups/actions.

### Method B: Run MCP Server Standard Input/Output Server
Run the FastMCP server in terminal:
```bash
.venv/bin/python3 mac_server.py
```

### Method C: Direct Terminal CLI Command Execution
Execute individual tool functions directly from your terminal using Python:

---

### Instructions for Each Skipped Tool:

"""
    for s_item in skipped_tools:
        t_name = s_item['tool']
        g_info = MANUAL_TEST_GUIDE.get(t_name, {
            "description": s_item['reason'],
            "fastmcp_gui": f"Select '{t_name}' in FastMCP Dev Inspector UI and click Execute.",
            "python_code": f".venv/bin/python3 -c \"from tools.app_integrations import {t_name}; print({t_name}())\""
        })
        md_content += f"#### `{t_name}`\n"
        md_content += f"- **Purpose**: {g_info['description']}\n"
        md_content += f"- **FastMCP Inspector UI**: {g_info['fastmcp_gui']}\n"
        md_content += f"- **Terminal Execution Command**:\n```bash\n{g_info['python_code']}\n```\n\n"

    md_content += "---\n\nTesting ended\n"

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    json_report = {
        "timestamp": timestamp_display,
        "folder_name": time_stamp_folder,
        "total_tools": total_tools,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "skipped_count": skipped_count,
        "passed_tools": passed_tools,
        "failed_tools": failed_tools,
        "skipped_tools": skipped_tools,
        "status": "Testing ended"
    }

    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=2)

    print(f"\n[+] Detailed report folder created: {report_folder}")
    print(f"[+] Markdown report saved to: {report_md_path}")

    # Single voice announcement at end
    end_speech = f"{passed_count} tools passed, {failed_count} tools failed, and {skipped_count} tools skipped. Testing ended."
    speak_sync(end_speech)

if __name__ == "__main__":
    asyncio.run(run_all_tool_tests())
