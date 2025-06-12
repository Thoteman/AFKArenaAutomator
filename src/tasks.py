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

## TODO: fix
def claim_fast_rewards(device_id, scrcpy, logger, amount):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/fast_rewards_red.png"):
            logger("Claimed fast rewards!", "success")
            return
        else:
            logger("Fast rewards already claimed.", "info")

# All functions related to dark forest screen
def bounty_board(device_id, scrcpy, logger):
    pass

def temporal_rift(device_id, scrcpy, logger):
    pass

def kings_tower(device_id, scrcpy, logger):
    pass

def arcane_labyrinth(device_id, scrcpy, logger):
    pass

# All functions related to Arena of Heroes screen
def treasure_vanguard(device_id, scrcpy, logger):
    pass

def treasure_scramble(device_id, scrcpy, logger):
    pass

def arena_of_heroes(device_id, scrcpy, logger):
    pass

def legends_challenger(device_id, scrcpy, logger):
    pass

def legends_championship(device_id, scrcpy, logger):
    pass

# All functions related to Ranhorn screen
def store(device_id, scrcpy, logger):
    pass

def beast_grounds(device_id, scrcpy, logger):
    pass

def noble_tavern(device_id, scrcpy, logger):
    pass

def resonating_crystal(device_id, scrcpy, logger):
    pass

def temple_of_ascension(device_id, scrcpy, logger):
    pass

def oak_inn(device_id, scrcpy, logger):
    pass

def dragon_isle(device_id, scrcpy, logger):
    pass

# All functions related to Guild screen
def guild_hunt(device_id, scrcpy, logger):
    pass

def twisted_realm(device_id, scrcpy, logger):
    pass

# All functions related to banners
def solemn_vow(device_id, scrcpy, logger):
    pass

def friends(device_id, scrcpy, logger):
    pass

def mail(device_id, scrcpy, logger):
    pass

def bag(device_id, scrcpy, logger):
    pass

def quests(device_id, scrcpy, logger):
    pass

def merchants(device_id, scrcpy, logger):
    pass

def events(device_id, scrcpy, logger):
    pass