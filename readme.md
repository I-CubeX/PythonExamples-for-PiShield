##I-CubeX Raspberry Pi sensor interface: Python Examples

Raspberry Pi Python (2.7 / 3.4+) demo code for getting data from the analog sensors connected to the I-CubeX Pi Shield, with optional OSC sending capability.

Contents:
- AnalogRead8.py: (Python 2) reads 8 channels of analog input, and prints to console.
- AnalogReadMIDI.py: (Python 3) reads 2 channels, and sends them via MIDI to other software (requires JACK-Client).
- AnalogReadOSC.py: (Python 2) same as above, and sends it via OSC to external host (requires pyOSC).
- AnalogReadOSC-SP.py: (Python 3) same as above, and sends it via OSC to local host running Sonic Pi (requires python-osc).
- AnalogReadOSC_max_test.maxpat: Max/MSP patch for testing the OSC functionality.
- KeyboardEmulator: (Python 2) assumes X and Y analog joysticks are plugged into the first 2 channels. maps up/down/left/right to the keyboard keys w/s/a/d, in the style of FPS game controls. The application using it must of course have keyboard focus. Designed to work with the GUI and tested with Minecraft.
- PDFViewerController: (Python 2) adapts KeyboardEmulator example but used to trigger next and previous page commands in XPDF so that the script can be used as an automatic music page turner. Also unlike the previous example, a trigger causes the script to block a while since we're interested in discrete commands, not continous movement.
- TouchMe.py: (Python 2) simple thresholding for ON/OFF of the first analog channel. Designed to work with sensors like the ReachOn capacitive touch that emits a 0 when there is no touch, and a high value when touch is detected. Uses sys.stdin to create a non-scrolling console output.
- TurtleTest.py: (Python 2) Works in the GUI. Uses X and Y input (same as KeyboardEmulator above) to control the drawing of the Python Turtle)

Requirements:
- Raspberry Pi board running Raspbian
- I-CubeX RPi Shield
- Some analog sensors of your choice

Software:
- Raspbian OS set up with SPI\* 
- Python 2.7.x with spidev\*
- Python 3.4+ with spidev
- Max/MSP (optional, for the test demo)
- Python libraries:
  - pyuserinput (install from pip)
  - pyOSC (install from [github](https://github.com/ptone/pyosc)) or python-osc
  - JACK-Client (install from pip)
  

(*these are already included in our pre-configured image, for manual setup instructions, check out our product page for details and tutorials)

The following shows the python sketch running on the Raspberry Pi (via ssh) communicating with the Max patch on a different computer:


![gif demo](https://j.gifs.com/qxZgAp.gif)

Tested setup: RPi2 running Raspbian Jessie, but should work with other versions as well as long as software and hardware has been configured.
