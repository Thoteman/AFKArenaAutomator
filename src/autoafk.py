# src/autoafk.py
from adbauto import *
from src.tasks import *
from PIL import Image
import cv2
import configparser

DEVICE_ID = ""
SCRCPY_CLIENT = None
CONFIG_PATH = "config.ini"

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
    global DEVICE_ID, SCRCPY_CLIENT
    if not DEVICE_ID:
        logger("No device connected. Please connect to an emulator first.", "error")
        return
    
    if not SCRCPY_CLIENT:
        logger("scrcpy client is not running. Please start it first.", "error")
        return
    
    random_text = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=20))

    img = SCRCPY_CLIENT.last_frame
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img_rgb)
    pil_img.save(f"screenshots/screenshot_{random_text}.png")

    logger(f"Screenshot saved to {f"screenshots/screenshot_{random_text}.png"}", "success")

def start_daily_tasks(logger):
    global DEVICE_ID, SCRCPY_CLIENT, CONFIG_PATH
    if DEVICE_ID:
        logger("Device already connected. Please disconnect from emulator first.", "error")
        return
    
    connect_emulator(logger)

    if SCRCPY_CLIENT:
        logger("scrcpy client is already running. Please stop it first.", "error")
        return
    
    start_scrcpy_client(logger)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    if config['Tasks']['Claim AFK Rewards'] == 'True':
        logger("Starting AFK rewards claim task...", "info")
        claim_afk_rewards(DEVICE_ID, SCRCPY_CLIENT, logger)

    time.sleep(3)

    if config['Tasks']['Campaign Battle'] == 'True':
        logger("Starting Campaign Battle task...", "info")
        campaign_battle(DEVICE_ID, SCRCPY_CLIENT, logger)

    time.sleep(3)
    if config['Tasks']['Claim Fast Rewards'] == 'True':
        logger("Starting Fast Rewards claim task...", "info")
        claim_fast_rewards(DEVICE_ID, SCRCPY_CLIENT, logger)

    stop_scrcpy_client(logger)