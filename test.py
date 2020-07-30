# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.


import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)

pixels[0] = (255, 0, 0)