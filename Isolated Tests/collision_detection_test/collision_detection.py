#ABOUT COLLISION DETECTION: The function g_code() is the function called in other files
#-------------------------- It takes the coordinates the piece needed to move, the destinitation, and is_kill as arguments
#-------------------------- It returns the "G-Code" for where the motors need to move and when the electromagnet needs to activate/deactivate

def gcode(piece: str, destination: str, is_kill: bool) -> str:
    print(f'gcode({piece}, {destination}, {is_kill}) executed!')