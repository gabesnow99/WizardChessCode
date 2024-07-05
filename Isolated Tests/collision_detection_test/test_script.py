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
    piece_to_move = input('Please enter the location of the piece\nyou would like to move: ')
    if not piece_to_move:
        break
    move_piece(piece_to_move, input('Please enter the location to where you would like to move this piece: '))
    show_board()

cls()
