import spidev
import time
import OSC
import sys

IP_ADDR='192.168.1.153'
PORT=7000
MSG_ADDR='/ICubeX/analog'


#initialize the OSC sender. (make sure server is running on other side at the right IP/PORT
oscSender = OSC.OSCClient()
oscSender.connect((IP_ADDR,PORT))
oscMsg = OSC.OSCMessage()


NUM_CH = 8
adcValues = [0 for i in range(NUM_CH)]

spi = spidev.SpiDev() #init SPI device
spi.open(0,0)         #open SPI port 0

def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val


while 1:
   try:
      time.sleep(0.02) #50 hz output
      oscMsg.clear()
      oscMsg.setAddress(MSG_ADDR)
      for ch in range(0, NUM_CH):
         val = readADC(ch)
         adcValues[ch] = readADC(ch)
         oscMsg.append(val)
      print "ADC Values = ", adcValues
      try:
         oscSender.send(oscMsg) 
      except OSC.OSCClientError:
         print "Error! Unable to connect. Check destination OSC server is running and IP/PORT is correct!\n"
         sys.exit(0)
   except KeyboardInterrupt:
      break

print "\n\ngoodbye."

