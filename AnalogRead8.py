import spidev
import time

NUM_CH = 8

spi = spidev.SpiDev()
spi.open(0,0)

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
         print "ADC Values = ", adcValues
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."

