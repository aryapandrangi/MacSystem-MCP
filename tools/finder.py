import os
import subprocess
from typing import List
from .applescript import run_applescript

PROTECTED_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Movies"),
    os.path.expanduser("~/Library"),
    os.path.expanduser("~")
]

def _is_protected_path(abs_path: str) -> bool:
    """Checks if path matches or is a parent of a protected user directory."""
    for protected in PROTECTED_DIRS:
        if abs_path == protected or abs_path == os.path.dirname(protected):
            return True
    return False

def reveal_in_finder(path: str) -> str:
    """Reveals file or directory path in macOS Finder."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abs_path):
            return f"Path '{abs_path}' does not exist to reveal in Finder."
        subprocess.run(["open", "-R", abs_path], check=True)
        return f"Revealed '{abs_path}' in Finder."
    except Exception as e:
        return f"Failed to reveal in Finder: {e}"

def get_finder_selection() -> str:
    """Returns file paths currently selected in frontmost Finder window."""
    try:
        script = '''
        tell application "Finder"
            set sel to selection
            set outputText to ""
            repeat with item_ in sel
                set outputText to outputText & (POSIX path of (item_ as alias)) & "\\n"
            end repeat
            return outputText
        end tell
        '''
        res = run_applescript(script)
        return res.strip() if res else "No files selected in Finder."
    except Exception as e:
        return f"Finder selection status: {e}"

def set_finder_tags(path: str, tags: List[str]) -> str:
    """Sets Finder color tags on file path. STRICT GUARDRAIL: Tagging allowed ONLY inside /tmp/."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        
        # GUARDRAIL: Strictly restrict tag modification to /tmp/ paths
        if not (abs_path.startswith("/tmp/") or abs_path.startswith("/private/tmp/")):
            return f"Guardrail Blocked: Modifying Finder tags on '{abs_path}' is strictly forbidden. Tags can only be modified on temporary test files inside /tmp/."

        if not os.path.exists(abs_path):
            return f"Path '{abs_path}' does not exist to set Finder tags."
        
        tags_str = ",".join(tags)
        subprocess.run(["tag", "--set", tags_str, abs_path], check=True)
        return f"Set tags {tags} on '{abs_path}'"
    except Exception as e:
        return f"Set Finder tags status: {e}"

def quick_look(path: str) -> str:
    """Opens QuickLook preview panel for file path."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abs_path):
            return f"Path '{abs_path}' does not exist for QuickLook."
        subprocess.Popen(["qlmanage", "-p", abs_path])
        return f"Opened QuickLook for '{abs_path}'"
    except Exception as e:
        return f"QuickLook status: {e}"

def move_to_trash(path: str) -> str:
    """Moves file or directory to Trash. STRICT GUARDRAIL: Protected user folders cannot be trashed."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))

        # GUARDRAIL: Prevent trashing user root or system directories
        if _is_protected_path(abs_path):
            return f"Guardrail Blocked: Cannot move protected directory '{abs_path}' to Trash."

        if not os.path.exists(abs_path):
            return f"Path '{abs_path}' does not exist to move to Trash."
        script = f'''
        tell application "Finder"
            delete POSIX file "{abs_path}"
        end tell
        '''
        run_applescript(script)
        return f"Moved '{abs_path}' to Trash."
    except Exception as e:
        return f"Move to trash status: {e}"

def spotlight_search(query: str) -> str:
    """Searches local filesystem via macOS mdfind Spotlight CLI."""
    try:
        res = subprocess.run(["mdfind", query], capture_output=True, text=True, check=True)
        files = res.stdout.strip().split("\n")[:20]
        return "\n".join(files) if files else f"No Spotlight results for '{query}'."
    except Exception as e:
        return f"Spotlight search status: {e}"

def empty_trash() -> str:
    """Empties macOS Trash."""
    try:
        script = 'tell application "Finder" to empty trash'
        run_applescript(script)
        return "Trash emptied."
    except Exception as e:
        return f"Empty trash status: {e}"
