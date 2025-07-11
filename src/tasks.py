from adbauto import *
from src.utils import go_to_startscreen, is_color_match, choose_formation_to_copy, resource_path
import time

BACK_BUTTON = (30, 1890)
DELAY = 3

def set_delay(delay):
    try:
        global DELAY
        DELAY = delay
    except Exception as e:
        print(e)
        raise

# All functions related to campaign screen
def claim_afk_rewards(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            tap(device_id,  scrcpy.resolution[0]//2, scrcpy.resolution[1]//5*4) # Hard coded to click chest, as depending on how long you have been afk it uses a different image
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")) and not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png")):
                tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def campaign_battle(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/campaign/begin_battle_button.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/campaign/begin_battle_button_multistage.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/end_autobattle_button.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")) and not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png")):
                            tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                            time.sleep(DELAY)
                        return True
        return False
    except Exception as e:
        print(e)
        raise
        

def claim_fast_rewards(device_id, scrcpy, amount, logger):
    try:
        go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/campaign/fast_rewards.png")) or tap_img_when_visible(device_id, scrcpy, resource_path("res/campaign/fast_rewards_red.png")):
                time.sleep(DELAY)
                claim_button = find_image(scrcpy.last_frame, resource_path("res/campaign/fast_rewards_free.png"))
                if not claim_button:
                    logger("Fast rewards already claimed! Skipping this task.", "warning")
                    tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                    return True
                for _ in range(amount):
                    tap(device_id, claim_button[0], claim_button[1])
                    time.sleep(DELAY)
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")) and not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png")):
                    tap(device_id,  BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise
            
def friendship_points(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/friends.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/banner/friends.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/friend_points.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise

def loan_mercenaries(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/friends.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/banner/friends.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mercenaries.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mercenaries_manage.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mercenaries_apply.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mercenaries_lend.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)
                    return True
        return False
    except Exception as e:
        print(e)
        raise

def read_mail(device_id, scrcpy, delete=False):
    try:
        go_to_startscreen(device_id, scrcpy, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/mail.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/banner/mail.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mail_read.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if delete:
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mail_delete.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        tap_img_when_visible(device_id, scrcpy, resource_path("res/banner/mail_delete_confirm.png"), timeout=5, random_delay=True)
                        time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise

def bounty_board(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/bounty_board.png"))
            time.sleep(DELAY)

            # This is only when an event is active
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/event_bounty_unselected.png")) or find_image(scrcpy.last_frame, resource_path("res/darkforest/event_bounty_selected.png")):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_claim.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                while tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/event_bounty_dispatch.png")):
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_herochoice.png"), timeout=5, random_delay=True, threshold=0.8)
                    time.sleep(DELAY)
                    tap(device_id, 118, 1482) # This is the upper left hero (what the game advices to send)
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_start.png"), timeout=5, random_delay=True)
                    time.sleep(DELAY)

            # This is the solo bounty board TODO: Make it possible to send each bounty on their own
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/solo_bounty_unselected.png")) or find_image(scrcpy.last_frame, resource_path("res/darkforest/solo_bounty_selected.png")):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_claim.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_dispatch.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_start.png"))
                    time.sleep(DELAY)

            # This is the team bounty board
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/team_bounty_unselected.png")) or find_image(scrcpy.last_frame, resource_path("res/darkforest/team_bounty_selected.png")):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_claim.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_dispatch.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/solo_bounty_start.png"))
                    time.sleep(DELAY)

            tap_img_when_visible(device_id, scrcpy, resource_path("res/global/back_arrow.png"), timeout=5, random_delay=True)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def claim_weekly_staves(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/gg.png"), timeout=5, random_delay=True, threshold=0.8)
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def treasure_scramble(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "arena", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/treasure_scramble.png"), random_delay=True, threshold=0.8):
                time.sleep(DELAY)
                while find_image(scrcpy.last_frame, resource_path("res/darkforest/treasure_scramble_flag.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/treasure_scramble_flag.png"), random_delay=True, threshold=0.8)
                    time.sleep(DELAY)
                    if find_image(scrcpy.last_frame, resource_path("res/darkforest/treasure_scramble_button.png")):
                        tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/treasure_scramble_button.png"), random_delay=True, threshold=0.8)
                        time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise
            
def arena_of_heroes(device_id, scrcpy, amount, logger):
    try:
        go_to_startscreen(device_id, scrcpy, "arena", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes.png")):
                time.sleep(DELAY)
                if not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text.png")):
                    return False
                # Clear exclamation mark
                if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_record.png")):
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text.png")):
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)
                # Start battles
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/arena_of_heroes_challenge.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    for battle in range(amount):
                        win = False
                        if not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text2.png")):
                            return False, battle
                        possible_enemies = find_all_images(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_button.png"))
                        weakest_enemy = sorted(possible_enemies, key=lambda pt: pt[1], reverse=True)[0]
                        tap(device_id, weakest_enemy[0], weakest_enemy[1])
                        time.sleep(DELAY)
                        tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/arena_of_heroes_battle.png"), timeout=5, random_delay=True)
                        time.sleep(DELAY)
                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/arena_of_heroes_skip.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text2.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_reward.png")):
                                win = True
                            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                            time.sleep(DELAY)
                        logger(f"Arena of Heroes battle {battle + 1} {'won' if win else 'lost'}", "success" if win else "error")
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)

                    return True, battle + 1
        return False, 0
    except Exception as e:
        print(e)
        raise

def gladiator_coins(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "arena", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
            while not tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/legend_challenger.png")):
                #TODO: Check scroll distance when an event is active
                scroll(device_id, "up", 300, scrcpy.resolution[0]//2, scrcpy.resolution[1]//2)
                time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/legend_challenger_chest1.png"), timeout=5, random_delay=True) or tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/legend_challenger_chest2.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise

def temporal_rift(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/temporal_rift.png"), threshold=0.8)
            time.sleep(DELAY)
            if not find_image(scrcpy.last_frame, resource_path("res/darkforest/temporal_fountain.png"), threshold=0.8):
                tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/temporal_fountain.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise

def kings_tower(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_main.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY+3)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY+3)
                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                            time.sleep(DELAY*2)
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/end_autobattle_button.png"), timeout=5, random_delay=True):
                                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                                    time.sleep(DELAY)
                                return True
        return False
    except Exception as e:
        print(e)
        raise
        
def arcane_labyrinth(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/arcane_labyrinth.png"), threshold=0.8)
            time.sleep(DELAY)
            #TODO: Implement Arcane Labyrinth tasks
    except Exception as e:
        print(e)
        raise

def claim_wall_reward(device_id, scrcpy):
    try:
        if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/wall_rewards.png"), timeout=5, random_delay=True):
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/wall_claim.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
        while not find_image(scrcpy.last_frame, resource_path("res/city/wall_text.png")):
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(DELAY)
    except Exception as e:
        print(e)
        raise

def wall_of_legends(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, "citydown", DELAY)
        
        if find_image(scrcpy.last_frame, resource_path("res/city/wall_red.png")):
            tap_img_when_visible(device_id, scrcpy, resource_path("res/city/wall_red.png"))
            time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/city/wall_text.png")):
                claimed = False       
                # TODO: Change Coordinates and Values when I get this next milestone
                if is_color_match(get_pixel_color(scrcpy.last_frame, 475, 216), (233, 66, 54)): # Lightbearers Milestone
                    tap(device_id, 475, 216)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed Lightbearers Milestone", "success")
                    claimed = True

                if is_color_match(get_pixel_color(scrcpy.last_frame, 1024, 216), (255, 100, 65)): # Maulers Milestone
                    tap(device_id, 1024, 216)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed Maulers Milestone", "success")
                    claimed = True

                # TODO: Change Coordinates when I get this next milestone
                if is_color_match(get_pixel_color(scrcpy.last_frame, 475, 597), (255, 100, 65)): # Wilders Milestone
                    tap(device_id, 475, 597)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed Wilders Milestone", "success")
                    claimed = True

                if is_color_match(get_pixel_color(scrcpy.last_frame, 1024, 597), (255, 100, 65)): # Graveborn Milestone
                    tap(device_id, 1024, 597)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed Graveborn Milestone", "success")
                    claimed = True

                if is_color_match(get_pixel_color(scrcpy.last_frame, 1014, 995), (233, 60, 40)): # Campaign Stage Milestone
                    tap(device_id, 1014, 995)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed Campaign Stage Milestone", "success")
                    claimed = True

                # TODO: Change Coordinates when I get this next milestone
                if is_color_match(get_pixel_color(scrcpy.last_frame, 1014, 1345), (233, 66, 54)): # King's Tower Milestone
                    tap(device_id, 1014, 1345)
                    time.sleep(DELAY)
                    claim_wall_reward(device_id, scrcpy)
                    logger("Claimed King's Tower Milestone", "success")
                    claimed = True
                    
                while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                return claimed
        return False
    except Exception as e:
        print(e)
        raise

def store_purchases(device_id, scrcpy, refreshes):
    try:
        go_to_startscreen(device_id, scrcpy, "citydown", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/store.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store.png"))
            time.sleep(DELAY)

            refresh_count = 0
            
            for refresh in range(refreshes + 1):  # +1 for the initial buy
                if not find_image(scrcpy.last_frame, resource_path("res/city/store_text.png")):
                    tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                    time.sleep(DELAY)
                    return False, refresh_count
                if find_image(scrcpy.last_frame, resource_path("res/city/store_quickbuy.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_quickbuy.png"))
                    time.sleep(DELAY)
                    if find_image(scrcpy.last_frame, resource_path("res/city/store_purchase.png"), threshold=0.8):
                        tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_purchase.png"), threshold=0.8)
                        time.sleep(DELAY)
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)
                        if refresh_count != refreshes:
                            if find_image(scrcpy.last_frame, resource_path("res/city/store_refresh.png")):
                                tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_refresh.png"))
                                time.sleep(DELAY)
                                if find_image(scrcpy.last_frame, resource_path("res/city/store_refresh_confirm.png")):
                                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_refresh_confirm.png"))
                                    time.sleep(DELAY)
                                    refresh_count += 1
            while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)

            return True, refresh_count

        return False, 0
    except Exception as e:
        print(e)
        raise

def resonating_crystal(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "citydown", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/crystal.png")):
            return False

        if find_image(scrcpy.last_frame, resource_path("res/city/crystal_red.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/crystal_red.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/crystal_levelup.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/crystal_confirm.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/city/crystal_strengthen.png")):
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                        time.sleep(DELAY)
            while find_image(scrcpy.last_frame, resource_path("res/city/crystal_strengthen.png")):
                tap_image(device_id, scrcpy.last_frame, resource_path("res/city/crystal_strengthen.png"))
                time.sleep(DELAY/2)
            while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
            return True
        tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
        return False
    except Exception as e:
        print(e)
        raise

def hunting_contract(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "guild", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/guild_hunt.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hunt.png"))
            time.sleep(DELAY)
            while tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_contract.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_nextteam.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_beginbattle.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/arena_of_heroes_skip.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)
                            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                            time.sleep(DELAY)
            while tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_contract_chest.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def guild_hunt(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "guild", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/guild_hunt.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hunt.png"))
            time.sleep(DELAY)
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow1.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow1.png"), threshold=0.8)
                    time.sleep(DELAY)
                elif find_image(scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow2.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow2.png"), threshold=0.8)
                    time.sleep(DELAY)
                elif find_image(scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow3.png"), threshold=0.8):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hunt_arrow3.png"), threshold=0.8)
                    time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_hunt_quickbattle.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_hunt_sweep.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def twisted_realm(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "guild", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/guild_hell.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_hell.png"))
            time.sleep(DELAY)
            if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_twistedrealm.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_twisted_begin.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_twisted_auto.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/city/guild_twisted_noskip.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/guild_twisted_noskip.png"))
                            time.sleep(DELAY)
                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_twisted_activate.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)
                            tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_twisted_exit.png"), timeout=5, random_delay=True)
                            time.sleep(DELAY)
                            while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                                time.sleep(DELAY)
                            return True
        while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
            tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
            time.sleep(DELAY)
        return False
    except Exception as e:
        print(e)
        raise

def oak_inn_gifts(device_id, scrcpy):
    try:
        go_to_startscreen(device_id, scrcpy, "cityup", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/inn.png"), threshold=0.8):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/inn.png"), threshold=0.8)
            time.sleep(DELAY)
            while find_image(scrcpy.last_frame, resource_path("res/city/inn_gift.png"), threshold=0.8):
                tap_image(device_id, scrcpy.last_frame, resource_path("res/city/inn_gift.png"), threshold=0.8)
                time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                tap(device_id, BACK_BUTTON[0], BACK_BUTTON[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise

def push_campaign(device_id, scrcpy, logger, formation_no=1, artifacts=True, singlestage=False):
    try:
        while True:
            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_campaign.png")):
                go_to_startscreen(device_id, scrcpy, "campaign", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/campaign/begin_battle_button.png"), threshold=0.8)
                    time.sleep(DELAY)
                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/campaign/begin_battle_button_multistage.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
            print(singlestage, find_image(scrcpy.last_frame, resource_path("res/autopush/singlestage.png"), threshold=0.8), formation_no > 0)
            match singlestage, find_image(scrcpy.last_frame, resource_path("res/autopush/singlestage.png"), threshold=0.8), formation_no > 0:
                case (True, _, True):
                    choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                case (False, None, True):
                    choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                case (False, _, True):
                    pass
                case (_, _, False):
                    pass

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    level_up = False
                    time.sleep(30)
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0.png"), threshold=0.9):
                            time.sleep(30)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(30)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"))
                    time.sleep(DELAY)
    except Exception as e:
        print(e)
        raise

def push_tower(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:

        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_tower.png")):
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_tower.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_main.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0tower.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"))
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_lb(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:
        
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_lb.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_lb.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_lb.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0lb.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"))
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_m(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:
        
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_m.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_m.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_m.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0m.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"))
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_w(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:

        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_w.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_w.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_w.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0w.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"))
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_gb(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:

        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_gb.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_gb.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_gb.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0gb.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png")):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8)
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_cel(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:

        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_cel.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_cel.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_cel.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0cel.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png")):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8)
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise

def push_hypo(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    try:

        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_hypo.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True)
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/vs_hypo.png")):
                go_to_startscreen(device_id, scrcpy, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower.png"), threshold=0.8)
                    time.sleep(DELAY)

                    if tap_img_when_visible(device_id, scrcpy, resource_path("res/autopush/kings_tower_hypo.png"), timeout=5, random_delay=True):
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                            return True

                        if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/kings_tower_battle.png"), timeout=5, random_delay=True):
                            time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)

            if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/begin_autobattle_button.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/global/confirm_begin_autobattle_button.png"), timeout=5, random_delay=True, threshold=0.8):
                    time.sleep(DELAY*2)
                    level_up = False
                    while not level_up:
                        while find_image(scrcpy.last_frame, resource_path("res/autopush/push_0hypo.png"), threshold=0.9):
                            time.sleep(10)
                        tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png")):
                            tap(device_id, scrcpy.resolution[0] // 2, scrcpy.resolution[1] // 2)
                            time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/confirm_0.png")):
                            tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_close.png"), threshold=0.8)
                            time.sleep(10)
                        else:
                            level_up = True
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/autopush/confirm_exit.png"), threshold=0.8)
                    time.sleep(DELAY)

    except Exception as e:
        print(e)
        raise