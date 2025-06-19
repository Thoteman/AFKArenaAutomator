from adbauto import *
import time

BACK_BUTTON = (30, 1890)

# All functions related to campaign screen
def claim_afk_rewards(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        tap(device_id,  scrcpy.resolution[0]//2, scrcpy.resolution[1]//2)
        time.sleep(3)
        tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
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
        if tap_img_when_visible(device_id, scrcpy, "res/global/end_autobattle_button.png", timeout=5, random_delay=True):
            success = True
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/back_arrow.png", timeout=5, random_delay=True)
        logger("Battle started successfully!", "success") if success else logger("Battle failed to start.", "error")

def claim_fast_rewards(device_id, scrcpy, logger, amount):
    if find_image(scrcpy.last_frame, "res/campaign/campaign_unselected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/campaign_unselected.png")
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/fast_rewards_red.png"):
            time.sleep(3)
            claim_button = find_image(scrcpy.last_frame, "res/campaign/fast_rewards_free.png")
            for _ in range(amount):
                tap(device_id, claim_button[0], claim_button[1])
                time.sleep(3)
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(3)
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            logger(f"Claimed fast rewards {amount} of time(s)!", "success")
            return
        else:
            logger("Fast rewards already claimed.", "info")

# All functions related to dark forest screen 
# TODO: ADD CLAIM FUNCTIONS TO BOUNTY BOARD
def bounty_board(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/bounty_board.png")
        time.sleep(3)

        # This is only when an event is active
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/event_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/event_bounty_selected.png"):
            time.sleep(3)
            while tap_image(device_id, scrcpy.last_frame, "res/darkforest/event_bounty_dispatch.png"):
                time.sleep(3)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/event_bounty_herochoice.png", timeout=5, random_delay=True, threshold=0.8)
                time.sleep(3)
                tap(device_id, 118, 1482) # This is the upper left hero (what the game advices to send)
                time.sleep(3)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/event_bounty_start.png", timeout=5, random_delay=True)
                time.sleep(3)

        # This is the solo bounty board TODO: Make it possible to send each bounty on their own
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/solo_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/solo_bounty_selected.png"):
            time.sleep(3)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_dispatch.png", timeout=5, random_delay=True):
                time.sleep(3)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_start.png")
                time.sleep(3)

        # This is the team bounty board
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/team_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/team_bounty_selected.png"):
            time.sleep(3)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_dispatch.png", timeout=5, random_delay=True):
                time.sleep(3)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_start.png")
                time.sleep(3)

        tap_img_when_visible(device_id, scrcpy, "res/global/back_arrow.png", timeout=5, random_delay=True)
        logger("Bounty Board tasks completed!", "success")
            
    else:
        logger("Bounty Board start button not found.", "error")

def temporal_rift(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/temporal_rift.png", threshold=0.8)
        time.sleep(3)
        while not find_image(scrcpy.last_frame, "res/darkforest/temporal_fountain.png", threshold=0.8):
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/temporal_fountain.png", timeout=5, random_delay=True)
        time.sleep(3)
        while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(3)
        logger("Temporal Rift tasks completed!", "success")

def kings_tower(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower.png", threshold=0.8)
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower_main.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower_battle.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap_img_when_visible(device_id, scrcpy, "res/global/confirm_begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(3)
        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
        time.sleep(3)
        if tap_img_when_visible(device_id, scrcpy, "res/global/end_autobattle_button.png", timeout=5, random_delay=True):
            success = True
        else:
            success = False
        time.sleep(3)
        while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(3)
        logger("King's tower started successfully!", "success") if success else logger("King's tower failed to start.", "error")

    

def arcane_labyrinth(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arcane_labyrinth.png", threshold=0.8)
        time.sleep(3)
        #TODO: Implement Arcane Labyrinth tasks

# All functions related to Arena of Heroes screen
def treasure_scramble(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena.png", threshold=0.8)
        time.sleep(3)
        # TODO: change numbers when new seasons start and I get screenshots
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/treasure_scramble_1.png", timeout=5, random_delay=True) or \
          tap_image(device_id, scrcpy.last_frame, "res/darkforest/treasure_scramble_1.png", timeout=5, random_delay=True) or \
          tap_image(device_id, scrcpy.last_frame, "res/darkforest/treasure_scramble_1.png", timeout=5, random_delay=True) or \
          tap_image(device_id, scrcpy.last_frame, "res/darkforest/treasure_scramble_1.png", timeout=5, random_delay=True):
            time.sleep(3)
            
# TODO
def arena_of_heroes(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena.png", threshold=0.8)
        time.sleep(3)


def legends_challenger(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena.png", threshold=0.8)
        time.sleep(3)
        scroll(device_id, "up", 500, 500, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
        if tap_img_when_visible(device_id, scrcpy, "res/darkforest/legends_challenger.png", threshold=0.8):
            time.sleep(3)

# TODO
def legends_championship(device_id, scrcpy, logger):
    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/darkforest_unselected.png", threshold=0.8)
        time.sleep(3)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena.png", threshold=0.8)
        time.sleep(3)

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