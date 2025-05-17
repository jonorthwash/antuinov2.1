# antuinov2.1
Improved antuino software

This is the software for Antuino, an RF lab in a box for radio hams, RF tinkerers. Both the circuit and the software are under GPL, feel free to use them. 

The Antuino is uses an Arduino Nano as its controller. The have to be compiled using the Arduino IDE that is downloadable from www.arduino.cc . Copy all these files into a folder first. It may prompt you to rename the folder, choose 'Yes'. 

IMPORTANT: 
The Antuino uses a modified version of the glcd library. This is included as a zip file in this repository. The Arduino has a simple way to handle libraries - Each library is a sub-folder inside the libraries folder. Download glcd.zip and extract it as 'glcd' folder inside your Arduino's library sub-folder. This will install it as a library in Arduino.

## Serial control

Serial control of the Antuino, using code from [kholia/Antuino-V1](https://github.com/kholia/Antuino-V1/blob/AiO/antuino_analyzer_27mhz_v2/antuino_analyzer_27mhz_v2.ino).

There are several modes.

The `demo/` directory includes the following files:
* [`AntuinoTerm.py`](./demos/AntuinoTerm.py) - lifted mostly from [kholia/Antuino-V1](https://github.com/kholia/Antuino-V1/blob/AiO/src/AntuinoTerm.py), does the serial communications.  Could stand to be rewritten without a `while` loop, but does the job.
* [`analyseAntuino.py`](./demos/analyseAntuino.py) - uses `AntuinoTerm.py` as a library, analyses various amateur bands, and writes to files.  (Will need to create `./logs` directory or specify where to store logs with `--logdir`.)
