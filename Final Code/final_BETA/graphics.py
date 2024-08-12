#NOTES: Segoe UI Symbol is the terminal font that removes the purple pawn curse. But it does ruin normal character spacing

from python_prototype import *

ASCII_BOARD_TEMPLATE = '''  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗
8 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
7 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
6 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
5 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
4 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
3 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
2 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
1 ║   │   │   │   │   │   │   │   ║
  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝
    A   B   C   D   E   F   G   H'''
CHESS_PIECES = ['♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟']

DEFAULT_GAME = ''
ascii_board = ASCII_BOARD_TEMPLATE

def install_game(game_to_instal: Game):
  global DEFAULT_GAME
  DEFAULT_GAME = game_to_instal
  print(DEFAULT_GAME.board_data())

def empty_board(game: Game = DEFAULT_GAME):
    global ascii_board
    ascii_board = ASCII_BOARD_TEMPLATE
    game.clear_off_pieces()


def find_square(string: str) -> int:
    col = ord(string[0].upper()) - ord('A') + 1
    row = 9 - int(string[1])
    index = 36 + 72 * (row - 1) + 4 * col
    return index 

def replace(square: str, new_char: str):
    global ascii_board
    index = find_square(square)
    ascii_board = ascii_board[:index] + new_char + ascii_board[index + 1:]

def read_in_board(data: str):
  global ascii_board
  ascii_board = ASCII_BOARD_TEMPLATE
  assert isinstance(data, str), 'read_in_board requires a string'
  for i in range(0, len(data), 4):
      replace(f'{data[i]}{data[i + 1]}', CHESS_PIECES[int(data[i + 2]) * 10 + int(data[i + 3])])

def show_board(game: Game = DEFAULT_GAME):
    read_in_board(game.board_data())
    print(ascii_board)

def return_board(game: Game = DEFAULT_GAME):
    read_in_board(game.board_data())
    return ascii_board

def return_txt_board(game: Game = DEFAULT_GAME):
    global ascii_board
    read_in_board(game.board_data())
    big_count =  0

    # Convert string to list of characters
    ascii_board_list = list(ascii_board)
    
    for i, rank in enumerate('87654321'):
        lil_count = 0
        for j, file in enumerate('ABCDEFGH'):
            index = find_square(file + rank)
            char = ascii_board[index]
            if char == ' ':
                lil_count += 1
                if lil_count % 5 != 0:
                    ascii_board_list.insert(index + big_count - 1, '\u0020')
                    big_count += 1
    for i in range(28, -1, -4):
        ascii_board_list.insert(-i - 1, ' ')

    # Convert list back to string
    ascii_board_modified = ''.join(ascii_board_list)
    return ascii_board_modified
