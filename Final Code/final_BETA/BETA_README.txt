

_pychache_ folder: Don't touch. It is for the interpreter.

resources folder: for GUI.py

_TEST_SCRIPT.py for early troubleshooting serial communication

collision_detection probably needs to be renamed rout_planner (and then finished)

final_BETA is Penny's little mind

graphics is terminal character graphical display of python_prototype 

GUI is pygame GUI for penny (needs to implement python_prototype.py) NOTE: scale_factor is unique to the system display scale. If there are errors on a different machine, try setting to 1 and switching system display scale to 100% in machine settings. 

python_prototype.py is a prototype game class that will be transferred to .ino when complete (maybe)

script is the file that runs the game and communicates with Penny

support.py is a list of support functions useful in the interpreter for dynamic debugging in the shell

Wizzard chess results are the results of the scripts last game! (when python_prototype starts working again, should add a .json export as well)