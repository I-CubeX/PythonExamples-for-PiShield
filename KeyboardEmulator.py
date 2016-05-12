import spidev
import time
from pykeyboard import PyKeyboard 

#############################
# KeyboardEmulator.py
# 
# uses thesholding of values on first two analog input channels to control a virtual keyboard for emitting 'w' 's' 'a' 'd' keys
#
#

NUM_CH = 2

spi = spidev.SpiDev()
spi.open(0,0)

kbd = PyKeyboard()

def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val

adcValues = [0 for i in range(8)]


while 1:
   try:
      time.sleep(0.1) #10 hz output
      for ch in range(0,7):
        adcValues[ch] = readADC(ch)
        if adcValues[1] < 200:
            print "UP!"
            kbd.press_key('w')
        else:
            kbd.release_key('w')
        if adcValues[1] > 700:
            print "DOWN!"
            kbd.press_key('s') 
        else:
            kbd.release_key('s')
        if adcValues[0] < 200:
            print "LEFT!"
            kbd.press_key('a')
        else:
            kbd.release_key('a')
        if adcValues[0] > 700:
            print "RIGHT!"
            kbd.press_key('d')
        else:
            kbd.release_key('d')
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."


