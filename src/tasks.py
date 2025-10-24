from adbauto import *
from src.utils import go_to_startscreen, is_color_match, choose_formation_to_copy, resource_path, remove_duplicate_centers
from src.strings import *
import time
from PIL import Image
from datetime import datetime, timezone
import cv2

## Global values
DELAY = 3


def set_delay(delay):
    """
    Set the global delay value for all tasks, ensuring it is at least 1 second.
    
    Args:
        delay (int): The delay in seconds to be set.
    """
    try:
        global DELAY
        DELAY = delay if delay >= 1 else 1
    except Exception as e:
        print(e)
        raise


def claim_afk_rewards(device_id, scrcpy, logger):
    """
    Claims AFK rewards from the campaign screen.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
    
    Returns:
        bool: True if rewards were claimed, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            tap(device_id,  claim_afk_rewards_chest[0], claim_afk_rewards_chest[1])
            time.sleep(DELAY)
            if not find_image(scrcpy.last_frame, resource_path("res/campaign/claim_afk_rewards_text.png")):
                return False
            tap(device_id,  collect_afk_rewards_button[0], collect_afk_rewards_button[1])
            return True
    except Exception as e:
        print(e)
        raise


def campaign_battle(device_id, scrcpy, logger):
    """
    Performs a campaign battle from the campaign screen.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if the battle was completed, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            tap(device_id, campaign_screen_battle_button[0], campaign_screen_battle_button[1])
            time.sleep(DELAY)
            ## If it is a multi stage battle, there is an extra button to tap
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/campaign/multi_battle_text.png")):
                    tap(device_id, campaign_multi_battle_button[0], campaign_multi_battle_button[1])
                    time.sleep(DELAY)
                    break
                time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                    tap(device_id, start_battle_button[0], start_battle_button[1])
                    time.sleep(DELAY)
                    ## Confirm begin autobattle
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                        return False
                    while find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                        time.sleep(1)
                    tap(device_id, pause_battle_button[0], pause_battle_button[1])
                    time.sleep(DELAY)
                    tap(device_id, exit_battle_button[0], exit_battle_button[1])
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                        time.sleep(1)
                    tap(device_id, back_button[0], back_button[1])
                    return True
                time.sleep(DELAY)
        return False
    except Exception as e:
        print(e)
        raise
        

def claim_fast_rewards(device_id, scrcpy, amount, logger):
    """
    Claims fast rewards from the campaign screen.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        amount (int): The number of times to claim fast rewards.
        logger (function): Logger function to log messages.

    Returns:
        bool: True if the fast rewards were claimed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "campaign", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
            tap(device_id, fast_reward_button[0], fast_reward_button[1])
            time.sleep(DELAY)
            if find_image(scrcpy.last_frame, resource_path("res/campaign/fast_rewards_text.png")):
                if not find_image(scrcpy.last_frame, resource_path("res/campaign/fast_rewards_free.png")):
                    logger("Fast rewards already claimed! Skipping this task.", "warning")
                    tap(device_id,  back_button[0], back_button[1])
                    return True      
                for _ in range(amount):
                    tap(device_id, claim_fast_rewards_button[0], claim_fast_rewards_button[1])
                    time.sleep(DELAY)
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")) and not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png")):
                    tap(device_id,  back_button[0], back_button[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise

            
def friendship_points(device_id, scrcpy, logger):
    """
    Sends and receives friendship points from friends.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.

    Returns:
        bool: True if friendship points were sent/received successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/friends.png")):
            tap(device_id, banner_friends_button[0], banner_friends_button[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/banner/friends_text.png")):
                    tap(device_id, friends_send_and_receive_button[0], friends_send_and_receive_button[1])
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
                    return True
                time.sleep(DELAY)
        return False
    except Exception as e:
        print(e)
        raise


def loan_mercenaries(device_id, scrcpy, logger):
    """
    Manages mercenaries by sending them to friends.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.

    Returns:
        bool: True if mercenaries were sent successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/friends.png")):
            tap(device_id, banner_friends_button[0], banner_friends_button[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/banner/friends_text.png")):
                    tap(device_id, friends_mercenaries_button[0], friends_mercenaries_button[1])
                    time.sleep(DELAY)
                    break
                time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/banner/mercenaries_text.png")):
                    time.sleep(DELAY)
                    tap(device_id, friends_mercenaries_manage_button[0], friends_mercenaries_manage_button[1])
                    time.sleep(DELAY)
                    tap(device_id, friends_mercenaries_apply_button[0], friends_mercenaries_apply_button[1])
                    time.sleep(DELAY)
                    tap(device_id, friends_mercenaries_send_button[0], friends_mercenaries_send_button[1])
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
                    return True
        return False
    except Exception as e:
        print(e)
        raise


def read_mail(device_id, scrcpy, logger, delete=False):
    """
    Reads and optionally deletes all mail.
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        delete (bool): Whether to delete all mail after reading.
        
    Returns:
        bool: True if mail was read (and deleted if specified) successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "rightbanner", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/banner/friends.png")):
            tap(device_id, banner_mail_button[0], banner_mail_button[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/banner/mail_text.png")):
                    tap(device_id, mail_claim_all_button[0], mail_claim_all_button[1])
                    time.sleep(DELAY)
                    tap(device_id, mail_claim_rewards_button[0], mail_claim_rewards_button[1])
                    time.sleep(DELAY)
                    if delete:
                        tap(device_id, mail_delete_all_button[0], mail_delete_all_button[1])
                        time.sleep(DELAY)
                        tap(device_id, mail_delete_all_confirm_button[0], mail_delete_all_confirm_button[1])
                        time.sleep(DELAY)
                        while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                            tap(device_id, back_button[0], back_button[1])
                            time.sleep(DELAY)
                    return True
                time.sleep(DELAY)
        return False
    except Exception as e:
        print(e)
        raise


def bounty_board(device_id, scrcpy, logger):
    """
    Manages the bounty board by claiming and dispatching bounties.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if bounty board was managed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap(device_id, bounty_board_on_map[0], bounty_board_on_map[1])
            time.sleep(DELAY)
            if find_image(scrcpy.last_frame, resource_path("res/darkforest/bounty_board_text.png")):

                # This is only when an event is active
                ## TODO: Rewrite this once there is a new event
                # if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/event_bounty_unselected.png")) or find_image(scrcpy.last_frame, resource_path("res/darkforest/event_bounty_selected.png")):
                #     time.sleep(DELAY)
                #     if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_claim.png"), timeout=5, random_delay=True):
                #         time.sleep(DELAY)
                #     while tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/event_bounty_dispatch.png")):
                #         time.sleep(DELAY)
                #         tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_herochoice.png"), timeout=5, random_delay=True, threshold=0.8)
                #         time.sleep(DELAY)
                #         tap(device_id, 118, 1482) # This is the upper left hero (what the game advices to send)
                #         time.sleep(DELAY)
                #         tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/event_bounty_start.png"), timeout=5, random_delay=True)
                #         time.sleep(DELAY)

                # This is the solo bounty board TODO: Make it possible to send each bounty on their own
                tap(device_id, bounty_board_solo_flag[0], bounty_board_solo_flag[1])
                time.sleep(DELAY)
                tap(device_id, bounty_board_claim_all_button[0], bounty_board_claim_all_button[1])
                time.sleep(DELAY)
                tap(device_id, bounty_board_send_all_button[0], bounty_board_send_all_button[1])
                time.sleep(DELAY)
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/bounty_board_dispatch_text.png")):
                    tap(device_id, bounty_board_dispatch_button[0], bounty_board_dispatch_button[1])
                    time.sleep(DELAY)

                # This is the team bounty board
                tap(device_id, bounty_board_team_flag[0], bounty_board_team_flag[1])
                time.sleep(DELAY)
                tap(device_id, bounty_board_claim_all_button[0], bounty_board_claim_all_button[1])
                time.sleep(DELAY)
                tap(device_id, bounty_board_send_all_button[0], bounty_board_send_all_button[1])
                time.sleep(DELAY)
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/bounty_board_dispatch_text.png")):
                    tap(device_id, bounty_board_dispatch_button[0], bounty_board_dispatch_button[1])
                    time.sleep(DELAY)

                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png")):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise


## TODO: Add timing memory as this needs to be done only once in a week
def claim_weekly_staves(device_id, scrcpy, logger):
    """
    Claims weekly staves from the Ghoulish Gallery.
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if weekly staves were claimed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap(device_id, ghoulish_gallery_on_map[0], ghoulish_gallery_on_map[1])
            time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise


def treasure_scramble(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "arena", DELAY)

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
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise


def arena_of_heroes(device_id, scrcpy, amount, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "arena", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
            if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes.png")):
                time.sleep(DELAY)
                if not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text.png")):
                    return False
                # Clear exclamation mark
                if tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_record.png")):
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_of_heroes_text.png")):
                        tap(device_id, back_button[0], back_button[1])
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
                            tap(device_id, back_button[0], back_button[1])
                            time.sleep(DELAY)
                        logger(f"Arena of Heroes battle {battle + 1} {'won' if win else 'lost'}", "success" if win else "error")
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)

                    return True, battle + 1
        return False, 0
    except Exception as e:
        print(e)
        raise


def gladiator_coins(device_id, scrcpy, logger):
    """
    Claims gladiator coins from the arena legends challenger chest.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if gladiator coins were claimed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "arena", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
            while not tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/legend_challenger.png")):
                #TODO: Check scroll distance when an event is active
                scroll(device_id, "up", 300, scrcpy.resolution[0]//2, scrcpy.resolution[1]//2)
                time.sleep(DELAY)
            if find_image(scrcpy.last_frame, resource_path("res/darkforest/legend_challenger_text.png")):
                time.sleep(DELAY)
                tap(device_id, arena_legends_challenger_chest[0], arena_legends_challenger_chest[1])
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/arena_text.png")):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise


def temporal_rift(device_id, scrcpy, logger):
    """
    Claims the afk rewards from the temporal rift fountain.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if temporal rift rewards were claimed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap(device_id, temporal_rift_on_map[0], temporal_rift_on_map[1])
            time.sleep(DELAY)
            if not find_image(scrcpy.last_frame, resource_path("res/darkforest/temporal_rift_text.png")):
                tap(device_id, middle_of_screen[0], middle_of_screen[1])
                time.sleep(DELAY)
            if find_image(scrcpy.last_frame, resource_path("res/darkforest/temporal_rift_text.png")):
                tap(device_id, temporal_rift_fountain[0], temporal_rift_fountain[1])
                time.sleep(DELAY)
                while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                return True
        return False
    except Exception as e:
        print(e)
        raise


def kings_tower(device_id, scrcpy, logger):
    """
    Performs a battle in the King's Tower.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        
    Returns:
        bool: True if the battle was completed, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                    break
                time.sleep(DELAY)
            tap(device_id, kings_tower_main[0], kings_tower_main[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_main_text.png")):
                    break
                time.sleep(DELAY)
            tap(device_id, kings_tower_button[0], kings_tower_button[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                    tap(device_id, start_battle_button[0], start_battle_button[1])
                    time.sleep(DELAY)
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                        return False
                    ## Confirm begin autobattle
                    while find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                        time.sleep(1)
                    tap(device_id, pause_battle_button[0], pause_battle_button[1])
                    time.sleep(DELAY)
                    tap(device_id, exit_battle_button[0], exit_battle_button[1])
                    time.sleep(DELAY)
                    while not find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                        time.sleep(1)
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
                    return True
        return False
    except Exception as e:
        print(e)
        raise


def arcane_labyrinth(device_id, scrcpy, logger):
    """
    Completes the Arcane Labyrinth.
    IMPORTANT: You need to have the Dismal Labyrinth with sweeping unlocked.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
    
    Returns:
        bool: True if the Arcane Labyrinth was completed successfully, False otherwise.
    """
    try:
        go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
            tap(device_id, labyrinth_on_map[0], labyrinth_on_map[1])
            time.sleep(DELAY)
            ## This screen takes longer to load, so a little delay added
            for _ in range(3):
                if not find_image(scrcpy.last_frame, resource_path("res/darkforest/labyrinth_text.png")):
                    time.sleep(DELAY)
                else:
                    break
            tap(device_id, labyrinth_dismal_maze[0], labyrinth_dismal_maze[1])
            time.sleep(DELAY)
            ## Check if in a team or solo
            if find_image(scrcpy.last_frame, resource_path("res/darkforest/labyrinth_team_text.png")):
                if tap_img_when_visible(device_id, scrcpy, resource_path("res/darkforest/labyrinth_team_sweep.png"), timeout=5, random_delay=True):
                    time.sleep(DELAY)
                    if find_image(scrcpy.last_frame, resource_path("res/darkforest/labyrinth_sweep_confirm.png")):
                        tap(device_id, labyrinth_sweep_button[0], labyrinth_sweep_button[1])
                        time.sleep(DELAY)
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/labyrinth_roamer.png")):
                            tap(device_id, labyrinth_exit_roamer[0], labyrinth_exit_roamer[1])
                            time.sleep(DELAY)
                            return True
                ## In a team but already done labyrinth
                elif find_image(scrcpy.last_frame, resource_path("res/darkforest/labyrinth_team_sweep_done.png")):
                    logger("Labytinth already done this cycle... Skipping.", "info")
                    while not find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
                    return True
                ## In a team, but teammates didn't sweep, so start doing it yourself
                ## TODO
                else:
                    pass
            ## Solo labyrinth
            ##TODO
            else:
                pass
    except Exception as e:
        print(e)
        raise


def store_purchases(device_id, scrcpy, logger, refreshes):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "citydown", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/store.png")):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store.png"))
            time.sleep(DELAY)

            refresh_count = 0
            
            for refresh in range(refreshes + 1):  # +1 for the initial buy
                if not find_image(scrcpy.last_frame, resource_path("res/city/store_text.png")):
                    tap(device_id, back_button[0], back_button[1])
                    time.sleep(DELAY)
                    return False, refresh_count
                if find_image(scrcpy.last_frame, resource_path("res/city/store_quickbuy.png")):
                    tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_quickbuy.png"))
                    time.sleep(DELAY)
                    if find_image(scrcpy.last_frame, resource_path("res/city/store_purchase.png"), threshold=0.8):
                        tap_image(device_id, scrcpy.last_frame, resource_path("res/city/store_purchase.png"), threshold=0.8)
                        time.sleep(DELAY)
                        tap(device_id, back_button[0], back_button[1])
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
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)

            return True, refresh_count

        return False, 0
    except Exception as e:
        print(e)
        raise


def resonating_crystal(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "citydown", DELAY)

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
                        tap(device_id, back_button[0], back_button[1])
                        time.sleep(DELAY)
            while find_image(scrcpy.last_frame, resource_path("res/city/crystal_strengthen.png")):
                tap_image(device_id, scrcpy.last_frame, resource_path("res/city/crystal_strengthen.png"))
                time.sleep(DELAY/2)
            while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
            return True
        tap_image(device_id, scrcpy.last_frame, resource_path("res/darkforest/darkforest_unselected.png"), threshold=0.8)
        return False
    except Exception as e:
        print(e)
        raise


def hunting_contract(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "guild", DELAY)

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
                            tap(device_id, back_button[0], back_button[1])
                            time.sleep(DELAY)
            while tap_img_when_visible(device_id, scrcpy, resource_path("res/city/guild_contract_chest.png"), timeout=5, random_delay=True):
                time.sleep(DELAY)
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise


def guild_hunt(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "guild", DELAY)

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
                        tap(device_id, back_button[0], back_button[1])
            while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise


def twisted_realm(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "guild", DELAY)

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
                                tap(device_id, back_button[0], back_button[1])
                                time.sleep(DELAY)
                            return True
        while not find_image(scrcpy.last_frame, resource_path("res/city/guild_text.png")):
            tap(device_id, back_button[0], back_button[1])
            time.sleep(DELAY)
        return False
    except Exception as e:
        print(e)
        raise


def oak_inn_gifts(device_id, scrcpy, logger):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "cityup", DELAY)

        if find_image(scrcpy.last_frame, resource_path("res/city/inn.png"), threshold=0.8):
            tap_image(device_id, scrcpy.last_frame, resource_path("res/city/inn.png"), threshold=0.8)
            time.sleep(DELAY)
            while find_image(scrcpy.last_frame, resource_path("res/city/inn_gift.png"), threshold=0.8):
                tap_image(device_id, scrcpy.last_frame, resource_path("res/city/inn_gift.png"), threshold=0.8)
                time.sleep(DELAY)
            while not find_image(scrcpy.last_frame, resource_path("res/city/city_selected.png"), threshold=0.8):
                tap(device_id, back_button[0], back_button[1])
                time.sleep(DELAY)
            return True
        return False
    except Exception as e:
        print(e)
        raise


def push_campaign(device_id, scrcpy, logger, formation_no=1, artifacts=True, singlestage=False):
    """
    Automates pushing through campaign battles.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        singlestage (bool): Whether to copy single stage battles. Default is False.
    """
    try:
        while True:
            if not find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                go_to_startscreen(device_id, scrcpy, logger, "campaign", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/campaign/campaign_selected.png")):
                    tap(device_id, campaign_screen_battle_button[0], campaign_screen_battle_button[1])
                    time.sleep(DELAY)
                    ## If it is a multi stage battle, there is an extra button to tap
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/campaign/multi_battle_text.png")):
                            tap(device_id, campaign_multi_battle_button[0], campaign_multi_battle_button[1])
                            time.sleep(DELAY)
                            break
                        time.sleep(DELAY)

            match singlestage, find_image(scrcpy.last_frame, resource_path("res/autopush/singlestage.png"), threshold=0.8), formation_no > 0:
                case (True, _, True):
                    choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                case (False, None, True):
                    choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                case (False, _, True):
                    pass
                case (_, _, False):
                    pass

            time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue campaign push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/hero_xp_increase.png")):
                            tap(device_id, exit_auto_battle_button[0], exit_auto_battle_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_text.png")):
                                tap(device_id, continue_auto_battle_button[0], continue_auto_battle_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_tower(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_main_text.png")):
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_main[0], kings_tower_main[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_main_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/campaign/battle_factions.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_lb(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Lightbearer faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.

    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_lb.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_lightbearer.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_lightbearer[0], kings_tower_lightbearer[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_lb.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_lightbearer.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_m(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Mauler faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        
    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_m.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_mauler.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_mauler[0], kings_tower_mauler[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_m.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                                return True
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_mauler.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_w(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Wilder faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        
    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_w.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_wilder.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_wilder[0], kings_tower_wilder[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_w.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                                return True
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_wilder.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_gb(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Graveborn faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        
    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_gb.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_graveborn.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_graveborn[0], kings_tower_graveborn[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_gb.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                                return True
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_graveborn.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_cel(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Celestial faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        
    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_cel.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_celestial.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_celestial[0], kings_tower_celestial[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_cel.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                                return True
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_celestial.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def push_hypo(device_id, scrcpy, logger, formation_no=1, artifacts=True):
    """
    Automates pushing through King's Tower battles for Hypogean faction.
    
    Args:
        device_id (str): The ID of the device.
        scrcpy (Scrcpy): The Scrcpy instance for screen capturing.
        logger (function): Logger function to log messages.
        formation_no (int): The formation number to use. Default is 1.
        artifacts (bool): Whether to copy artifacts. Default is True.
        
    Returns:
        bool: True if the maximum amount of floors was reached, stays in a loop until interrupted otherwise.
    """
    try:
        while True:
            if find_image(scrcpy.last_frame, resource_path("res/autopush/text_hypo.png")):
                if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                    return True
                tap(device_id, kings_tower_button[0], kings_tower_button[1])
                time.sleep(DELAY)

            if not find_image(scrcpy.last_frame, resource_path("res/autopush/battle_hypogean.png")):
                go_to_startscreen(device_id, scrcpy, logger, "darkforest", DELAY)

                if find_image(scrcpy.last_frame, resource_path("res/darkforest/darkforest_selected.png"), threshold=0.8):
                    tap(device_id, kings_tower_on_map[0], kings_tower_on_map[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/darkforest/kings_tower_text.png")):
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_hypogean[0], kings_tower_hypogean[1])
                    time.sleep(DELAY)
                    ## This screen takes longer to load, so a little delay added
                    for _ in range(3):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/text_hypo.png")):
                            if find_image(scrcpy.last_frame, resource_path("res/autopush/done_60.png")):
                                return True
                            break
                        time.sleep(DELAY)
                    tap(device_id, kings_tower_button[0], kings_tower_button[1])
                    time.sleep(DELAY)

            if formation_no > 0:
                choose_formation_to_copy(device_id, scrcpy, logger, formation_no, artifacts, DELAY)
                time.sleep(DELAY)

            if find_image(scrcpy.last_frame, resource_path("res/autopush/battle_hypogean.png")):
                tap(device_id, start_auto_battle_button[0], start_auto_battle_button[1])
                time.sleep(DELAY)
                tap(device_id, confirm_auto_battle_button[0], confirm_auto_battle_button[1])
                time.sleep(1)
                if find_image(scrcpy.last_frame, resource_path("res/autopush/not_enough_cr.png")):
                    logger("Combat rating too low to continue tower push.", "error")
                    return
                level_up = False
                time.sleep(30)
                while not level_up:
                    time.sleep(60)
                    tap(device_id, middle_of_screen[0], middle_of_screen[1])
                    time.sleep(DELAY)
                    ## Check for level up screen
                    if find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                        if find_image(scrcpy.last_frame, resource_path("res/autopush/items_placed_in_bag.png")):
                            tap(device_id, exit_auto_battle_tower_button[0], exit_auto_battle_tower_button[1])
                            time.sleep(DELAY)
                            level_up = True
                        else:
                            while find_image(scrcpy.last_frame, resource_path("res/autopush/pause_auto_battle_tower_text.png")):
                                tap(device_id, continue_auto_battle_tower_button[0], continue_auto_battle_tower_button[1])
                                time.sleep(DELAY)
    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise


def unlimited_summons_cycle(device_id, scrcpy, logger, awakened=[], celepog=[], F4=[], overwrite_on_success="False", double_4f="False"):
    try:
        go_to_startscreen(device_id, scrcpy, logger, "unlimited", DELAY)
        found_summon = False
        cycle = 1
        seen_awakened = 0
        seen_celepog = 0
        seen_4f = 0
        overwrite_on_success = True if overwrite_on_success == "True" else False
        double_4f = True if double_4f == "True" else False
        while not found_summon:
            time.sleep(5)
            found_awakened = False
            found_celepog = False
            found_4f = False

            if find_image(scrcpy.last_frame, resource_path("res/unlimited/back.png")):
                tap(device_id, unlimited_summons_tap_next[0], unlimited_summons_tap_next[1])
                time.sleep(5)

            if awakened == []:
                found_awakened = True
            else:
                for a in awakened:
                    if find_image(scrcpy.last_frame, resource_path(f"res/unlimited/{a}.png"), threshold=0.8):
                        found_awakened = True
                        seen_awakened += 1

            if celepog == []:
                found_celepog = True
            else:
                for c in celepog:
                    if find_image(scrcpy.last_frame, resource_path(f"res/unlimited/{c}.png"), threshold=0.8):
                        found_celepog = True
                        seen_celepog += 1

            if F4 == []:
                found_4f = True
            else:
                for f in F4:
                    if double_4f:
                        summoned_4f = find_all_images(scrcpy.last_frame, resource_path(f"res/unlimited/{f}.png"), threshold=0.8)
                        summoned_4f = remove_duplicate_centers(summoned_4f)
                        if len(summoned_4f) >= 2:
                            found_4f = True
                            seen_4f += len(summoned_4f)

                    else:
                        if find_image(scrcpy.last_frame, resource_path(f"res/unlimited/{f}.png"), threshold=0.8):
                            found_4f = True
                            seen_4f += 1

            match found_awakened, found_celepog, found_4f:
                case (True, True, True):
                    logger(f"Cycle {cycle} [Saw {awakened} {seen_awakened} time(s), {celepog} {seen_celepog} time(s), and {F4} {seen_4f} time(s).]: Found the summon we want! Waiting for player to double-check...", "success")
                    found_summon = True
                    tap(device_id, unlimited_summons_tap_record[0], unlimited_summons_tap_record[1])
                    time.sleep(5)
                    if find_image(scrcpy.last_frame, resource_path("res/unlimited/replace_record.png")) and overwrite_on_success:
                        tap(device_id, unlimited_summons_tap_replace[0], unlimited_summons_tap_replace[1])

                case (True, True, False):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {awakened} and {celepog}, but not {F4}. Trying again...", "info")

                case (True, False, False):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {awakened}, but not {celepog} and not {F4}. Trying again...", "info")

                case (True, False, True):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {awakened} and {F4}, but not {celepog}. Trying again...", "info")

                case (False, True, False):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {celepog}, but not {awakened} and not {F4}. Trying again...", "info")

                case (False, True, True):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {celepog} and {F4}, but not {awakened}. Trying again...", "info")

                case (False, False, False):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found neither {awakened} nor {celepog} nor {F4}. Trying again...", "info")

                case (False, False, True):
                    logger(f"Cycle {cycle} [{seen_awakened}/{seen_celepog}/{seen_4f}]: Found {F4}, but not {awakened} and not {celepog}. Trying again...", "info")

            if not found_summon:
                cycle += 1
                for _ in range(2):
                    tap(device_id, unlimited_summons_tap_next[0], unlimited_summons_tap_next[1])
                    time.sleep(1)

    except Exception as e:
        logger(f"Error occurred: {e}", "error")
        raise