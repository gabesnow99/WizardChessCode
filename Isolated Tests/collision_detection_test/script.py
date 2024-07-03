import support #type: ignore
from python_prototype import *
from graphics import *

support.cls()

######################################################## FOR PYTHON SHELL ################################################################

messages = []

def move_piece():
    new_square = input('\nPlease enter the new location: ')
    if new_square == '':
        return True
    support.cls()
    pawn.moveTo(new_square)
    add_massage(f'\nMoved pawn to {new_square}:\n')
    printm()

def printm():
    messages.append(pawn.info)
    for message in messages: print(message)

def add_massage(string: str):
    messages.append(string)

while True:
    start = input('Please enter the starting location: ')
    if start == '':
        break
    support.cls()
    pawn = Piece(start, 'White')
    add_massage(f'pawn is created at: {start}\n')
    printm()

    while True:
        if move_piece():
            break
    break
support.cls()