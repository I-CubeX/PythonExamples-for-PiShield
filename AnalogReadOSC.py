import spidev
import time
import os
import OSC

IP_ADDR='192.168.1.153'
PORT=7000
MSG_ADDR='/ICubeX/analog'

oscSender = OSC.OSCClient()
oscSender.connect((IP_ADDR,PORT))
oscMsg = OSC.OSCMessage()


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
      time.sleep(0.02) #50 hz output
      oscMsg.clear()
      oscMsg.setAddress(MSG_ADDR)
      for ch in range(0,7):
         val = readADC(ch)
         adcValues[ch] = readADC(ch)
         oscMsg.append(val)
      print "ADC Values = ", adcValues
      oscSender.send(oscMsg) 
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."

