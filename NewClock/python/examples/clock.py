#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 57      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

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

def wheel10(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(int((pos * 3)/10), int((255 - pos * 3)/10), 0)
    elif pos < 170:
        pos -= 85
        return Color(int((255 - pos * 3)/10), 0, int((pos * 3)/10))
    else:
        pos -= 170
        return Color(0, int((pos * 3)/10), int((255 - pos * 3)/10))
    
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
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
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
                
def rundown(strip, newHour10,newHour1,newMin10,newMin1):
    for i in range(0,10):
        strip.setPixelColor(i+30,wheel(int((i%10)*255/10)))
        if(newMin1==0):
            strip.setPixelColor(i+20,wheel(int((i%10)*255/10)))
            if(newMin10==0):
                strip.setPixelColor(i+10,wheel(int((i%10)*255/10)))
                if(newHour1==0 or (newHour1==1 and newHour10==0)):
                    strip.setPixelColor(i,wheel(int((i%10)*255/10)))
        strip.show()
        time.sleep(.1)
    for i in range(0,10):
        if(9-i)!= newMin1:
            strip.setPixelColor(9-i+30,Color(0,0,0))
        if(newMin1==0):
            if(9-i)!= newMin10:
                strip.setPixelColor(9-i+20,Color(0,0,0))
            if(newMin10==0):
                if(9-i)!= newHour1:
                    strip.setPixelColor(9-i+10,Color(0,0,0))
                if(newHour1==0 or (newHour1==1 and newHour10==0)):
                    if(9-i)!= newHour10:
                        strip.setPixelColor(9-i,Color(0,0,0))
        strip.show()
        time.sleep(.1)
        
# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')

    try:

        if not True:
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip, Color(0, 0, 255))  # Green wipe
            print ('Theater chase animations.')
            theaterChase(strip, Color(127,0,0))  # White theater chase
            theaterChase(strip, Color(0,127,   0))  # Red theater chase
            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            print ('Rainbow animations.')
            rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)
        colorWipe(strip, Color(0,0,0), 10)    
        t1 = time.localtime()
        
	t1Hour = t1.tm_hour%12
        t1Min = t1.tm_min
        if t1Hour == 0:
            t1Hour = 12
        t1Hour1 = t1Hour%10
        t1Hour10 = int(t1Hour/10)
        t1Min1 = t1Min%10
        t1Min10 = int(t1Min/10)
        for i in range(0,40):
            strip.setPixelColor(i,wheel(int((i%10)*255/10)))
            strip.show()
            time.sleep(.05)
        
        for k in range(40,58):
            strip.setPixelColor(k,wheel(int((k-40)*255/17)))
            strip.show()
            time.sleep(.05)
            
        for j in range(0,58):
            index = 57-j
            if(index == t1Hour10 or index == t1Hour1+10 or index == t1Min10+20 or index == t1Min1 + 30):
                time.sleep(.05)
            else:
                strip.setPixelColor(index,Color(0,0,0))
                strip.show()
                time.sleep(.05)
                
        counter = 0 
        while True:
            t2=time.localtime()
            t2Hour = t2.tm_hour%12
            t2Min = t2.tm_min
            if t2Hour == 0:
                t2Hour = 12
            t2Hour1 = t2Hour%10
            t2Hour10 = int(t2Hour/10)
            t2Min1 = t2Min%10
            t2Min10 = int(t2Min/10)
            
	    late_night = (t2Hour>23) and (t2Hour<6)

            if(t2Min1!=t1Min1):
                rundown(strip,t2Hour10,t2Hour1,t2Min10,t2Min1)
                t1Min1=t2Min1
            else:
                for i in range(0,17):
                    strip.setPixelColor(40+i, wheel10((i*255/17+counter)%255))
                strip.show()
                time.sleep(.01)
                counter+=1
                if(counter==256):
                    counter=0
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)
