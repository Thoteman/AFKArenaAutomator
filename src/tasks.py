from adbauto import *
import time

# All functions related to campaign screen
def claim_afk_rewards(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        tap(device_id, 540, 1500)
        time.sleep(3)
        tap(device_id, 540, 1500)
        if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
            logger("Claimed AFK rewards!", "success")

    else:
        logger("Campaign screen not detected.", "error")
        return

def campaign_battle(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/begin_battle_button.png")
        time.sleep(3)
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/begin_battle_button_multistage.png", timeout=5, random_delay=True):
            time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/confirm_begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
        time.sleep(3)
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/end_autobattle_button.png", timeout=5, random_delay=True):
            success = True
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/back_arrow.png", timeout=5, random_delay=True)
        logger("Battle started successfully!", "success") if success else logger("Battle failed to start.", "error")

def claim_fast_rewards(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        if find_image(scrcpy.last_frame, "res/campaign/fast_rewards.png"):
            logger("Fast rewards already claimed.", "info")
            return
        else:

            tap_image(device_id, scrcpy.last_frame, "res/campaign/fast_rewards_red.png")
            time.sleep(3)
            logger("Claimed fast rewards!", "success")

