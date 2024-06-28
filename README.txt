Not sure how these are formatted, Gabe probably knows haha
(do we have a big README or do we need one for each sketch?)

*Folders in repository are in full caps
*Sub Folders (including only the sketch file) are listed as bullet points
*Sketch file attributes are listed one indent inside each corresponding subfolder

[REPO MAP]
FINAL CODE:
- final_R1.0
	- Operations: setup, home carriage, moves carriage based on joystick input
	- edited, slightly consolidated, and improved from Electromagnet_integrated_test_2
	- Interrupts are attached to pins 2 and 3 and ISR works properly
	- PennyGoHome function works within a new main::function declared in Arduino's main.cpp 
	- IDE MODIFICATION REQUIERED: a slight change to main.cpp enables homingSequence() to operate. (a copy of this file is located in the root folder named "modifiedMain.cpp". a name change to "main.cpp" in the correct folder on the compiling machine is required for compilation
- final_R1.1
	- Operations: setup, home carriage, moves carriage based on joystick input, pressing button updates available serial 11-byte coordinates and moves carriage accordingly
	- derived from final_R1.0
	- ReadSerial() function added. Reads in 9 bytes to form 2 4-byte coordinates
	- Able to move from coordinate to coordinate with nonblocking functions

ISOLATED TEST:  (test individual components)
- collision detection
	- WILL USE serial communication to predict the quickest path from two squares while avoiding other pieces
	- WILL be an edit from from the final_R1.0 file and WILL contribute to final_R1.1, evenually
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

