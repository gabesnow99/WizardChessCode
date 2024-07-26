#ABOUT COLLISION DETECTION: The function g_code() is the function called in other files
#-------------------------- It takes the coordinates the piece needed to move, the destinitation, and is_kill as arguments
#-------------------------- It returns the "G-Code" for where the motors need to move and when the electromagnet needs to activate/deactivate

class Waypoint:

    def __init__(self, x='A', y=1, is_final_point=False):
        self.x = x
        self.y = y
        self.is_final_point = is_final_point

    # CONVERTS WAYPOINT DATA TO STRING FOR SERIAL COMMUNICATION
    def get_as_string(self):
        to_return = self.x
        to_return += str(self.y)
        # to_return += str(int(self.is_final_point))
        return to_return


def gcode(game_board, piece: str, destination: str, is_kill: bool) -> str:
    print(f'gcode({piece}, {destination}, {is_kill}) executed!')
    waypoints: str = ''
    if is_kill:
        handle_the_kill()
    find_direct_route()
    # TODO: ENDPONTS INDICATE LENGTH OF GCODE
    return waypoints

def chart_path(game_board, ):
    pass

def handle_the_kill(): #TODO FINISH THIS FUNCTION
    pass

def find_direct_route(): #TODO FINISH THIS FUNCTION
    find_next_collision()
    pass

def find_next_collision(): #TODO FINDS THE NEXT COLLISON. RETURNS A USEFULL VARIABLE OR RETURNS FALSE IF THERE IS NO OTHER COLLISION
    pass

def create_gcode() -> str: #TODO DETERMINE WHEN THIS SHOULD BE CALLED. RETURNS THE GCODE TO BE READ BY THE ARDUINO
    pass


if __name__=="main":
    a = Waypoint("B", 3)
    b = Waypoint("C", 4)
    print(a.get_as_string())
    print(b.get_as_string())
