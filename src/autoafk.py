from adbauto import *
from utils import check_afk_running

device_id = get_ldplayer_device()

if check_afk_running(device_id) == None:
    print()
