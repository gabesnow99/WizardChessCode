import sys

if __name__ != '__main__':
    print("__name__ != '__main__'\nNo script.py code was executed")
    sys.exit()

from support import *
from python_prototype import *
from graphics import *
# import GUI #NOTE LEAVE AS import to preserve namespace errors with Piece class etc
import serial
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200
SER = None #serial.Serial(SERIAL_PORT, BAUD_RATE)
    
cls()

######################################################## FOR ARDUINO ################################################################
def connect_to_Penny():
    print(f'connecting to {SERIAL_PORT}... ', end='')
    timeout = 1000
    while True:
        if SER.is_open:
            break
        time.sleep(10)
        timeout -= 1
        if timeout <= 0:
            print('Timeout error: no connection to penny found.')
            sys.exit()
    print('connected!')
    data = b''
    while True:
        if SER.in_waiting > 0:
            data = SER.read(SER.in_waiting)  # Read all available data
            lines = data.decode('utf-8').split('\r\n')
            for line in lines:
                if line == '' or '@' in line:
                    continue
                print(f'Penny said, "{line}"')
        else:
            time.sleep(1)  # Sleep for 1 second before checking again. Sometimes fixes strange behavior
        if b'@' in data: # @ is the last byte character Penny will send before beginning loop() executions 
            break

def tell_Penny(string: str, loud: bool = True):
    if loud: print(f'Hey Penny! {string}') #TODO We should move this to the move_piece() when we are done testing so we say Hey Penny A1 to D4
    a_secret = bytes(string, 'utf-8')
    SER.write(a_secret)

def wait_for_code(code, timeout=30, loop=.1):
    code = code
    start_time = time.time()
    data = b''
    while True:
        if SER.in_waiting > 1:
            data = SER.read(SER.in_waiting)
            data = data.decode('utf-8')
            if code in data:
                return
        if time.time() - start_time > timeout:
            print("Timeout: Code not found.")
            return
        time.sleep(loop) # technically not necessary this prevents a "BUSY LOOP" from the CPU consult Gabe on this
        # TODO we should instead of wait for completion, send many waypoints at once, arduino stores each one 
        # ---- to execute in order while sending completion codes as it moves along

def hit_a_home_run_Penny():
    print('Hit a home run, Penny!\n"OKAY!," said Penny.')
    waypoints = [
    '<^0000,0000_19>',
    '<^3000,0000_29>',
    '<^2925,0668_39>',
    '<^2703,1302_49>',
    '<^2345,1870_59>',
    '<^1870,2345_69>',
    '<^1302,2703_79>',
    '<^0668,2925_89>',
    '<^0000,0000_99>'
    ] #'<^0000,3000_09>' is the second to last in the homerun series but right now penny only takes 9 waypoints at a time
    for waypoint in waypoints:
        tell_Penny(waypoint, False)
        wait_for_code('@')
    print('''"I'm aaaall done! :)," said Penny.\nWell done, Penny! Well done.''')

def move_piece_IRL(piece_to_move: str, destination_square: str, is_kill: bool) -> str:
    if is_kill:
        None #TODO HANDLE THE KILL
    #TODO CALL SOME NEW ROUT PLANNER FUNCTION THAT DETERMINES IF ELECTROMAGNET TURNS ON OR OFF
    waypoints = []
    waytpoint = create_waypoint(piece_to_move, destination_square)
    waypoints.append(waytpoint)
    for waypoint in waypoints:
        SER.write(waypoint)
        wait_for_code('@')
        
    return waypoints

def create_waypoint(piece_to_move: str, destination_square: str):
    pos = Position(piece_to_move[0], int(piece_to_move[1]))
    x, y = convert_coord(pos.coordinates['x']), convert_coord(pos.coordinates['y'])
    output = str(x) + str(y)
    pos = Position(destination_square[0], int(destination_square[1]))
    x, y = convert_coord(pos.coordinates['x']), convert_coord(pos.coordinates['y'])
    output += str(x) + str(y)
    output = output.encode('utf-8')

def convert_coord(coord: int) -> str:
    assert isinstance(coord, int), 'coord must be an integer'
    assert coord <= 9999, 'coord is too big'
    assert coord >= 0, 'this function cannot handle negative coords yet'
    if not (coord // 1000 == 0):
        return str(coord)
    elif not (coord // 100 == 0):
        return '0' + str(coord)
    elif not (coord // 10 == 0):
        return '00' + str(coord)
    else:
        return '000' + str(coord)
    
# *********** TEST BLOCKED SHELL ************  
# connect_to_Penny()
# running = True
# print('Penny is listening... be carefule what you tell her.')
# while running:
#     for i in range(4):
#         tell_Penny('<^0000,0000_11>')
#         wait_for_code('@')
#         tell_Penny('<^1000,1000_11>')
#         wait_for_code('@')
#     usr_input = input()
#     if usr_input:
#         running = False
#         hit_a_home_run_Penny()

# input('Enter to close serial communication') # NOTE Something odd happens. if we delete this line Penny restarts everytime after hit_a_home_run_Penny()
# SER.close()
# input('Enter to exit')
# cls()
# print('test complete')
# sys.exit()
# *********** TEST BLOCKED SHELL ************  

######################################################## FOR PYTHON SHELL ################################################################
game = Game()
install_game(game)
messages = []
next_message = ''
# connect_to_Penny()

def printm():
    print('\n')
    for message in messages: print(message)

def add_massage(string: str):
    messages.append(string)

def update_terminal():
    cls()
    show_board(game)
    print(f'# live white pieces:{len(game.live_white_pieces)}')
    print(f'# live black pieces:{len(game.live_black_pieces)}')
    print(f'# dead pieces:{len(game.dead_pieces)}')

update_terminal()

while True:
    is_kill = False
    piece_to_move: str = input('Hit Enter to exit or enter the location of the piece\nyou would like to move: ').upper()
    if not piece_to_move:
        answer: str = input('Are you sure?\nEnter = Yes    Any letter = No\nAnswer: ').upper()
        if not answer:
            break
        while not piece_to_move:
            piece_to_move: str = input('Enter the location of the piece\nyou would like to move: ').upper()
    destination_square: str = input('Hit Enter to exit or enter the location to where you\nwould like to move this piece: ').upper()
    if not destination_square:
        answer: str = input('Are you sure?\nEnter = Yes    Any letter = No\nAnswer: ').upper()
        if not answer:
            break
        while not destination_square:
            destination_square: str = input('Enter the location to where you\nwould like to move this piece: ').upper()
    piece_to_move, destination_square, is_kill= game.move_piece(piece_to_move, destination_square)
    print(piece_to_move, destination_square, is_kill)
    move_piece_IRL(piece_to_move, destination_square, is_kill)
    update_terminal()
    print('PIECE CAPTURED!') if is_kill else None
    if is_kill:
        next_message = piece_to_move.upper() + ' CAPTURED ' + destination_square.upper()
    else:
        next_message = f' {piece_to_move.upper()}   to   {destination_square.upper()}'
    coord1 = [HALF_WALL_LENGTH + WALL_LENGTH * (int(ord(piece_to_move[0].upper()) - ord('A') + 1) - 1), HALF_WALL_LENGTH + WALL_LENGTH * (int(piece_to_move[1]) - 1)]
    coord2 = [HALF_WALL_LENGTH + WALL_LENGTH * (int(ord(destination_square[0].upper()) - ord('A') + 1) - 1), HALF_WALL_LENGTH + WALL_LENGTH * (int(destination_square[1]) - 1)]
    print(coord1, '->', coord2)
    print('    ', next_message)
    add_massage(next_message)

cls()
show_board(game)
printm()
print(game.pgn) #TODO make pgn
input('Hit enter to clear screen...')

######################################################## HANDLE EXIT ################################################################
def file_export():
    with open('Wizzard Chess Results.txt', 'w', encoding='utf-8') as file:
        string = return_txt_board() + '\n\n'
        string += f'# live white pieces: {len(game.live_white_pieces)}\n'
        string += f'# live black pieces: {len(game.live_black_pieces)}\n'
        string += f'# dead pieces: {len(game.dead_pieces)}\n'
        string += '\nMoves:\n'
        for message in messages:
            string += message + '\n'
        string += '\n' + game.pgn #TODO pgn
        for char in string:
            file.write(char)

# SER.close()
file_export()
cls()
