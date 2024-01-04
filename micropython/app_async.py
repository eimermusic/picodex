from time import time, sleep, localtime, mktime
import ntptime
import uasyncio as asyncio
import framebuf
from upydexcom import Dexcom
from config import cfg
from display import oled
import wifi
import logging

from const import (
    DEXCOM_TREND_SYMBOLS,
    BIG_NUMBER_SYMBOLS,
    TIMER_RECTS,
)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create file handler and set level to error
    file_handler = logging.FileHandler("error.log")
    file_handler.setLevel(logging.WARNING)
    # Create a formatter
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")
    # Add formatter to the handlers
    file_handler.setFormatter(formatter)
    # Add handlers to logger
    logger.addHandler(file_handler)

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

def showRects(elapsed):
    i = 1
    while i <= (elapsed//60):
        r = TIMER_RECTS.get(i)
        if r:
            print(r)
            oled.fill_rect(r[0], r[1], r[2], r[3], 1)
        i += 1

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

def format_local_time_diff(lt):
    return "{:02d}:{:02d}".format(lt[4], lt[5])

def format_local_datetime(lt):
    return "{}-{}-{} {}:{}:{}".format(lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])


class DisplayData:
    mmol_l: string = ""
    trend: int = 0
    delta: string = ""
    latest_time: time = time()
    
    def latest_is_old():
        # Is the latest reading old?
        old_threshold = time()-10*60
        return int(latest_time) < old_threshold


async def dexcom_fetcher(data: DisplayData):
    sleep_interval = 300

    oled.fill(0)
    oled.text("Dexcom login...", 0, 24)
    oled.show()
    dexcom = Dexcom(cfg['dexcom_username'], cfg['dexcom_password'], ous=True)
    oled.fill(0)
    oled.text("Loading CGM Data", 0, 24)
    oled.show()

    while True:
        #try:

        # Get glucose readings
        readings = dexcom.get_glucose_readings(max_count=2)
        latest = readings[0]
        previous = readings[1]
        
        # Current value
        data.mmol_l = '{:.1f}'.format(latest.mmol_l)
        data.trend = latest.trend
        # Change from previous value
        data.delta = '{:+.1f}'.format(latest.mmol_l - previous.mmol_l)
        # Time of current value
        data.latest_time = latest.time


        time_passed = time() - int(latest.time)
        interval = 305 - time_passed
        print(f"localtime: {format_local_datetime(localtime())}")
        print(f"eventtime: {format_local_datetime(localtime(int(latest.time)))}")
        print(f"passed: {time_passed}, interval: {interval}")
        sleep_interval = interval if interval > 9  else 10
        #except:
        #    print("caught unknown error")
        #    log.exception("Dexcom fetch Unknown error")
        #    sleep_interval = 60
        
        print(f"sleeping for: {sleep_interval}")
        await asyncio.sleep(sleep_interval)
    return None


async def display_updater(data):
    sleep_interval = 5

    while True:

        if not data.mmol_l:
            print("nothing to display, sleeping")
            await asyncio.sleep(sleep_interval)

        # render to screen
        oled.fill(0)
        integer, decimal_char = data.mmol_l.split(".")
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

        trend_symbol = get_trend_symbol(data.trend)
        oled.blit(trend_symbol, 92, 4)

        # lower text
        old_threshold = time()-10*60
        if int(data.latest_time) < old_threshold:
            oled.text("OLD", 52, 44)
            oled.rect(0, 0, 128, 64, 1)
            oled.rect(1, 1, 126, 62, 1)

        oled.text(format_local_time(cettime(int(data.latest_time))), 4, 44)
        oled.text(data.delta, 92, 44)

        time_passed = time() - int(data.latest_time)
        showRects(time_passed)
#         time_passed_f = format_local_time_diff(localtime(time_passed))
#         oled.text(time_passed_f, 4, 44)

        oled.show()


        interval = 305 - time_passed
        print(f"localtime: {format_local_datetime(localtime())}, eventtime: {format_local_datetime(localtime(int(data.latest_time)))}")
        print(f"passed: {time_passed}, interval: {interval}")
        #except:
        #    print("caught unknown error")
        #    sleep_interval = 60
        
        await asyncio.sleep(sleep_interval)
    return None


async def rerun_on_exception(coro, *args, **kwargs):
    while True:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            # don't interfere with cancellations
            raise
        except Exception:
            print("Caught exception")
            logging.exception("Task exception")
            oled.fill(0)
            oled.text("ERROR ERROR", 0, 32)
            oled.show()
            raise






setup_logging()

# connect to wifi
wifi.connect()

# shared data
data = DisplayData()

async def main():
    ntptime.settime()
    dexcom_task = asyncio.create_task(rerun_on_exception(dexcom_fetcher, data))
    display_task = asyncio.create_task(rerun_on_exception(display_updater, data))
    await asyncio.sleep(0)
    print('both tasks running')
    await dexcom_task
#     await display_task
    print('All done')

asyncio.run(main())

