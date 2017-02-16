import spidev
import time
from pykeyboard import PyKeyboard 

#############################
# KeyboardEmulator.py
# 
# uses thesholding of values on first two analog input channels to control a virtual keyboard for emitting 'w' 's' 'a' 'd' keys
#
# adapted to send 'n' and 'b' keystrokes to control XPDF as a music page turner

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

# does a quick read to get rid of successive high values
# that may be present for a given gesture event
def purgeADC(ch):
   for i in range(0,2):
      adcValues[ch] = readADC(ch)
      time.sleep(0.01)

adcValues = [0 for i in range(0,NUM_CH)]

armADC = True

while 1:
   try:
      time.sleep(0.1) #10 hz output
      if armADC:
         for ch in range(0,NUM_CH):
           adcValues[ch] = readADC(ch)
           print adcValues[0], adcValues[1]
           if adcValues[0] > 250:
               print "Next Page!"
               kbd.press_key('n')
               kbd.release_key('n')
               time.sleep(1.5) #blocking sleep; not elegant but 
               purgeADC(0)
 
           if adcValues[1] > 200:
               print "Previous Page!"
               kbd.press_key('b')
               kbd.release_key('b')
               time.sleep(0.5)
               purgeADC(1)
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."


