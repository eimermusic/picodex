
from machine import reset, Pin, SPI, I2C
from ssd1306 import SSD1306_SPI
from sh1106 import SH1106_I2C
import framebuf
import sys
from config import cfg

from const import (
    DEXCOM_TREND_SYMBOLS,
    BIG_NUMBER_SYMBOLS,
)

class Display:
    pix_res_x  = 128
    pix_res_y = 64

    oled: framebuf.FrameBuffer

    def __init__(self, name: str):
        do = f"init_{name}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            self.oled = func()
        else:
            print('Unknown display requested') 
            sys.exit()

        self.oled.contrast(1)
        self.oled.fill(0)
        self.oled.show()


    def init_SH1106_I2C(self):
        i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
        i2c_addr = [hex(ii) for ii in i2c_dev.scan()] # get I2C address in hex format
        if i2c_addr==[]:
            print('No I2C Display Found') 
            sys.exit() # exit routine if no dev found
        else:
            print("I2C Address      : {}".format(i2c_addr[0])) # I2C device address
            print("I2C Configuration: {}".format(i2c_dev)) # print I2C params
        return SH1106_I2C(self.pix_res_x, self.pix_res_y, i2c_dev, res=None, addr=0x3c, rotate=180)


    def init_SSD1306_SPI(self):
        spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
        return SSD1306_SPI(self.pix_res_x, self.pix_res_y, spi, Pin(17),Pin(20), Pin(16))


oled = Display(cfg['display_type']).oled
