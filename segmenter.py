# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from neopixel import *
import argparse
from random import randint
import threading


# LED strip configuration:
LED_COUNT      = 300    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class StripSegment(Adafruit_NeoPixel):

    def __init__(self, _LED_COUNT, _LED_PIN, _LED_FREQ_HZ, _LED_DMA, _LED_INVERT, _LED_BRIGHTNESS, _LED_CHANNEL, start, end):
        super(StripSegment, self).__init__(_LED_COUNT, _LED_PIN, _LED_FREQ_HZ, _LED_DMA, _LED_INVERT, _LED_BRIGHTNESS, _LED_CHANNEL)
        self.start = start
        self.end = end

    def setPixelColor(self, i, color):
        super(StripSegment, self).setPixelColor(i+self.start, color)

    def numPixels(self):
        return self.end - self.start


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # # Create NeoPixel object with appropriate configuration.
    strip = StripSegment(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, 0, 139)
    # # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            length = input('leds to light?')
            for i in range(300):
                if i <= length:
                    strip.setPixelColor(i,Color(int(255*((i/300)%1)),int(255*((i+100/300)%1)),int(255*((i+200/300)%1))))
                else:
                    strip.setPixelColor(i,Color(0,0,0))

                strip.show()




    except KeyboardInterrupt:
        if args.clear:
            for strip in strips:
                colorWipe(strip, Color(0, 0, 0), 3)
