import board
import neopixel
import random
import time
import MySQLdb as mariadb
import math
from itertools import chain

PIXEL_PIN	= board.D18
LED_COUNT	= 100
ORDER		= neopixel.RGB
BRIGHTNESS	= 1

leds = neopixel.NeoPixel(PIXEL_PIN, LED_COUNT, brightness=BRIGHTNESS,auto_write=True, pixel_order=ORDER)
leds.fill((0,0,0))
