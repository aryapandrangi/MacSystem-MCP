from .applescript import run_applescript

def media_control(action: str) -> str:
    """Controls media playback ('play', 'pause', 'playpause', 'next', 'previous')."""
    act = action.lower().strip()
    key_codes = {
        "play": 16,
        "pause": 16,
        "playpause": 16,
        "next": 19,
        "previous": 20,
        "prev": 20
    }
    if act in key_codes:
        script = f'''
        try:
            tell application "Music"
                if "{act}" = "playpause" or "{act}" = "play" or "{act}" = "pause" then playpause
                if "{act}" = "next" then next track
                if "{act}" = "previous" or "{act}" = "prev" then previous track
            end tell
        on error
            try
                tell application "Spotify"
                    if "{act}" = "playpause" or "{act}" = "play" or "{act}" = "pause" then playpause
                    if "{act}" = "next" then next track
                    if "{act}" = "previous" or "{act}" = "prev" then previous track
                end tell
            end try
        end try
        '''
        try:
            run_applescript(script)
            return f"Media control executed: '{action}'"
        except Exception as e:
            return f"Media control '{action}' status: {e}"
    else:
        raise ValueError(f"Unknown media action: {action}. Supported: play, pause, playpause, next, previous")
