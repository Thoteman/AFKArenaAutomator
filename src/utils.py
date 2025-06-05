from adbauto import *

def check_afk_running(device_id):
    """
    Get the current activity of the device.
    
    Args:
        device: The ADB device instance.
        
    Returns:
        str: The current activity of the device.
    """
    # Use dumpsys to get the current focus activity
    # This command may vary based on the Android version and device
    # Ensure that 'grep' is available in the shell environment
    current_activity = shell(device_id, "dumpsys window windows | grep -E 'mCurrentFocus'")
    print(f"Current activity: {current_activity}")
    if "com.lilithgames.hgame.gp.id" in current_activity:
        return "Test Server"
    elif "com.lilithgame.hgame.gp" in current_activity:
        return "Official Server"
    return None

def start_afk(device_id):
    """
    Start the AFK Arena app on the device.
    
    Args:
        device_id: The ID of the ADB device.
    """
    # Use the shell command to start the app
    shell(device_id, "am start -n com.lilithgame.hgame.gp/sh.lilithgame.hgame.AppActivity")

def start_afk_test(device_id):
    """
    Start the AFK Arena test server app on the device.
    
    Args:
        device_id: The ID of the ADB device.
    """
    # Use the shell command to start the test server app
    shell(device_id, "am start -n com.lilithgames.hgame.gp.id/sh.lilithgame.hgame.AppActivity")