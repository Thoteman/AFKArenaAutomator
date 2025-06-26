from adbauto import *
from src.utils import go_to_startscreen
import time

BACK_BUTTON = (30, 1890)
DELAY = 3

def set_delay(delay):
    global DELAY
    DELAY = delay

# All functions related to campaign screen
def claim_afk_rewards(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        tap(device_id,  scrcpy.resolution[0]//2, scrcpy.resolution[1]//5*4) # Hard coded to click chest, as depending on how long you have been afk it uses a different image
        time.sleep(DELAY)
        while not find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png") and not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
            tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(DELAY)
        return True
    return False

def campaign_battle(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        tap_image(device_id, scrcpy.last_frame, "res/campaign/begin_battle_button.png")
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/begin_battle_button_multistage.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/global/begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/global/confirm_begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/global/end_autobattle_button.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png") and not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False
        

def claim_fast_rewards(device_id, scrcpy, amount, logger):
    go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

    if find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png"):
        if tap_img_when_visible(device_id, scrcpy, "res/campaign/fast_rewards.png") or tap_img_when_visible(device_id, scrcpy, "res/campaign/fast_rewards_red.png"):
            time.sleep(DELAY)
            claim_button = find_image(scrcpy.last_frame, "res/campaign/fast_rewards_free.png")
            if not claim_button:
                logger("Fast rewards already claimed! Skipping this task.", "warning")
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                return False
            for _ in range(amount):
                tap(device_id, claim_button[0], claim_button[1])
                time.sleep(DELAY)
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/campaign/campaign_selected.png") and not find_image(scrcpy.last_frame, "res/city/city_selected.png"):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False
            
def friendship_points(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

    if find_image(scrcpy.last_frame, "res/banner/friends.png"):
        tap_image(device_id, scrcpy.last_frame, "res/banner/friends.png")
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/banner/friend_points.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png"):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False

def loan_mercenaries(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

    if find_image(scrcpy.last_frame, "res/banner/friends.png"):
        tap_image(device_id, scrcpy.last_frame, "res/banner/friends.png")
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/banner/mercenaries.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/banner/mercenaries_manage.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, "res/banner/mercenaries_apply.png", timeout=5, random_delay=True):
                    time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, "res/banner/mercenaries_lend.png", timeout=5, random_delay=True):
                    time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
    return False

# TODO: Add mails that aren't automatically claimed
def read_mail(device_id, scrcpy, delete=False):
    go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

    if find_image(scrcpy.last_frame, "res/banner/mail.png"):
        tap_image(device_id, scrcpy.last_frame, "res/banner/mail.png")
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/banner/mail_read.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            if delete:
                if tap_img_when_visible(device_id, scrcpy, "res/banner/mail_delete.png", timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, "res/banner/mail_delete_confirm.png", timeout=5, random_delay=True)
                    time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png"):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False

# All functions related to dark forest screen 
def bounty_board(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_image(device_id, scrcpy.last_frame, "res/darkforest/bounty_board.png")
        time.sleep(DELAY)

        # This is only when an event is active
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/event_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/event_bounty_selected.png"):
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/event_bounty_claim.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
            while tap_image(device_id, scrcpy.last_frame, "res/darkforest/event_bounty_dispatch.png"):
                time.sleep(DELAY)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/event_bounty_herochoice.png", timeout=5, random_delay=True, threshold=0.8)
                time.sleep(DELAY)
                tap(device_id, 118, 1482) # This is the upper left hero (what the game advices to send)
                time.sleep(DELAY)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/event_bounty_start.png", timeout=5, random_delay=True)
                time.sleep(DELAY)

        # This is the solo bounty board TODO: Make it possible to send each bounty on their own
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/solo_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/solo_bounty_selected.png"):
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_claim.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_dispatch.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_start.png")
                time.sleep(DELAY)

        # This is the team bounty board
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/team_bounty_unselected.png") or find_image(scrcpy.last_frame, "res/darkforest/team_bounty_selected.png"):
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_claim.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_dispatch.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
                tap_img_when_visible(device_id, scrcpy, "res/darkforest/solo_bounty_start.png")
                time.sleep(DELAY)

        tap_img_when_visible(device_id, scrcpy, "res/global/back_arrow.png", timeout=5, random_delay=True)
        return True
    return False

# All functions related to Arena of Heroes screen
def treasure_scramble(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "arena", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/treasure_scramble.png", random_delay=True, threshold=0.8):
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False
            
def arena_of_heroes(device_id, scrcpy, amount, logger):
    go_to_startscreen(device_id, scrcpy, "arena", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
        if tap_image(device_id, scrcpy.last_frame, "res/darkforest/arena_of_heroes.png"):
            time.sleep(DELAY)
            if not find_image(scrcpy.last_frame, "res/darkforest/arena_of_heroes_text.png"):
                return False
            # Clear exclamation mark
            if tap_image(device_id, scrcpy.last_frame, "res/darkforest/arena_of_heroes_record.png"):
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, "res/darkforest/arena_of_heroes_text.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
            # Start battles
            if tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena_of_heroes_challenge.png", timeout=5, random_delay=True):
                time.sleep(DELAY)
                for battle in range(amount):
                    win = False
                    if not find_image(scrcpy.last_frame, "res/darkforest/arena_of_heroes_text2.png"):
                        return False, battle
                    possible_enemies = find_all_images(scrcpy.last_frame, "res/darkforest/arena_of_heroes_button.png")
                    weakest_enemy = sorted(possible_enemies, key=lambda pt: pt[1], reverse=True)[0]
                    tap(device_id, weakest_enemy[0], weakest_enemy[1])
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena_of_heroes_battle.png", timeout=5, random_delay=True)
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, "res/darkforest/arena_of_heroes_skip.png", timeout=5, random_delay=True):
                        time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, "res/darkforest/arena_of_heroes_text2.png"):
                        if find_image(scrcpy.last_frame, "res/darkforest/arena_of_heroes_reward.png"):
                            win = True
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)
                    logger(f"Arena of Heroes battle {battle + 1} {'won' if win else 'lost'}", "success" if win else "error")
                while not find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)

                return True, battle + 1
    return False, 0

def gladiator_coins(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "arena", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
        while not tap_image(device_id, scrcpy.last_frame, "res/darkforest/legend_challenger.png"):
            scroll(device_id, "down", 300, scrcpy.resolution[0]//2, scrcpy.resolution[1]//2)
            time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/darkforest/legend_challenger_chest1.png", timeout=5, random_delay=True) or tap_img_when_visible(device_id, scrcpy, "res/darkforest/legend_challenger_chest2.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/darkforest/arena_text.png"):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False

def temporal_rift(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/temporal_rift.png", threshold=0.8)
        time.sleep(DELAY)
        if not find_image(scrcpy.last_frame, "res/darkforest/temporal_fountain.png", threshold=0.8):
            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
            time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/darkforest/temporal_fountain.png", timeout=5, random_delay=True):
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False

def kings_tower(device_id, scrcpy):
    go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower.png", threshold=0.8)
        time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower_main.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/kings_tower_battle.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/global/begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap_img_when_visible(device_id, scrcpy, "res/global/confirm_begin_autobattle_button.png", timeout=5, random_delay=True)
        time.sleep(DELAY)
        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
        time.sleep(DELAY)
        if tap_img_when_visible(device_id, scrcpy, "res/global/end_autobattle_button.png", timeout=5, random_delay=True):
            while not find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
    return False
        
# TODO: not yet implemented as I haven't unlocked highest level
def arcane_labyrinth(device_id, scrcpy, logger):
    go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

    if find_image(scrcpy.last_frame, "res/darkforest/darkforest_selected.png", threshold=0.8):
        tap_img_when_visible(device_id, scrcpy, "res/darkforest/arcane_labyrinth.png", threshold=0.8)
        time.sleep(DELAY)
        #TODO: Implement Arcane Labyrinth tasks

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