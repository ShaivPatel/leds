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



def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):

        whitepixels = []
        while len(whitepixels) < 5:
            pixel = randint(0,strip.numPixels())
            if pixel not in whitepixels:
                whitepixels.append(pixel)


        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            if i in whitepixels:
                strip.setPixelColor(i,Color(50,50,50))


        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""

    for i in range(strip.numPixels()):

        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def clear(strip):

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))

def snake(strip= None, strips = (), length = 10, wait_ms=50):

    if strip is not None:
        strips = (strip)

    for i in range(strips[0].numPixels() - length):
        clear(strip1)
        clear(strip2)
        for j in range(length):
            pixel = i+j
            color = wheel(pixel%256)
            for strip in strips:
                strip.setPixelColor(pixel, color)


        for strip in strips:
            strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # # Create NeoPixel object with appropriate configuration.
    # strip1 = StripSegment(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, 0, 139)
    # strip2 = StripSegment(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, 140, 299)
    # # Intialize the library (must be called once before other functions).
    # strip1.begin()
    # strip2.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')


    strips = set()
    try:

        for i in range(10):
            strip = StripSegment(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, i*10, i*10+30)
            strip.begin()
            strips.add(strip)

        while True:
            snake(strips = strips, wait_ms=5)



    except KeyboardInterrupt:
        if args.clear:
            for strip in strips:
                colorWipe(strip, Color(0, 0, 0), 3)
