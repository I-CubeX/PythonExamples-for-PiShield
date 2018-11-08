import spidev
import time
import sys

NUM_CH = 8 #max number of channels of ADC

# SPI device
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000 # required for Raspbian Stretch

###################
# ADC read function
###################
def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val

##############
# Program loop
##############
while 1:
   try:
      time.sleep(0.1) #10 hz output
      adcValue = readADC(0)
      msgStr = " Touch is "
      if (adcValue > 500) :
         msgStr+= "ON"
      else:
         msgStr+= "OFF"
      sys.stdout.write("\r\x1b[K" + "ADC Value = " + str(adcValue)+ msgStr)
      sys.stdout.flush()
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."

