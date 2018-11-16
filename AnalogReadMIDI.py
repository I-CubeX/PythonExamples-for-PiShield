# Python 3 script for sending sensor data as MIDI messages
# via a Jack virtual MIDI port (see http://jackaudio.org) to
# MIDI software like Giada (see https://giadamusic.com)
#

import spidev
import time
import sys
import jack
import math


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


midiOutBuffer = []

client = jack.Client('PiShield')
midi_out = client.midi_outports.register('MidiOut')

@client.set_process_callback
def process(frames):
    midi_out.clear_buffer()
    if (len(midiOutBuffer)):
        for msg in midiOutBuffer:
            midi_out.write_midi_event(0, msg)
        midiOutBuffer.clear()

client.activate()


NUM_SAMPLES = 10
triggered = [False for i in range(NUM_CH)]
velocity = [0 for i in range(NUM_CH)]
values = [[0 for i in range(NUM_SAMPLES)] for j in range(NUM_CH)]

# send a NoteOn message when a tap gesture is detected and
# map its intensity to velocity using an I-CubeX Touch or similar sensor
def peakTrigger(chan, value, end):
    if (value > 10): # threshold to prevent false triggering
        if not triggered[chan]: # look for trigger
          sumValues = 0
          sumNum = 0
          maxValue = 0
          trigger = False
          for i in range(NUM_SAMPLES - 1, 0, -1):
             if (values[chan][i] > 0):
                 sumValues += values[chan][i]
                 sumNum += 1
             if ((i > 0) and (values[chan][i - 1] <= values[chan][i]) and (values[chan][i] > 0)):
                 trigger = True;
          if (trigger): # trigger MIDI NoteOn with average peak mapped to velocity
              #velocity[chan] = (sumValues / sumNum) * 127 / 1023 # linear
              velocity[chan] = math.pow((sumValues / sumNum), 2) / math.pow(1023, 2) * 127 # power
              if (round(velocity[chan]) > 0):
                  print("\nsensor[%d].velocity = " % chan, round(velocity[chan]), values[chan])
                  midiOutBuffer.append((144, 64 + chan, round(velocity[chan])))
                  triggered[chan] = True
    else: 
        if triggered[chan] and end: # send a MIDI NoteOn with zero velocity, ie. a NoteOff
            velocity[chan] = 0
            print("\nsensor[%d].velocity = " % chan, round(velocity[chan]))
            midiOutBuffer.append((144, 64 + chan, 0))
        triggered[chan] = False

# send ControlChange message whenever the value changes of
# an I-CubeX Push, Slide, Turn or similar sensor 
def changeContinuous(chan, val):
    #val = 0.7 * values[chan][1] + 0.3 * val # smoothing filter
    controlValue = round(val * 127 / 1023)
    if (controlValue != round(values[chan][1] * 127 / 1023)):
        midiOutBuffer.append((176, chan, controlValue)) # send ADC value as Control Change message
        print("\nsensor[%d].control = " % chan, controlValue)
            

while True:
   try:
      time.sleep(0.01) # 100 hz output; change as needed
      for ch in range(0, NUM_CH):
         val = readADC(ch)
         adcValues[ch] = val
         for i in range(NUM_SAMPLES - 1, 0, -1):
            values[ch][i] = values[ch][i - 1]
         values[ch][0] = val
         if (ch == 0):
             peakTrigger(ch, val, True) 
         elif (ch == 1):
             changeContinuous(ch, val)            
      #print("ADC Values = ", adcValues)
   except KeyboardInterrupt:
      break

print("\n\ngoodbye.")

