import time
from RPLCD import CharLCD
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11])

while True:
    lcd.write_string(u"Hello world!")
    time.sleep(1)
    lcd.clear()
    time.sleep(1)