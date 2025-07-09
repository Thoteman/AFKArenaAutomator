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
    try:
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

        if find_image(scrcpy.last_frame, "res/global/hero_trial_button.png"):
            tap_image(device_id, scrcpy.last_frame, "res/global/hero_trial_button.png")
            time.sleep(delay)

        match task:
            case "campaign":
                while not find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png") and not find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                            
                if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
                    tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
                    time.sleep(delay)
                
                return
            
            case "rightbanner":
                while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8) and not find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
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
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
                    time.sleep(delay)
                
                return
            
            case "arena":
                if find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                    return
                
                while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8) and not find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
                    time.sleep(delay)

                if find_image(scrcpy.last_frame, "res/darkforest/arena.png"):
                    tap_image(device_id, scrcpy.last_frame, "res/darkforest/arena.png")
                    time.sleep(delay)

                while not find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                return
            
            case "citydown":
                while not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
                    print(scrcpy.last_frame)
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                scroll(device_id, "up", 1200, 600)
                time.sleep(delay)
                
                return
            
            case "cityup":
                while not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                scroll(device_id, "down", 1200, 600)
                time.sleep(1)
                scroll(device_id, "down", 1200, 600)
                time.sleep(delay)
                
                return
            
            case "guild":
                if find_image(scrcpy.last_frame, "res/city/guild_text.png"):
                    return
                
                while not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(delay)
                
                scroll(device_id, "down", 1200, 600)
                time.sleep(1)
                scroll(device_id, "down", 1200, 600)
                time.sleep(delay)

                if find_image(scrcpy.last_frame, "res/city/guild.png", threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, "res/city/guild.png", threshold=0.8)
                    time.sleep(delay)

                    while not find_image(scrcpy.last_frame, "res/city/guild_text.png"):
                        tap(device_id, scrcpy.resolution[0]//2, 2*scrcpy.resolution[1]//3)
                        time.sleep(delay)
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(delay)
                
                return
    except AttributeError:
        raise AttributeError


def is_color_match(actual, expected, tolerance=5):
    return all(abs(int(a) - int(e)) <= tolerance for a, e in zip(actual, expected))

def filter_near_duplicates(points, y_threshold=5):
    """
    Filters out points that are within `y_threshold` pixels in Y.
    Assumes points are sorted or can be grouped by Y proximity.
    """
    if not points:
        return []

    # Sort points by Y value
    points = sorted(points, key=lambda p: p[1])
    filtered = [points[0]]

    for x, y in points[1:]:
        _, last_y = filtered[-1]
        if abs(y - last_y) > y_threshold:
            filtered.append((x, y))

    return filtered

def set_artifacts(device_id, scrcpy, artifacts, delay = 3):
    """
    Sets the artifacts for the hero in the artifact selection screen.
    
    Args:
        device_id: The ID of the ADB device.
        scrcpy: The Scrcpy instance for capturing frames.
        artifacts: A list of artifact names to set.
    """
    try:
        if find_image(scrcpy.last_frame, "res/autopush/artifacts_allselected.png"):
            tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_allselected.png")
            time.sleep(delay)

        if artifacts:
            if find_image(scrcpy.last_frame, "res/autopush/artifacts_inverted.png"):
                tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_inverted.png")
                time.sleep(delay)
                tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_unselected.png")
                time.sleep(delay)
            elif find_image(scrcpy.last_frame, "res/autopush/artifacts_unselected.png"):
                tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_unselected.png")
                time.sleep(delay)

            if not find_image(scrcpy.last_frame, "res/autopush/artifacts_selected.png"):
                return
        else:
            if find_image(scrcpy.last_frame, "res/autopush/artifacts_inverted.png"):
                tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_inverted.png")
                time.sleep(delay)
            elif find_image(scrcpy.last_frame, "res/autopush/artifacts_selected.png"):
                tap_image(device_id, scrcpy.last_frame, "res/autopush/artifacts_selected.png")
                time.sleep(delay)

            if not find_image(scrcpy.last_frame, "res/autopush/artifacts_unselected.png"):
                return
            
        tap_img_when_visible(device_id, scrcpy, "res/autopush/artifacts_confirm.png", delay=delay)
        time.sleep(delay)
    except Exception:
        raise Exception