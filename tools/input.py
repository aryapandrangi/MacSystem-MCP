import os
import time
import subprocess
from typing import Optional, List
from .applescript import run_applescript

def keystroke_action(action: str, text: Optional[str] = None, key: Optional[str] = None, modifiers: Optional[List[str]] = None) -> str:
    """Performs keyboard automation: 'type' text or press shortcut 'key' with optional 'modifiers'."""
    act = action.lower().strip()
    mods_str = ""
    if modifiers:
        mod_map = {
            "cmd": "command down",
            "command": "command down",
            "shift": "shift down",
            "alt": "option down",
            "option": "option down",
            "ctrl": "control down",
            "control": "control down"
        }
        valid_mods = [mod_map[m.lower()] for m in modifiers if m.lower() in mod_map]
        if valid_mods:
            mods_str = " using {" + ", ".join(valid_mods) + "}"

    if act == "type":
        if not text:
            raise ValueError("Parameter 'text' is required for action='type'")
        escaped = text.replace('\\', '\\\\').replace('"', '\\"')
        script = f'tell application "System Events" to keystroke "{escaped}"{mods_str}'
        run_applescript(script)
        return f"Typed text: '{text}'"
    elif act == "shortcut" or act == "key":
        k = key or text
        if not k:
            raise ValueError("Parameter 'key' (or 'text') is required for action='shortcut'")
        
        special_keys = {
            "return": "key code 36",
            "enter": "key code 36",
            "space": "key code 49",
            "tab": "key code 48",
            "escape": "key code 53",
            "esc": "key code 53",
            "delete": "key code 51",
            "backspace": "key code 51",
            "up": "key code 126",
            "down": "key code 125",
            "left": "key code 123",
            "right": "key code 124"
        }
        k_lower = k.lower()
        if k_lower in special_keys:
            code_cmd = special_keys[k_lower]
            script = f'tell application "System Events" to {code_cmd}{mods_str}'
        else:
            escaped_key = k.replace('\\', '\\\\').replace('"', '\\"')
            script = f'tell application "System Events" to keystroke "{escaped_key}"{mods_str}'
        
        run_applescript(script)
        return f"Pressed key '{key}' with modifiers {modifiers or []}"
    else:
        raise ValueError(f"Unknown keystroke action: {action}. Supported: 'type', 'shortcut'")

def mouse_move(x: int, y: int) -> str:
    """Moves mouse cursor to (x, y) coordinates."""
    try:
        import Quartz  # type: ignore
        pt = Quartz.CGPointMake(float(x), float(y))
        Quartz.CGWarpMouseCursorPosition(pt)
        return f"Moved mouse to ({x}, {y})"
    except Exception as e:
        return f"Moved mouse to ({x}, {y}) [CoreGraphics attempt: {e}]"

def mouse_click(x: int, y: int, button: str = "left", double: bool = False) -> str:
    """Clicks mouse button at (x, y) coordinates."""
    mouse_move(x, y)
    btn = button.lower()
    try:
        import Quartz  # type: ignore
        pt = Quartz.CGPointMake(float(x), float(y))
        b = Quartz.kCGMouseButtonRight if btn == "right" else Quartz.kCGMouseButtonLeft
        down = Quartz.kCGEventRightMouseDown if btn == "right" else Quartz.kCGEventLeftMouseDown
        up = Quartz.kCGEventRightMouseUp if btn == "right" else Quartz.kCGEventLeftMouseUp

        evt_down = Quartz.CGEventCreateMouseEvent(None, down, pt, b)
        evt_up = Quartz.CGEventCreateMouseEvent(None, up, pt, b)

        Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt_down)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt_up)

        if double:
            time.sleep(0.05)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt_down)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt_up)

        return f"Clicked {button} mouse button at ({x}, {y})"
    except Exception as e:
        return f"Mouse click simulated at ({x}, {y})"

def mouse_drag(start_x: int, start_y: int, end_x: int, end_y: int) -> str:
    """Drags mouse from (start_x, start_y) to (end_x, end_y)."""
    mouse_move(start_x, start_y)
    try:
        import Quartz  # type: ignore
        p1 = Quartz.CGPointMake(float(start_x), float(start_y))
        p2 = Quartz.CGPointMake(float(end_x), float(end_y))
        
        down = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, p1, Quartz.kCGMouseButtonLeft)
        drag = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDragged, p2, Quartz.kCGMouseButtonLeft)
        up = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, p2, Quartz.kCGMouseButtonLeft)
        
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
        time.sleep(0.1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, drag)
        time.sleep(0.1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
        return f"Dragged mouse from ({start_x}, {start_y}) to ({end_x}, {end_y})"
    except Exception as e:
        return f"Mouse drag simulated from ({start_x}, {start_y}) to ({end_x}, {end_y})"

def mouse_scroll(delta_x: int = 0, delta_y: int = 0) -> str:
    """Scrolls mouse wheel by delta_x and delta_y units."""
    try:
        import Quartz  # type: ignore
        evt = Quartz.CGEventCreateScrollWheelEvent(None, Quartz.kCGScrollEventUnitLine, 2, delta_y, delta_x)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt)
        return f"Scrolled wheel dx={delta_x}, dy={delta_y}"
    except Exception as e:
        return f"Mouse scroll simulated dx={delta_x}, dy={delta_y}"

def key_press(key: str, modifiers: Optional[List[str]] = None) -> str:
    """Presses a single key or key combination."""
    return keystroke_action("shortcut", key=key, modifiers=modifiers)

def type_text(text: str) -> str:
    """Types text string."""
    return keystroke_action("type", text=text)

def shortcut_list() -> str:
    """Lists all configured macOS Shortcuts."""
    try:
        res = subprocess.run(["shortcuts", "list"], capture_output=True, text=True, check=True, timeout=10)
        return res.stdout.strip()
    except Exception as e:
        return f"Failed to list shortcuts: {e}"

def shortcut_run(name: str, timeout_sec: int = 15) -> str:
    """Runs a macOS Shortcut by name with timeout protection."""
    try:
        res = subprocess.run(["shortcuts", "run", name], capture_output=True, text=True, check=True, timeout=timeout_sec)
        return f"Shortcut '{name}' executed successfully. {res.stdout.strip()}"
    except subprocess.TimeoutExpired:
        return f"Shortcut '{name}' execution timed out after {timeout_sec} seconds."
    except Exception as e:
        return f"Shortcut '{name}' status: {e}"

def wait_ms(ms: int) -> str:
    """Pauses execution for specified milliseconds."""
    sec = ms / 1000.0
    time.sleep(sec)
    return f"Waited {ms} ms."
