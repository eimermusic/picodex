# Picodex

## A Dexcom CGM bedroom (or kitchen) display based on the Raspberry Pi Pico W

![Final working Picodex device](https://raw.githubusercontent.com/eimermusic/picodex/main/img/picodex-final.jpg)

## Components

### Raspberry Pi Pico W
[Official website](https://www.raspberrypi.com/products/raspberry-pi-pico/).


### 2.4" 128x64 OLED display with SPI or I2C interface
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
This repo is organized into a few folders for the hardware and software side of things.

### Hardware
`hardware` contains the stl files for 2 different versions of the case. Both cases print with n supports just fine on my dirt cheap Ender 3 printer using the cheapest PLA I had. The Pico and screen are both fastened using guide-pegs and hot glue so they don't rattle loose over time. The cases are both assembled just by interference fit. No fastners or adhesives needed. The fit is a bit tight but once snapped into place they are not likely to come loose.

![Version 3 case](https://raw.githubusercontent.com/eimermusic/picodex/main/hardware/Picodex%20v3/picodex3.jpg)

The V3 case has the USB power connector on the right side. This is the smaller, easier to both print, and to assemble.

![Version 2 case](https://raw.githubusercontent.com/eimermusic/picodex/main/hardware/Picodex%20v2/picodex2.jpg)

The V2 case has the USB power connector at the back and is therefore a bit larger.

Both cases are intended for desk/table use. No wall mounting case at this time.

(The version 1 case looked like the v2 but with a fully vertical front)

### Micropython
`micropython` contains the software that runs the device after installing micropython on the Pico.

`micropython/upydexcom` is a port of the [Pydexcom project](https://github.com/gagebenne/pydexcom) to run on a Micropython device. This is also available as fork called [UPydexcom project](https://github.com/eimermusic/upydexcom)

## Using this project for your own CGM display
- `micropython/config.example.py` is intended to be renamed to `config.py` and should contain your wifi and Dexcom login information.
- `micropython/main.py` supports two kinds of screen drivers. My small dev screen needed a different driver from the bigger screen used in the final device. Depending on the screen you connect, you may need to comment/uncomment the screen setup near the top of the file. I plan to extract this into more clean import files.



## References

[Pico W Pinout](https://picow.pinout.xyz)
[Pydexcom project](https://github.com/gagebenne/pydexcom)
[Micropython docs](https://docs.micropython.org/en/latest/index.html)
[Micropython "standard" library](https://github.com/micropython/micropython-lib)
[Micropything programming for screens](https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen)
[Display driver SH1106](https://github.com/robert-hh/SH1106)
[Display driver SSD1306 (might actually be shipped with Micropython)](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py)
[Debugging memory usage](https://forum.micropython.org/viewtopic.php?t=3499)
[Huge library of pixelfonts that are good for use with screens like this](https://int10h.org/oldschool-pc-fonts/fontlist/font?ibm_dos_iso8)
[Options for powering the Pico](https://howchoo.com/pi/how-to-power-the-raspberry-pi-pico)





more to come...
