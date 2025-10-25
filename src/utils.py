import configparser
import time
import sys, os, shutil
import numpy as np
from adbauto import *
from src.strings import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_config_path():
    # We'll store the real config in the same directory as the .exe
    exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    if exe_dir.endswith("src"):
        exe_dir = exe_dir[:-4]  # Remove 'src' from the path
    target_path = os.path.join(exe_dir, "config.ini")

    # If it doesn't exist yet, copy from the bundled resource
    if not os.path.exists(target_path):
        shutil.copy(resource_path("config.ini"), target_path)

    return target_path


def check_afk_running(device_id, logger):
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
    try:
        current_activity = shell(device_id, "dumpsys window windows | grep -E 'mCurrentFocus'")
        if "com.lilithgames.hgame.gp.id" in current_activity:
            return "Test Server"
        elif "com.lilithgame.hgame.gp" in current_activity:
            return "Official Server"
        return None
    except Exception as e:
        logger(f"Error checking AFK Arena running state: {e}", "error")
        return "Error"

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

def go_to_startscreen(device_id, scrcpy, logger, task, delay=3):
    """
    Navigate to the start screen for this specific task.
    
    Args:
        device_id: The ID of the ADB device.
    """
    try:
        config = configparser.ConfigParser()
        config.read(get_config_path())
        test_server = bool(config['Global']['Test Server'])
        running = check_afk_running(device_id, logger)

        if not running and not test_server:
            print("AFK Arena is not running. Starting the app...")
            start_afk(device_id)
            time.sleep(delay * 3)

        if not running and test_server:
            print("AFK Arena Test Server is not running. Starting the app...")
            start_afk_test(device_id)
            time.sleep(delay * 3)

        if find_image(scrcpy.last_frame, resource_path("res/global/hero_trial_button.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/global/hero_trial_button.png"))
            time.sleep(delay)

        match task:
            case "campaign":
                while not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")) and not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_unselected.png")):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                            
                if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_unselected.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/campaign/campaign_unselected.png"))
                    time.sleep(delay)
                
                return
            
            case "rightbanner":
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, resource_path("res/banner/closed_right_banner_red.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/banner/closed_right_banner_red.png"))
                    time.sleep(delay)

                elif find_image(scrcpy.last_frame, resource_path("res/banner/closed_right_banner.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/banner/closed_right_banner.png"))
                    time.sleep(delay)

                return
            
            case "darkforest":
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                    time.sleep(delay)
                
                return
            
            case "arena":
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                    return
                
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                    time.sleep(delay)

                tap(device_id, arena_on_map[0], arena_on_map[1])
                time.sleep(delay)

                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                return
            
            case "citydown":
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)

                tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                time.sleep(delay)
                tap(device_id, back_button[0], back_button[1])
                time.sleep(delay)
                
                for _ in range(2):
                    scroll(device_id, "up", 1200, 600)
                    time.sleep(delay)
                
                return
            
            case "cityup":
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)

                tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                time.sleep(delay)
                tap(device_id, back_button[0], back_button[1])
                time.sleep(delay)
                
                scroll(device_id, "down", 1200, 600)
                time.sleep(delay)
                
                return
            
            case "guild":
                if find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                    return
                
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)

                tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                time.sleep(delay)
                tap(device_id, back_button[0], back_button[1])
                time.sleep(delay)
                
                scroll(device_id, "down", 1200, 600)
                time.sleep(delay)
                tap(device_id, guild_on_map[0], guild_on_map[1])

                while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                    tap(device_id, guild_chest[0], guild_chest[1])
                    time.sleep(delay)
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)
                return
            
            case "unlimited":
                if find_image(scrcpy.last_frame, resource_path("res/unlimited/text.png")):
                    tap(device_id, 730, 1650)
                    time.sleep(delay)
                    tap(device_id, 850, 1830)
                    time.sleep(delay)
                    return
                
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8) and not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(delay)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
                    time.sleep(delay)

                if not find_image(scrcpy.last_frame, resource_path("res/unlimited/icon.png")):
                    tap(device_id, 100, 400)
                    time.sleep(delay)

                if find_image(scrcpy.last_frame, resource_path("res/unlimited/icon.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/unlimited/icon.png"), threshold=0.8)
                    time.sleep(delay)
                    tap(device_id, 730, 1650)
                    time.sleep(delay)
                    tap(device_id, 850, 1830)
                    time.sleep(delay)
                    return

    except Exception as e:
        print(e)
        raise


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

def remove_duplicate_centers(centers, threshold=10):
    """
    Removes centers that are within threshold px in both X and Y from another center.
    Uses NumPy for speed.
    """
    centers = np.array(centers, dtype=np.int32)
    deduped = []

    for center in centers:
        if len(deduped) == 0:
            deduped.append(center)
            continue

        kept = np.array(deduped)
        diffs = np.abs(kept - center)
        if not np.any(np.all(diffs <= threshold, axis=1)):
            deduped.append(center)

    return np.array(deduped, dtype=np.int32)

def choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, delay=3):
    """
    Choose a formation to copy based on the formation number.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        delay (int): Delay in seconds for waiting between actions. Default is 3.
    """
    try:
        tap(device_id, formations_button[0], formations_button[1])
        time.sleep(delay)
        ## This screen takes longer to load, so a little delay added
        for _ in range(3):
            if not find_image(scrcpy.last_frame, resource_path("res/autopush/formations_text.png")):
                time.sleep(delay)

        formations = find_all_images(scrcpy.last_frame, resource_path("res/autopush/formations_select.png"))
        formations = filter_near_duplicates(formations)
        if len(formations) == 0:
            logger("No formations available, using current formation.", "warning")
            formation_using = 0
            tap(device_id, back_button[0], back_button[1])
            time.sleep(delay)
        elif formation_no > len(formations):
            logger(f"Formation {formation_no} not available, using last formation instead.", "warning")
            formation_using = len(formations)
        else:
            formation_using = formation_no

        if formation_using > 0:
            tap(device_id, formations[formation_using - 1][0], formations[formation_using - 1][1])
            time.sleep(delay)
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_statistics_text.png")):
                    tap(device_id, formations_use_button[0], formations_use_button[1])
                    set_artifacts(device_id, scrcpy, artifacts, delay)
                    time.sleep(delay)
                    tap(device_id, artifacts_confirm_button[0], artifacts_confirm_button[1])
                    time.sleep(delay)
                    return
                time.sleep(delay)   
    except Exception as e:
        print(e)
        raise

def set_artifacts(device_id, scrcpy, artifacts, delay = 3):
    """
    Set artifacts based on the artifacts boolean.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        artifacts (bool): Whether to copy artifacts. Default is True.
        delay (int): Delay in seconds for waiting between actions. Default is 3.
    """
    try:
        ## Wait for the artifacts screen to load
        for _ in range(3):
            if find_image(scrcpy.last_frame, resource_path("res/autopush/artifacts_text.png")):
                break
            time.sleep(delay)

        if find_image(scrcpy.last_frame, resource_path("res/autopush/artifacts_1_0.png")) or find_image(scrcpy.last_frame, resource_path("res/autopush/artifacts_1_1.png")):
            tap(device_id, artifacts_checkmark_1[0], artifacts_checkmark_1[1])
            time.sleep(delay)

        if artifacts:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/artifacts_0_1.png")):
                return
            else:
                tap(device_id, artifacts_checkmark_2[0], artifacts_checkmark_2[1])
                time.sleep(delay)
                return
        else:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/artifacts_0_0.png")):
                return
            else:
                tap(device_id, artifacts_checkmark_2[0], artifacts_checkmark_2[1])
                time.sleep(delay)
                return
    except Exception as e:
        print(e)
        raise