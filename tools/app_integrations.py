import os
import json
import subprocess
from typing import Optional, List, Dict, Any
from .applescript import run_applescript

def mail_tool(
    action: str,
    account: Optional[str] = None,
    limit: int = 10,
    message_id: Optional[str] = None,
    to: Optional[str] = None,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    query: Optional[str] = None
) -> str:
    """Interact with macOS Mail app: 'read_inbox', 'read_message', 'send_draft', or 'search'."""
    act = action.lower().strip()
    try:
        if act == "read_inbox":
            script = f'''
            tell application "Mail"
                set inboxMsgs to messages of inbox
                set outputText to ""
                set msgCount to count of inboxMsgs
                if msgCount > {limit} then set msgCount to {limit}
                repeat with i from 1 to msgCount
                    set m to item i of inboxMsgs
                    set outputText to outputText & (id of m as string) & ";" & (sender of m) & ";" & (subject of m) & ";" & (date received of m as string) & "\\n"
                end repeat
                return outputText
            end tell
            '''
            res = run_applescript(script)
            if not res or not res.strip():
                return "Inbox is empty or unreadable."
            msgs = []
            for line in res.strip().split("\n"):
                parts = line.split(";")
                if len(parts) >= 4:
                    msgs.append({"id": parts[0], "sender": parts[1], "subject": parts[2], "date": parts[3]})
            return json.dumps(msgs, indent=2)

        elif act == "read_message":
            if not message_id:
                raise ValueError("message_id is required for read_message")
            script = f'''
            tell application "Mail"
                set m to first message of inbox whose id is {message_id}
                return (sender of m) & "\\n" & (subject of m) & "\\n" & (content of m)
            end tell
            '''
            return run_applescript(script)

        elif act == "send_draft":
            if not to or not subject or not body:
                raise ValueError("to, subject, and body are required for send_draft")
            script = f'''
            tell application "Mail"
                set msg to make new outgoing message with properties {{subject:"{subject.replace('"', '\\"')}", content:"{body.replace('"', '\\"')}", visible:true}}
                tell msg
                    make new to recipient at end of to recipients with properties {{address:"{to}"}}
                end tell
            end tell
            '''
            run_applescript(script)
            return f"Created Mail draft to '{to}' with subject '{subject}'."

        elif act == "search":
            if not query:
                raise ValueError("query is required for search action")
            script = f'''
            tell application "Mail"
                set foundMsgs to messages of inbox whose subject contains "{query.replace('"', '\\"')}" or content contains "{query.replace('"', '\\"')}"
                set outputText to ""
                repeat with m in foundMsgs
                    set outputText to outputText & (id of m as string) & ";" & (sender of m) & ";" & (subject of m) & "\\n"
                end repeat
                return outputText
            end tell
            '''
            res = run_applescript(script)
            return f"Mail search results for '{query}':\n{res}"
        else:
            raise ValueError(f"Unknown mail action: {action}")
    except Exception as e:
        return f"Mail action status: {e}"

def calendar_tool(
    action: str,
    calendar_name: Optional[str] = None,
    limit: int = 10,
    title: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    location: Optional[str] = None,
    event_id: Optional[str] = None
) -> str:
    """Interact with macOS Calendar app: 'list_events', 'create_event', or 'delete_event'."""
    act = action.lower().strip()
    try:
        if act == "list_events":
            script = '''
            tell application "Calendar"
                set evts to every event of calendar 1
                set outputText to ""
                repeat with e in evts
                    set outputText to outputText & (summary of e) & " (" & (start date of e as string) & ")\\n"
                end repeat
                return outputText
            end tell
            '''
            res = run_applescript(script)
            return f"Calendar Events:\n{res}"

        elif act == "create_event":
            if not title:
                raise ValueError("title is required for create_event")
            script = f'''
            tell application "Calendar"
                tell calendar 1
                    make new event with properties {{summary:"{title.replace('"', '\\"')}"}}
                end tell
            end tell
            '''
            run_applescript(script)
            return f"Created event '{title}' in Calendar."

        elif act == "delete_event":
            if not event_id and not title:
                raise ValueError("event_id or title is required for delete_event")
            search_str = title or event_id
            script = f'''
            tell application "Calendar"
                tell calendar 1
                    delete (first event whose summary contains "{search_str.replace('"', '\\"')}")
                end tell
            end tell
            '''
            run_applescript(script)
            return f"Deleted event matching '{search_str}' from Calendar."
        else:
            raise ValueError(f"Unknown calendar action: {action}")
    except Exception as e:
        return f"Calendar action status: {e}"

def messages_tool(
    action: str,
    recipient: Optional[str] = None,
    text: Optional[str] = None,
    limit: int = 10
) -> str:
    """Interact with iMessage/Messages app: 'send' or 'read_recent'."""
    act = action.lower().strip()
    try:
        if act == "send":
            if not recipient or not text:
                raise ValueError("recipient and text are required for send action")
            script = f'''
            tell application "Messages"
                set targetService to 1st service whose service type is iMessage
                set targetBuddy to buddy "{recipient}" of targetService
                send "{text.replace('"', '\\"')}" to targetBuddy
            end tell
            '''
            run_applescript(script)
            return f"Sent iMessage to '{recipient}'."
        elif act == "read_recent":
            script = '''
            tell application "Messages"
                try
                    return name of every chat
                on error err
                    return "No active chat sessions: " & err
                end try
            end tell
            '''
            res = run_applescript(script)
            return f"Recent Messages:\n{res}"
        else:
            raise ValueError(f"Unknown messages action: {action}")
    except Exception as e:
        return f"Messages action status: {e}"

def safari_tool(
    action: str,
    url: Optional[str] = None,
    js_script: Optional[str] = None
) -> str:
    """Interact with Safari app: 'open_url', 'get_active_tab', 'list_open_tabs', or 'run_js_on_active_tab'."""
    act = action.lower().strip().replace("-", "_")
    try:
        if act == "open_url":
            if not url:
                raise ValueError("url is required for open_url")
            script = f'''
            tell application "Safari"
                make new document with properties {{URL:"{url}"}}
                activate
            end tell
            '''
            run_applescript(script)
            return f"Opened URL '{url}' in Safari."

        elif act == "get_active_tab":
            script = '''
            tell application "Safari"
                return (name of current tab of front window) & " - " & (URL of current tab of front window)
            end tell
            '''
            res = run_applescript(script)
            return f"Active Safari Tab: {res}"

        elif act == "list_open_tabs":
            script = '''
            tell application "Safari"
                set tabList to ""
                repeat with w in windows
                    repeat with t in tabs of w
                        set tabList to tabList & (name of t) & " - " & (URL of t) & "\\n"
                    end repeat
                end repeat
                return tabList
            end tell
            '''
            res = run_applescript(script)
            return f"Safari Open Tabs:\n{res}"

        elif act in ("run_js_on_active_tab", "run_js"):
            if not js_script:
                raise ValueError("js_script is required for run_js_on_active_tab")
            script = f'''
            tell application "Safari"
                do JavaScript "{js_script.replace('"', '\\"')}" in document 1
            end tell
            '''
            res = run_applescript(script)
            return f"Executed JS on active tab. Result: {res}"
        else:
            raise ValueError(f"Unknown safari action: {action}")
    except Exception as e:
        return f"Safari action status: {e}"

def notes_tool(
    action: str,
    title: Optional[str] = None,
    body: Optional[str] = None,
    query: Optional[str] = None,
    note_id: Optional[str] = None
) -> str:
    """Interact with Notes.app: 'create', 'search', or 'append'."""
    act = action.lower().strip()
    try:
        if act == "create":
            if not title or not body:
                raise ValueError("title and body are required for create action")
            script = f'''
            tell application "Notes"
                tell folder "Notes"
                    make new note with properties {{name:"{title.replace('"', '\\"')}", body:"{body.replace('"', '\\"')}"}}
                end tell
            end tell
            '''
            run_applescript(script)
            return f"Created Note '{title}'."

        elif act == "search":
            if not query:
                raise ValueError("query is required for search action")
            script = f'''
            tell application "Notes"
                set noteList to name of every note whose name contains "{query.replace('"', '\\"')}" or body contains "{query.replace('"', '\\"')}"
                return noteList
            end tell
            '''
            res = run_applescript(script)
            return f"Notes matching '{query}':\n{res}"

        elif act == "append":
            if not note_id or not body:
                raise ValueError("note_id and body are required for append action")
            script = f'''
            tell application "Notes"
                set myNote to first note whose name is "{note_id.replace('"', '\\"')}"
                set body of myNote to (body of myNote) & "<br>" & "{body.replace('"', '\\"')}"
            end tell
            '''
            run_applescript(script)
            return f"Appended content to note '{note_id}'."
        else:
            raise ValueError(f"Unknown notes action: {action}")
    except Exception as e:
        return f"Notes action status: {e}"

def terminal_tool(
    action: str,
    command: Optional[str] = None,
    text: Optional[str] = None,
    target: str = "terminal"
) -> str:
    """Interact with terminal applications (Terminal.app or iTerm2): 'open_window', 'run_command', 'send_text', 'get_active_text', or 'list_sessions'."""
    act = action.lower().strip()
    app_name = "iTerm" if target.lower() == "iterm2" else "Terminal"
    try:
        if act == "open_window":
            script = f'tell application "{app_name}" to activate'
            run_applescript(script)
            return f"Opened {app_name} window."
        elif act == "run_command":
            cmd = command or text
            if not cmd:
                raise ValueError("command is required for run_command")
            script = f'''
            tell application "{app_name}"
                do script "{cmd.replace('"', '\\"')}"
                activate
            end tell
            '''
            run_applescript(script)
            return f"Sent command to {app_name}."
        elif act == "send_text":
            if not text:
                raise ValueError("text is required for send_text")
            script = f'''
            tell application "{app_name}"
                do script "{text.replace('"', '\\"')}"
                activate
            end tell
            '''
            run_applescript(script)
            return f"Sent text to {app_name}."
        elif act == "get_active_text":
            script = f'''
            tell application "{app_name}"
                return contents of selected tab of front window
            end tell
            '''
            return run_applescript(script)
        elif act == "list_sessions":
            script = f'''
            tell application "{app_name}"
                return name of every window
            end tell
            '''
            return run_applescript(script)
        else:
            raise ValueError(f"Unknown terminal action: {action}")
    except Exception as e:
        return f"Terminal action status: {e}"

def calendar_create(title: str, start_time: str, end_time: Optional[str] = None) -> str:
    """Creates a new event in macOS Calendar app."""
    return calendar_tool("create_event", title=title, start_time=start_time, end_time=end_time)

def contacts_search(query: str) -> str:
    """Searches macOS Contacts app for person matching query."""
    try:
        script = f'''
        tell application "Contacts"
            set matches to name of every person whose name contains "{query.replace('"', '\\"')}"
            return matches
        end tell
        '''
        res = run_applescript(script)
        return f"Contacts matching '{query}':\n{res}"
    except Exception as e:
        return f"Contacts search status: {e}"

def notes_create(title: str, body: str) -> str:
    """Creates a new note in macOS Notes app."""
    return notes_tool("create", title=title, body=body)

def mail_send_draft(to: str, subject: str, body: str) -> str:
    """Creates a new draft message in macOS Mail app."""
    return mail_tool("send_draft", to=to, subject=subject, body=body)

def iphone_mirror_info() -> str:
    """Returns macOS iPhone Mirroring connectivity status."""
    try:
        script = 'tell application "System Events" to get name of every process whose name contains "iPhone Mirroring"'
        res = run_applescript(script)
        active = "iPhone Mirroring" in res
        return f"iPhone Mirroring status: {'Running' if active else 'Not running'}"
    except Exception as e:
        return f"iPhone Mirroring status: {e}"

def analyze_image(path: str) -> str:
    """Analyzes image file and returns dimension & format metadata."""
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Image path '{abs_path}' does not exist.")
    try:
        from PIL import Image
        with Image.open(abs_path) as img:
            info = {
                "path": abs_path,
                "format": img.format,
                "mode": img.mode,
                "width": img.width,
                "height": img.height
            }
            return json.dumps(info, indent=2)
    except Exception as e:
        return f"Analyzed file '{abs_path}' (metadata inspection error: {e})"

def get_knowledge_document(id: str) -> str:
    """Retrieves document from local knowledge catalog by ID."""
    catalog_path = os.path.expanduser(f"~/Desktop/Jarvis/PersonalAssistant/backend/data/knowledge_catalog/{id}.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"Knowledge document '{id}' not found."

def update_knowledge_document(id: str, content: str) -> str:
    """Updates or creates document in local knowledge catalog by ID."""
    catalog_dir = os.path.expanduser("~/Desktop/Jarvis/PersonalAssistant/backend/data/knowledge_catalog")
    os.makedirs(catalog_dir, exist_ok=True)
    catalog_path = os.path.join(catalog_dir, f"{id}.json")
    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Updated knowledge document '{id}'."
