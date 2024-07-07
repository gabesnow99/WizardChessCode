from support import *
from python_prototype import *
from graphics import *

cls()

######################################################## FOR PYTHON SHELL ################################################################

messages = []

def printm():
    for message in messages: print(message)

def add_massage(string: str):
    messages.append(string)

while True:
    piece_to_move: str = input('"Hit Enter" to exit or enter the location of the piece\nyou would like to move: ')
    if not piece_to_move:
        break
    destination_square: str = input('"Hit Enter" to exit or enter the location to where you\nwould like to move this piece: ')
    if not destination_square:
        break
    move_piece(piece_to_move, destination_square)
    add_massage(piece_to_move.upper() + ' to ' + destination_square.upper())
    show_board()
    input('Hit enter to make next move...')
    cls()

cls()
printm()
show_board()
input('Hit enter to clear screen...')

cls()
