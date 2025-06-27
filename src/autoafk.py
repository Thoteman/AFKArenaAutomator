# src/autoafk.py
from adbauto import *
from src.tasks import *
from PIL import Image
import cv2
import configparser

DEVICE_ID = ""
SCRCPY_CLIENT = None
CONFIG_PATH = "config.ini"
BACK_BUTTON = (30, 1890)
MAX_ATTEMPTS = 0
DELAY = 0

def connect_emulator(logger):
    global DEVICE_ID
    DEVICE_ID = get_emulator_device()
    logger(f"Connected to emulator with device ID: {DEVICE_ID}", "success")

def start_scrcpy_client(logger):
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

def stop_scrcpy_client(logger):
    global SCRCPY_CLIENT
    if not SCRCPY_CLIENT:
        logger("scrcpy client is not running.", "info")
        return
    
    stop_scrcpy(SCRCPY_CLIENT)
    SCRCPY_CLIENT = None
    logger("Video stream stopped.", "success")
    return

def take_screenshot(logger):
    global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH
    if not DEVICE_ID:
        connect_emulator(logger)

    if not SCRCPY_CLIENT:
        start_scrcpy_client(logger)
    
    random_text = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=20))

    img = SCRCPY_CLIENT.last_frame
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img_rgb)
    pil_img.save(f"screenshots/screenshot_{random_text}.png")

    logger(f"Screenshot saved to screenshots/screenshot_{random_text}.png", "success")

    stop_scrcpy_client(logger)

def start_daily_tasks(logger):
    global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH, MAX_ATTEMPTS, DELAY
    if not DEVICE_ID:
        connect_emulator(logger)

    if not SCRCPY_CLIENT:
        start_scrcpy_client(logger)

    logger("") # Logs newline for better readability
    
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    MAX_ATTEMPTS = int(config['Global']['Max Attempts'])
    DELAY = int(config['Global']['Delay'])
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