# Picodex

## A Dexcom CGM bedroom (or kitchen) display based on the Raspberry Pi Pico W

![Final working Picodex device](https://raw.githubusercontent.com/eimermusic/picodex/main/img/picodex-final.jpg)

## Components

### Raspberry Pi Pico W
[Official website](https://www.raspberrypi.com/products/raspberry-pi-pico/).


### 2.4" 128x64 OLED display
These are sold all over the web under many different brand names. JUst make sure it looks like this:
![OLED Display](https://raw.githubusercontent.com/eimermusic/picodex/main/img/oled-display.jpg)

E.g:
- [Amazon.se #1](https://www.amazon.se/dp/B07QJ4HPV9?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- [Amazon.se #2](https://www.amazon.se/dp/B09Z299L36?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- [Banggood.com](https://www.banggood.com/2_42-inch-7PIN-OLED-Display-LCD-Screen-Module-Resolution-128+64-SPI-or-IIC-Interface-SSD1309-Driver-p-1965615.html?utm_source=googleshopping&utm_medium=cpc_organic&gmcCountry=SE&utm_content=minha&utm_campaign=aceng-pmax-se-en-pc&currency=SEK&cur_warehouse=CN&createTmp=1&ID=6287832&utm_source=googleshopping&utm_medium=cpc_pt&utm_content=meruem&utm_campaign=aceng-pmax-se-all-en-220402-meruem&ad_id=&gclid=EAIaIQobChMIus-ii8zg_gIVF5RoCR1HDADTEAQYAiABEgLEkfD_BwE)

### Obvious tools, bits and bobs
You need some wires, soldering equipment, a computer and so on. Notable you don't actually need a 3D printer. Those can often be found in maker spaces or at some friend's house.. or a commercial printing service.

## Development Setup

![Breadboard development setup](https://raw.githubusercontent.com/eimermusic/picodex/main/img/dev-hardware.jpg)

All development was done on a breadboard, a Pico with headers solder on, and a smaller OLED display with the same resolution.

## Overview of this Repo
This repo is organiced into a few folders for the hardware and software side of things.

- `hardware` contains the stl files for 2 different versions of the case. The V2 case has the USB power connector at the back and is therefore a bit larger. The V3 case has the USP power connector on the right side. Bothn as intended for desk/table use. Not wall mounting.
- `micropython` contains the software that runs the device after installing micropython on the Pico. `config.example.py` is intended to be renamed to `config.py` and should contain your wifi and Dexcom login information.
- `micropython/upydexcom` is a port of the [Pydexcom project](https://github.com/gagebenne/pydexcom) to run on a Micropython device. This is also available as fork called [UPydexcom project](https://github.com/eimermusic/upydexcom)


more to come...
