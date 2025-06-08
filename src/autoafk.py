# src/autoafk.py
from adbauto import *

DEVICE_ID = ""

def connect_emulator(logger):
    global DEVICE_ID
    DEVICE_ID = get_emulator_device()
    logger(f"Connected to emulator with device ID: {DEVICE_ID}", "success")

def take_screenshot(logger):
    global DEVICE_ID
    random_text = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=20))
    screenshot_path = f"screenshots/screenshot_{random_text}.png"

    capture_screenshot(DEVICE_ID, screenshot_path)
    logger(f"Screenshot saved to {screenshot_path}", "success")