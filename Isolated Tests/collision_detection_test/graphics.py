#NOTES: Segoe UI Symbol is the terminal font that removes the purple pawn curse. But it does ruin normal character spacing

from python_prototype import board_data

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

ascii_board = ASCII_BOARD_TEMPLATE

def empty_board():
    global ascii_board
    ascii_board = ASCII_BOARD_TEMPLATE

def find_square(string: str) -> int:
    col = ord(string[0].upper()) - ord('A') + 1
    row = 9 - int(string[1])
    index = 36 + 72 * (row - 1) + 4 * col
    return index 

def replace(square: str, new_char: str):
    global ascii_board
    i = 0
    index = find_square(square)
    ascii_board = ascii_board[:index] + new_char + ascii_board[index + 1:]

def read_in_board(data: str):
  assert isinstance(data, str), 'read_in_board requires a string'
  empty_board()
  for i in range(0, len(data), 4):
      replace(f'{data[i]}{data[i + 1]}', CHESS_PIECES[int(data[i + 2]) * 10 + int(data[i + 3])])

def show_board():
    read_in_board(board_data())
    print(ascii_board)
