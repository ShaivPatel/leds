import time
from neopixel import *
import argparse
from music.visualization import boot_visualize, close_visualize, update_visualize
from music.microphone import close_stream
import threading

# LED strip configuration:
LED_COUNT      = 300   # Number of LED pixels.
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

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

    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


class Controller:

    def __init__(self, led_pin, led_brightness):

        self.LED_PIN = led_pin
        self.LED_BRIGHTNESS = led_brightness
        self.strip = Adafruit_NeoPixel(LED_COUNT, self.LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.requests = []
        self.status = 'Off'

    def run(self):

        colorWipe(self.strip, Color(0, 0, 0), 10)

        print('controller running')
        while True:
            if len(self.requests)>0:
                request=self.requests.pop(0)
                print('new request received: %s' % str(request))
                self.switchTo(request)

            if self.status == 'Strand Test':
                rainbow(self.strip,5)
                if len(self.requests)==0:
                    rainbowCycle(self.strip,5)
                if len(self.requests)==0:
                    theaterChaseRainbow(self.strip,5)
            elif 'Music' in self.status:
                update_visualize()
            else:
                colorWipe(self.strip, Color(0, 0, 0), 1)



    def switchTo(self, selection: int):

        if selection == '1':
            self.status = 'Strand Test'
            print('Strand selected.')

        elif selection == '2':
            self.status = 'Music - Scroll'
            print('Scroll selected.')
            close_visualize()
            boot_visualize('scroll', self.strip)
        elif selection == '3':
            self.status = 'Music - Energy'
            print('Energy selected.')
            close_visualize()
            boot_visualize('energy',self.strip)
        elif selection == '4':
            self.status = 'Music - Spectrum'
            print('Spectrum selected.')
            close_visualize()
            boot_visualize('spectrum', self.strip)
        else:
            self.status = 'Off'
            print('Turning lights off.')
            colorWipe(self.strip, Color(255,0,0), 10)
            colorWipe(self.strip, Color(0,255,0), 10)
            colorWipe(self.strip, Color(0,0,255), 10)
            colorWipe(self.strip, Color(0,0,0), 10)



