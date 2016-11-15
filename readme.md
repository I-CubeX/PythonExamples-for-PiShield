##I-CubeX Raspberry Pi sensor interface: Python Examples

Raspberry Pi Python (2.7) demo code for getting data from the analog sensors connected to the I-CubeX Pi Shield, with optional OSC sending capability.

Contents:
- AnalogRead8.py: reads 8 channels of analog input, and prints to console.
- AnalogReadOSC.py: same as above, and sends it via OSC to external host (requires pyOSC)
- AnalogReadOSC_max_test.maxpat: Max/MSP patch for testing the OSC functionality

Requirements:
- Raspberry Pi board running Raspbian
- I-CubeX RPi Shield
- Some analog sensors of your choice

Software:
- Raspbian OS set up with SPI\* 
- Python 2.7.x, with spidev\*
- Max/MSP (optional, for the test demo)
- Python libraries:
  - pyuserinput (install from pip)
  - pyOSC (install from [github](https://github.com/ptone/pyosc))
  

(*these are already included in our pre-configured image, for manual setup instructions, check out our product page for details and tutorials)

The following shows the python sketch running on the Raspberry Pi (via ssh) communicating with the Max patch on a different computer:


![gif demo](https://j.gifs.com/qxZgAp.gif)

Tested setup: RPi2 running Raspbian Jessie, but should work with other versions as well as long as software and hardware has been configured.
