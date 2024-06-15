Not sure how these are formatted, Gabe probably knows haha
(do we have a big README or do we need one for each sketch?)

*Folders in repository are in full caps
*Sub Folders (including only the sketch file) are listed as bullet points
*Sketch file attributes are listed one indent inside each corresponding subfolder

[REPO MAP]
FINAL CODE:
- final_R1.0

ISOLATED TEST:  (test individual components)
- collision detection
	- WILL USE serial communication to predict the quickest path from two squares while avoiding other pieces
- full_gantry_test
	- Uses stepper.h
	- Uses serial command line to move each axis
- joystick_test
	- Print input variables from joystick in serial line
- serial_test
	- Can't remember what this does
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

