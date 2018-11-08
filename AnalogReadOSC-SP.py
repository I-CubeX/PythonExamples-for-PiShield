# Python 3 script for sending sensor data as OSC messages
# to Sonic Pi (see https://sonic-pi.net).
#
# To trigger sounds with a Touch sensor, enable OSC in Sonic
# Pi preferences and use eg. this Sonic Pi script:
#
# triggered = false
# live_loop :foo do
#   use_real_time
#   s0, s1, s2 = sync "/osc/ICubeX/analog"
#   if s0 > 100 and not triggered
#     a = 64
#     b = s1 * 127 / 1023
#     c = s2 * 127 / 1023
#     synth :prophet, note: a, cutoff: b, sustain: c
#     triggered = true
#   else
#     if s0 < 10
#       triggered = false
#    end
#   end
# end

import spidev
import time
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import sys

HOST = "127.0.0.1" # localhost; change as needed
PORT = 4559 # OSC port Sonic Pi that listens to; change as needed
MSG_ADDR = '/ICubeX/analog' # change as needed


NUM_CH = 8
adcValues = [0 for i in range(NUM_CH)]

spi = spidev.SpiDev() #init SPI device
spi.open(0,0)         #open SPI port 0
spi.max_speed_hz = 1000000 # required for Raspbian Stretch

def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default=HOST,
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=PORT,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)


while 1:
   try:
      time.sleep(0.01) # 100 hz output; change as needed
      for ch in range(0, NUM_CH):
         val = readADC(ch)
         adcValues[ch] = readADC(ch)
      print("ADC Values = ", adcValues)
      client.send_message(MSG_ADDR, adcValues)
   except KeyboardInterrupt:
      break

print("\n\ngoodbye.")

