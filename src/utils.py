import configparser
import time
from adbauto import *

CONFIG_PATH = "config.ini"
BACK_BUTTON = (30, 1890)

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

def go_to_startscreen(device_id, scrcpy, task, delay=3):
    """
    Navigate to the start screen for this specific task.
    
    Args:
        device_id: The ID of the ADB device.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    test_server = bool(config['Global']['Test Server'])
    running = check_afk_running(device_id)

    if not running and not test_server:
        print("AFK Arena is not running. Starting the app...")
        start_afk(device_id)
        time.sleep(delay * 3)

    if not running and test_server:
        print("AFK Arena Test Server is not running. Starting the app...")
        start_afk_test(device_id)
        time.sleep(delay * 3)

    match task:
        case "campaign":
            while not find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png") and not find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(delay)
                        
            if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
                tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
                time.sleep(delay)
            
            return
        
        case "rightbanner":
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8) and not find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(delay)
            
            if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
                time.sleep(delay)
            
            if find_image(scrcpy.last_frame, "res/banner/closed_right_banner_red.png"):
                tap_image(device_id, scrcpy.last_frame, "res/banner/closed_right_banner_red.png")
                time.sleep(delay)

            elif find_image(scrcpy.last_frame, "res/banner/closed_right_banner.png"):
                tap_image(device_id, scrcpy.last_frame, "res/banner/closed_right_banner.png")
                time.sleep(delay)

            return
        
        case "darkforest":
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8) and not find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(delay)
            
            if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
                time.sleep(delay)
            
            return
        
        case "arena":
            if find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                return
            
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8) and not find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(delay)
            
            if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
                time.sleep(delay)

            if find_image(scrcpy.last_frame, "res/darkforest/arena.png"):
                tap_image(device_id, scrcpy.last_frame, "res/darkforest/arena.png")
                time.sleep(delay)

            while not find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(delay)
            
            return
        
        case "city":
            pass
