# src/autoafk.py
from adbauto import *
from src.tasks import *
from src.utils import get_config_path
from PIL import Image
from datetime import datetime, timezone
import cv2
import configparser

DEVICE_ID = ""
SCRCPY_CLIENT = None
CONFIG_PATH = get_config_path()
BACK_BUTTON = (30, 1890)
MAX_ATTEMPTS = 0
DELAY = 0

def connect_emulator(logger):
    try:
        global DEVICE_ID

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        port = int(config['Global']['Emulator Port']) if 'Emulator Port' in config['Global'] else 5555
        DEVICE_ID = get_emulator_device(port)
        logger(f"Connected to emulator with device ID: {DEVICE_ID}", "success")
    except Exception as e:
        logger(f"Failed to connect to emulator: {e}", "error")
        DEVICE_ID = ""
        return

def start_scrcpy_client(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT
        if not DEVICE_ID:
            logger("No device connected. Please connect to an emulator first.", "error")
            return
        
        if SCRCPY_CLIENT:
            logger("scrcpy client is already running.", "info")
            return
        
        SCRCPY_CLIENT = start_scrcpy(DEVICE_ID)
        logger("Started video stream.", "success")
        return
    except Exception as e:
        logger(f"Failed to start scrcpy client: {e}", "error")
        SCRCPY_CLIENT = None
        return

def stop_scrcpy_client(logger):
    global SCRCPY_CLIENT
    if not SCRCPY_CLIENT:
        logger("scrcpy client is not running.", "info")
        return
    
    stop_scrcpy(SCRCPY_CLIENT)
    SCRCPY_CLIENT.last_frame = None
    SCRCPY_CLIENT = None
    logger("Video stream stopped.", "success")
    
    return

def take_screenshot(logger):
    # pass
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error")
            return
        start_scrcpy_client(logger)
        
        random_text = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=20))

        img = SCRCPY_CLIENT.last_frame
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(img_rgb)
        pil_img.save(f"screenshots/screenshot_{random_text}.png")

        logger(f"Screenshot saved to screenshots/screenshot_{random_text}.png", "success")

        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def unlimited_summons(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, MAX_ATTEMPTS, DELAY
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error")
            return
        start_scrcpy_client(logger)

        logger("") # Logs newline for better readability
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)

        Awakened = []
        Awakened.append(config['Tasks']['Awakened'] if 'Awakened' in config['Tasks'] else "None")
        Awakened.append(config['Tasks']['Awakened 2 (optional)'] if 'Awakened 2 (optional)' in config['Tasks'] else "None")
        Awakened.append(config['Tasks']['Awakened 3 (optional)'] if 'Awakened 3 (optional)' in config['Tasks'] else "None")
        Awakened = [a for a in Awakened if a != "None"]

        Celepog = []
        Celepog.append(config['Tasks']['Celepog'] if 'Celepog' in config['Tasks'] else "None")
        Celepog.append(config['Tasks']['Celepog 2 (optional)'] if 'Celepog 2 (optional)' in config['Tasks'] else "None")
        Celepog.append(config['Tasks']['Celepog 3 (optional)'] if 'Celepog 3 (optional)' in config['Tasks'] else "None")
        Celepog = [c for c in Celepog if c != "None"]

        F4 = []
        F4.append(config['Tasks']['4F'] if '4F' in config['Tasks'] else "None")
        F4.append(config['Tasks']['4F 2 (optional)'] if '4F 2 (optional)' in config['Tasks'] else "None")
        F4.append(config['Tasks']['4F 3 (optional)'] if '4F 3 (optional)' in config['Tasks'] else "None")
        F4.append(config['Tasks']['4F 4 (optional)'] if '4F 4 (optional)' in config['Tasks'] else "None")
        F4.append(config['Tasks']['4F 5 (optional)'] if '4F 5 (optional)' in config['Tasks'] else "None")
        F4 = [f for f in F4 if f != "None"]

        overwrite_on_success = config['Tasks']['Overwrite on success'] if 'Overwrite on success' in config['Tasks'] else "False"
        double_4f = config['Tasks']['Double 4F'] if 'Double 4F' in config['Tasks'] else "False"
        triple_4f = config['Tasks']['Triple 4F'] if 'Triple 4F' in config['Tasks'] else "False"

        unlimited_summons_cycle(DEVICE_ID, SCRCPY_CLIENT, logger, Awakened, Celepog, F4, overwrite_on_success, double_4f)
        stop_scrcpy_client(logger)

    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")


def start_daily_tasks(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, MAX_ATTEMPTS, DELAY
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error")
            return
        start_scrcpy_client(logger)

        logger("") # Logs newline for better readability
        
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        MAX_ATTEMPTS = int(config['Global']['Max Attempts'])
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)

        if config['Tasks']['Claim AFK Rewards'] == 'True':
            attempt = 0
            result = False
            logger("Starting claiming AFK rewards...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = claim_afk_rewards(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Claimed AFK rewards!\n", "success") if result else logger("Failed claming AFK rewards.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Campaign Battle'] == 'True':
            attempt = 0
            result = False
            logger("Starting battle in Campaign...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = campaign_battle(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Campaign Battle completed!\n", "success") if result else logger("Campaign Battle failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Claim Fast Rewards'] == 'True':
            attempt = 0
            result = False
            logger("Starting to claim Fast Rewards...", "info")
            amount = int(config['Tasks']['Amount of Fast Rewards'])
            while attempt < MAX_ATTEMPTS and not result:
                result = claim_fast_rewards(DEVICE_ID, SCRCPY_CLIENT, amount, logger)
                attempt += 1
            logger(f"Claimed fast rewards {amount} of time(s)!\n", "success") if result else logger("Claiming fast rewards failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Friendship Points'] == 'True':
            attempt = 0
            result = False
            logger("Starting to claim Friendship Points...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = friendship_points(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Friendship Points claimed!\n", "success") if result else logger("Friendship Points claim failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Loan Mercenaries'] == 'True':
            attempt = 0
            result = False
            logger("Starting to loan Mercenaries...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = loan_mercenaries(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Mercenaries loaned!\n", "success") if result else logger("Mercenaries loan failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Read Mail'] == 'True':
            attempt = 0
            result = False
            delete = True if config['Tasks']['Delete Mail'] == 'True' else False
            logger("Starting to read Mail...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = read_mail(DEVICE_ID, SCRCPY_CLIENT, delete)
                attempt += 1
            logger(f"Mail read{' and deleted' if delete else ''}!\n", "success") if result else logger("Mail reading failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Bounty Board'] == 'True':
            attempt = 0
            result = False
            logger("Starting Bounty Board...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = bounty_board(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Bounty Board completed!\n", "success") if result else logger("Bounty Board failed.\n", "error")
            time.sleep(DELAY)

        # TODO: check last time this task was completed
        if config['Tasks']['Claim 10 weekly Staves (GG)'] == 'True':
            attempt = 0
            result = False
            logger("Starting Claim 10 weekly Staves (GG)...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = claim_weekly_staves(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Weekly Staves claimed!\n", "success") if result else logger("Weekly Staves claim failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Treasure Scramble'] == 'True':
            attempt = 0
            result = False
            logger("Starting Claim Treasure Scramble resources...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = treasure_scramble(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Treasure Scramble resources claimed!\n", "success") if result else logger("Treasure Scramble resources claim failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Arena of Heroes'] == 'True':
            attempt = 0
            result = False
            amount_of_battles = int(config['Tasks']['Amount of Arena Battles'])
            logger("Starting Arena of Heroes task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result, amount = arena_of_heroes(DEVICE_ID, SCRCPY_CLIENT, amount_of_battles, logger)
                amount_of_battles -= amount
                attempt += 1
            logger("Arena of Heroes battles completed!\n", "success") if result else logger("Arena of Heroes battles failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Claim Gladiator Coins'] == 'True':
            attempt = 0
            result = False
            logger("Starting Claiming Gladiator Coins...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = gladiator_coins(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Gladiator Coins claimed!\n", "success") if result else logger("Gladiator Coins claim failed.\n", "error")
            time.sleep(DELAY)  

        if config['Tasks']['Temporal Rift Fountain'] == 'True':
            attempt = 0
            result = False
            logger("Starting Temporal Rift Fountain task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = temporal_rift(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Temporal Rift fountain collected!\n", "success") if result else logger("Temporal Rift fountain failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['King\'s Tower Battle'] == 'True':
            attempt = 0
            result = False
            logger("Starting King's Tower Battle task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = kings_tower(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("King's Tower Battle completed!\n", "success") if result else logger("King's Tower Battle failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Arcane Labyrinth'] == 'True':
            logger("Starting Arcane Labyrinth task...", "info")
            arcane_labyrinth(DEVICE_ID, SCRCPY_CLIENT, logger)
            time.sleep(DELAY)

        if config['Tasks']['Wall of Legends'] == 'True':
            logger("Starting Wall of Legends task...", "info")
            result = wall_of_legends(DEVICE_ID, SCRCPY_CLIENT, logger)
            logger("Wall of Legends new Milestones claimed!\n", "success") if result else logger("No new milestones in Wall of Legends.\n", "success")
            time.sleep(DELAY)

        if config['Tasks']['Store Purchases'] == 'True':
            attempt = 0
            result = False
            amount_of_refreshes = int(config['Tasks']['Amount of Refreshes'])
            logger("Starting Store Purchases...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result, amount = store_purchases(DEVICE_ID, SCRCPY_CLIENT, amount_of_refreshes)
                amount_of_refreshes -= amount
                attempt += 1
            logger("Store Purchases completed!\n", "success") if result else logger("Store Purchases failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Resonating Crystal'] == 'True':
            attempt = 0
            result = False
            logger("Starting Resonating Crystal task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = resonating_crystal(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Resonating Crystal leveled!\n", "success") if result else logger("Not enough resources to level Resonating Crystal.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Hunting Contract'] == 'True':
            attempt = 0
            result = False
            logger("Starting Hunting Contract task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = hunting_contract(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Hunting Contract completed!\n", "success") if result else logger("Hunting Contract failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Guild hunt'] == 'True':
            attempt = 0
            result = False
            logger("Starting Guild hunt task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = guild_hunt(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Guild hunt completed!\n", "success") if result else logger("Guild hunt failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Twisted Realm'] == 'True':
            attempt = 0
            result = False
            logger("Starting Twisted Realm task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = twisted_realm(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Twisted Realm completed!\n", "success") if result else logger("Twisted Realm failed.\n", "error")
            time.sleep(DELAY)

        if config['Tasks']['Oak Inn Gifts'] == 'True':
            attempt = 0
            result = False
            logger("Starting Oak Inn Gifts task...", "info")
            while attempt < MAX_ATTEMPTS and not result:
                result = oak_inn_gifts(DEVICE_ID, SCRCPY_CLIENT)
                attempt += 1
            logger("Oak Inn Gifts claimed!\n", "success") if result else logger("Oak Inn Gifts claim failed.\n", "error")
            time.sleep(DELAY)

        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")
        return

def auto_push_campaign(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        singlestage = True if config['Global']['Copy Singlestage Formations'] == "True" else False
        start_scrcpy_client(logger)

        push_campaign(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts, singlestage)
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_tower(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        push_tower(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_lb(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [0, 4, 6]:
            logger("This task can only be run on Monday, Friday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_lb(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['lb'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_m(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [1, 4, 6]:
            logger("This task can only be run on Tuesday, Friday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_m(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['m'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_w(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [2, 5, 6]:
            logger("This task can only be run on Wednesday, Saturday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_w(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['w'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_gb(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [3, 5, 6]:
            logger("This task can only be run on Thursday, Saturday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_gb(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['gb'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_cel(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [2, 4, 6]:
            logger("This task can only be run on Wednesday, Friday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_cel(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['cel'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def auto_push_hypo(logger):
    try:
        global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, DELAY
        today = datetime.now(timezone.utc).weekday()
        if today not in [3, 5, 6]:
            logger("This task can only be run on Thursday, Saturday, or Sunday.", "error", True)
            return
        
        if not DEVICE_ID:
            connect_emulator(logger)

        if SCRCPY_CLIENT:
            logger("Already running a task. Can't run 2 at the same time.", "error", True)
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        DELAY = int(config['Global']['Delay']) if 'delay' in config['Global'] else 3
        set_delay(DELAY)
        formation_no = int(config['Global']['Copy Formation #']) if 'copy formation #' in config['Global'] else 1
        formation_no = formation_no if formation_no >= 0 and formation_no < 6 else 1
        artifacts = True if config['Global']['Copy Artifacts'] == "True" else False
        start_scrcpy_client(logger)

        done60 = push_hypo(DEVICE_ID, SCRCPY_CLIENT, logger, formation_no, artifacts)
        if done60:
            logger("All 60 battles done... Come back another day!")
            config['Autopush']['hypo'] = "True"
        stop_scrcpy_client(logger)
    except cv2.error:
        logger("Stopped the current action.", "error")
    except Exception as e:
        print(e)
        logger("Something went wrong.", "error")

def stop_action(logger):
    global SCRCPY_CLIENT
    if not SCRCPY_CLIENT:
        logger("No task is currently running.", "info")
        return
    
    logger("Stopping current action...", "info")
    stop_scrcpy_client(logger)