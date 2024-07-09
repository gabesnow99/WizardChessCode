#ABOUT COLLISION DETECTION: The function g_code() is the function called in other files
#-------------------------- It takes the coordinates the piece needed to move, the destinitation, and is_kill as arguments
#-------------------------- It returns the "G-Code" for where the motors need to move and when the electromagnet needs to activate/deactivate

def gcode(piece: str, destination: str, is_kill: bool) -> str:
    print(f'gcode({piece}, {destination}, {is_kill}) executed!')
    code: str = ''
    if is_kill:
        handle_the_kill()
    find_direct_route()
    return code

def handle_the_kill(): #TODO FINISH THIS FUNCTION
    pass

def find_direct_route(): #TODO FINISH THIS FUNCTION
    find_next_collision()
    pass

def find_next_collision(): #TODO FINDS THE NEXT COLLISON. RETURNS A USEFULL VARIABLE OR RETURNS FALSE IF THERE IS NO OTHER COLLISION
    pass

def create_gcode() -> str: #TODO DETERMINE WHEN THIS SHOULD BE CALLED. RETURNS THE GCODE TO BE READ BY THE ARDUINO
    pass
