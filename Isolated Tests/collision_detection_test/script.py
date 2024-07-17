from support import *
from python_prototype import *
from graphics import *
import serial
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200

cls()

# ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print('initializing... *should* be connected!')
# time.sleep(2)
print('wait for homingSequence() to finish!')
# time.sleep(5)
cls()

def send_to_arduino(piece_to_move: str, destination_square: str):
    piece: Piece = board[piece_to_move[0].upper()][int(piece_to_move[1])]
    x, y = convert_coord(piece.x), convert_coord(piece.y)
    output = x + ',' + y
    if is_occupied(destination_square):
        piece: Piece = board[destination_square[0].upper()][int(destination_square[1])]
        x, y = convert_coord(piece.x), convert_coord(piece.y)
    else:
        pos = Position(destination_square[0], int(destination_square[1]))
        x, y = convert_coord(pos.coordinates['x']), convert_coord(pos.coordinates['y'])
    output += f'x{x},{y}'
    output = output.encode('utf-8')
    # ser.write(output)
    return output

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

######################################################## FOR PYTHON SHELL ################################################################
messages = []
next_message = ''

def printm():
    print('\n')
    for message in messages: print(message)

def add_massage(string: str):
    messages.append(string)

def update_terminal():
    cls()
    show_board()
    print(f'# live white pieces:{len(live_white_pieces)}')
    print(f'# live black pieces:{len(live_black_pieces)}')
    print(f'# dead pieces:{len(dead_pieces)}')

def file_export():
    with open('Wizzard Chess Results.txt', 'w', encoding='utf-8') as file:
        string = return_txt_board() + '\n\n'
        string += f'# live white pieces: {len(live_white_pieces)}\n'
        string += f'# live black pieces: {len(live_black_pieces)}\n'
        string += f'# dead pieces: {len(dead_pieces)}\n'
        string += '\nMoves:\n'
        for message in messages:
            string += message + '\n'
        string += '\nPortable Game Notation:\n'
        #TODO pgn
        for char in string:
            file.write(char)

update_terminal()

while True:
    is_kill = False
    piece_to_move: str = input('Hit Enter to exit or enter the location of the piece\nyou would like to move: ').upper()
    if not piece_to_move:
        break
    destination_square: str = input('Hit Enter to exit or enter the location to where you\nwould like to move this piece: ').upper()
    if not destination_square:
        break
    send_to_arduino(piece_to_move, destination_square)
    if move_piece(piece_to_move, destination_square):
        is_kill = True
    update_terminal()
    print('PIECE CAPTURED!') if is_kill else None
    if is_kill:
        next_message = piece_to_move.upper() + ' CAPTURED ' + destination_square.upper()
    else:
        next_message = f' {piece_to_move.upper()}   to   {destination_square.upper()}'
    coord1 = [HALF_WALL_LENGTH + WALL_LENGTH * (int(ord(piece_to_move[0].upper()) - ord('A') + 1) - 1), HALF_WALL_LENGTH + WALL_LENGTH * (int(piece_to_move[1]) - 1)]
    coord2 = [HALF_WALL_LENGTH + WALL_LENGTH * (int(ord(destination_square[0].upper()) - ord('A') + 1) - 1), HALF_WALL_LENGTH + WALL_LENGTH * (int(destination_square[1]) - 1)]
    print(coord1, '->', coord2)
    print('       ', next_message)
    add_massage(next_message)

cls()
show_board()
printm()
print(pgn) #TODO make pgn
input('Hit enter to clear screen...')

# ser.close()
file_export()
cls()
