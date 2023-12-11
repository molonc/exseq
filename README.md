# exseq
This repository contains the code and design parts for the new expansion microscopy setup at the Aparicio Lab.

The 'Peristaltic Pump Code' folder contains python files that can be used in order to run the perstaltic pump. 

The folder named "mechanical_components" contains all the solidworks part files used for developping the shaker used in the expansion microscopy setup. It also contains part files from older versions of the designs. The parts available in this folder can be used as a reference.

"Print 1" contains the STL files and drawings for the four components printed for the first time (small clamp, large clamp, platform, and servomotor mount).

The folder "key_mechanical_components" contains the parts that I am continuing to modify in order to optimize the design (as well as the assembly showing how all the parts fit together.)

"Potential Platforms" contains part files for possible platforms to use for the shaker (they are all thorr labs components).

The "Boyden Lab Code" contains code from the Boyden for controlling their instruments when carrying out expansion microscopy. All of their code was written in Matlab.

Testing_servo.m contains code for controlling the servo motor angles.

Maybe_servoexseq.py contains code for controlling the shaker component in the expansion sequencing setup.

The "Working exSEQ code" contains the most current code that works with the exSeq Instrumentation. The main file is "fluidics.py" and it is dependent on the other python files. The "Python_Interpreter.cpp" and "Python_Interpreter.ino" are what is loaded onto the arduino so that it can recieve commands from the python and know what to do with it; either of these two files can be loaded onto the arduino since cpp and arduino are essentially the same. 
