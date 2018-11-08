import turtle;
import spidev
import time


#############################
# TurtleTest.y
#
# uses the first two analog input channels to control the position of the
# turtle. use in a windowing environment with an IDE like IDLE
#
#

NUM_CH = 8

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000 # required for Raspbian Stretch

def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val

adcValues = [0 for i in range(8)]



turtle.forward(10);
while 1:
   try:
      time.sleep(0.1) #10 hz output
      for ch in range(0,7):
        adcValues[ch] = readADC(ch)
        if adcValues[1] < 200:
            print "UP!"
            turtle.forward(2)
        if adcValues[1] > 700:
            print "DOWN!"
            turtle.backward(2)
        if adcValues[0] < 200:
            print "LEFT!"
            turtle.setheading(turtle.heading()+2.5)
        if adcValues[0] > 700:
            print "RIGHT!"
            turtle.setheading(turtle.heading()-2.5)
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."


