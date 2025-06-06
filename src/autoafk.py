from adbauto import *
from utils import check_afk_running

device_id = get_emulator_device()

if check_afk_running(device_id) == None:
    print()
