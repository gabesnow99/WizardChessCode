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

INTEGRATED TEST:  (progressively tests all components together)
- Joystick_Integrated_Test
	Uses Stepper.h
	Joystick Controls each axis, one at a time
	Joystick button toggles fast and slow speeds
- Joystick_Integrated_Test_2
	Uses AccelStepper.h	


KNOWN BUGS:
- ALL: Serial Communicator 64th character runs indefinitely
- Joystick_Integrated_Test: Current interrupt is unreliable. Gabe's millis command used to be reliable