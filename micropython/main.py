# main.py -- put your code here!

from machine import reset, Pin, SPI
from ssd1306 import SSD1306_SPI
# from machine import reset, Pin, I2C
# from sh1106 import SH1106_I2C
import framebuf
from time import time, sleep, localtime, mktime
import ntptime
from upydexcom import Dexcom
from config import cfg
import wifi

from const import (
    DEXCOM_TREND_SYMBOLS,
    BIG_NUMBER_SYMBOLS,
)

pix_res_x  = 128
pix_res_y = 64


spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
oled = SSD1306_SPI(pix_res_x, pix_res_y, spi, Pin(17),Pin(20), Pin(16))

# i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
# i2c_addr = [hex(ii) for ii in i2c_dev.scan()] # get I2C address in hex format
# if i2c_addr==[]:
#     print('No I2C Display Found') 
#     sys.exit() # exit routine if no dev found
# else:
#     print("I2C Address      : {}".format(i2c_addr[0])) # I2C device address
#     print("I2C Configuration: {}".format(i2c_dev)) # print I2C params
# oled = SH1106_I2C(pix_res_x, pix_res_y, i2c_dev, res=None, addr=0x3c, rotate=180)

oled.contrast(1)
oled.fill(0)
oled.show()


def load_image(filename):
    with open(filename, 'rb') as f:
        # f.readline()
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

def get_trend_symbol(trend: int):
    filename = DEXCOM_TREND_SYMBOLS[trend]
    return load_image(filename)

def get_big_number(char: str):
    filename = BIG_NUMBER_SYMBOLS[char]
    return load_image(filename)

def cettime(now=time()):
    year = localtime()[0]       #get current year
    HHMarch   = mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    
    if now < HHMarch :               # we are before last sunday of march
        cet=localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=localtime(now+3600) # CET:  UTC+1H
    return(cet)

def format_local_date(lt):
    return "{}-{}-{}".format(lt[0], lt[1], lt[2])

def format_local_time(lt):
    return "{:02d}:{:02d}".format(lt[3], lt[4])

def format_local_datetime(lt):
    return "{}-{}-{} {}:{}:{}".format(lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])

def runloop():
    sleep_interval = 300
    ntptime.settime()

    oled.fill(0)
    oled.text("Dexcom login...", 0, 24)
    oled.show()
    dexcom = Dexcom(cfg['dexcom_username'], cfg['dexcom_password'], ous=True)
    oled.fill(0)
    oled.show()

    while True:
        #try:

        # Get glucose readings
        readings = dexcom.get_glucose_readings(max_count=2)
        latest = readings[0]
        previous = readings[1]

        # Change in past 5min
        delta = '{:+.1f}'.format(latest.mmol_l - previous.mmol_l)

        # Is the latest reading old?
        old_threshold = time()-10*60
        latest_is_old = int(latest.time) < old_threshold
        
        # format display string
        mmol_l = '{:.1f}'.format(latest.mmol_l)

        # render to screen
        oled.fill(0)
        integer, decimal_char = mmol_l.split(".")
        if len(integer) > 1:
            deca = get_big_number(integer[0])
            oled.blit(deca, 4, 4)
            integer = integer[1:]

        single = get_big_number(integer[0])
        oled.blit(single, 28, 4)

        dot = get_big_number(".")
        oled.blit(dot, 52, 4)
        decimal = get_big_number(decimal_char)
        oled.blit(decimal, 62, 4)

        trend_symbol = get_trend_symbol(latest.trend)
        oled.blit(trend_symbol, 92, 4)

        # lower text
        if latest_is_old:
            oled.text("OLD", 52, 52)
            oled.rect(0, 0, 128, 64, 1)
            oled.rect(1, 1, 126, 62, 1)

        oled.text(format_local_time(cettime(int(latest.time))), 4, 44)
        oled.text(delta, 92, 44)
        oled.show()

        time_passed = time() - int(latest.time)
        interval = 305 - time_passed
        print(f"localtime: {format_local_datetime(localtime())}")
        print(f"eventtime: {format_local_datetime(localtime(int(latest.time)))}")
        print(f"passed: {time_passed}, interval: {interval}")
        sleep_interval = interval if interval > 9  else 10
        #except:
        #    print("caught unknown error")
        #    sleep_interval = 60
        
        print(f"sleeping for: {sleep_interval}")
        sleep(sleep_interval)
    return None


# connect to wifi
wifi.connect(oled)
# start polling for CGM data
try:
    runloop()
except TypeError:
    print("Dexcomn API error")
    runloop()
except:
    print("Unknown error, rebooting...")
    oled.fill(0)
    oled.text("UNKNOWN ERROR", 0, 16)
    oled.text("Rebooting...", 0, 40)
    oled.show()

    reset()
