import machine
import time
import network
import rp2
from config import cfg

def connect(oled):
    rp2.country('SE')
    print('connecting to')
    print(cfg['wifi_ssid'])

    oled.fill(0)
    oled.text("Connecting to", 0, 16)
    oled.text(cfg['wifi_ssid'], 0, 40)
    oled.show()
    time.sleep(1)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg['wifi_ssid'], cfg['wifi_password'])

    # Wait for connect or fail 12
    max_wait = 30
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        oled.fill(0)
        oled.text("Connecting...", 0, 16)
        oled.text(f"{max_wait}", 0, 40)
        oled.show()
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        # raise RuntimeError('network connection failed')
        print('network connection failed. Rebooting...')
        oled.fill(0)
        oled.text("Connection Error", 0, 16)
        oled.text("Rebooting...", 0, 40)
        oled.show()
        machine.reset()
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        oled.fill(0)
        oled.text("Connected", 0, 16)
        oled.text(status[0], 0, 40)
        oled.show()
        time.sleep(1)
    
    oled.fill(0)
    oled.show()
