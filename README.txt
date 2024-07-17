*Folders in repository are in full caps
*Sub Folders (including only the sketch file) are listed as bullet points
*Sketch file attributes are listed one indent inside each corresponding subfolder

[REPO MAP]
FINAL CODE:
- final_BETA
	- This is the offical BETA test
	- OPERATIONS: setup(), homingSequence, loop()
	- loop(): constantly reads in serial. if serial packet is validated it runs that code. repeats
	- the codes sent in are waypoints which also update the electromagnet
	- Communication from serial comes via python
- final_R1.0
	- Operations: setup, home carriage, moves carriage based on joystick input
	- edited, slightly consolidated, and improved from Electromagnet_integrated_test_2
	- Interrupts are attached to pins 2 and 3 and ISR works properly
	- PennyGoHome function works within a new main::function declared in Arduino's main.cpp 
	- IDE MODIFICATION REQUIERED: a slight change to main.cpp enables homingSequence() to operate
	- A copy of this file is located in the root folder named "modifiedMain.cpp"
	- example destination: "C:\Users\joshu\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.5\cores\arduino\main.cpp"
- final_R1.1
	- Operations: setup, home, moves carriage based on joystick input, pressing button updates available serial 11-byte coordinates and moves carriage accordingly
	- Derived from final_R1.0
	- ReadSerial() function added. Reads in 9 bytes to form 2 4-byte coordinates
	- Able to move from coordinate to coordinate with nonblocking functions
- final_R1.2
	- Derived from R1.1
	- Test Accuracy of motors
- final_R1.3
	- Derived from R1.2 AND python_prototype.py, test_script.py from the Isolated Tests/collision_detection folder
	- A virtual board is created mapped to the carriage's range
	- Serial communication reads in the parameters for moveTo() (i think thats that function... not sure) 
	- move_piece() moves the carriage from one square to another on the board
	- edited UpdateElectromagnet arugument to a Boolean
	- #include Chess.h from the same folder (TODO: rename to Piece.h and create more header files with other functions to clear up readability
	- #include Definitions.h which has a reference chess board showing corresponding index numbers to each square and all #define pieces

ISOLATED TEST:  (test individual components)
- collision detection
	- WILL USE serial communication to predict the quickest path from two squares while avoiding other pieces
	- WILL be an edit from from the final_R1.0 file and WILL contribute to final_R1.1, eventually
	- PYTHON PROTOTYPE: Graphically displays pieces and moves them, storing their locations and lists of live White/Black pieces, and dead pieces.
- full_gantry_test
	- Uses stepper.h
	- Uses serial command line to move each axis
- joystick_test
	- Print input variables from joystick in serial line
- serial_test
	- turns on led when reading serial
	- displays ACSII values from serial
- serial_test_2
	- Able to read two 4-byte coordinates into an array
- stepper_test
	- Uses stepper.h
	- Tests one stepper motor at time
- electromagnet_test
	- blinks LED and electromagnet

INTEGRATED TEST:  (progressively tests all components together)
- Joystick_Integrated_Test
	- Uses Stepper.h
	- Joystick Controls each axis, one at a time
	- Joystick button toggles fast and slow speeds
	- BUG: interrupt is not reliable. less preferred isButtonPushed used instead
- Joystick_Integrated_Test_2
	Uses AccelStepper.h
- Electromagnet_Integrated_Test
	- Uses Joystick to move EM
	- Button engages the EM
	- Includes limit switch action too
	- BUG: Semi-functional limit switch commands needs to be edited
	- BUG: interrupt is not reliable. less preferred isButtonPushed used instead 
- Electromagnet_Integrated_Test_2
	- Uses the AccelStepper.h library which enables both steppers to run simultaneously more smoothly  
	- Uses Joystick to move EM
	- Button engages the EM
	- Includes limit switch action too
	- BUG: Semi-functional limit switch command needs to be edited

