Not sure how these are formatted, Gabe probably knows haha
(do we have a big README or do we need one for each sketch?)

[REPO MAP]
ISOLATED TEST:  (test individual components)
- full_gantry_test
	Uses stepper.h
	Uses serial commandline to move each axis
- joystick_test
	Print input variables from joystick in serial line
- serial_test
	Can't remember what this does
- stepper_test
	Uses stepper.h
	Tests one stepper motor at time
- electromagnet_test
	blinks LED and electromagnet

INTEGRATED TEST:  (progressively tests all components together)
- Joystick_Integrated_Test
	Uses Stepper.h
	Joystick Controls each axis, one at a time
	Joystick button toggles fast and slow speeds
	BUG: interrupt is not reliable. less preferred isButtonPushed used instead
- Joystick_Integrated_Test_2
	Uses AccelStepper.h
- Electromagnet_Integrated_Test
	Uses Joystick to move EM
	Button engages the EM
	Includes limit switch action too
	BUG: Semi-functional limit switch commands need to be edited
	BUG: interrupt is not reliable. less preferred isButtonPushed used instead
