#NOTES: Segoe UI Symbol is the terminal font that removes the purple pawn curse. But it does ruin normal character spacing

from python_prototype import board_data

ascii_board = '''  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗
1 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
2 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
3 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
4 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
5 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
6 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
7 ║   │   │   │   │   │   │   │   ║
  ╠───┼───┼───┼───┼───┼───┼───┼───╣
8 ║   │   │   │   │   │   │   │   ║
  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝
    A   B   C   D   E   F   G   H'''
chess_pieces = ['♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟']

def empty_board():
    global ascii_board
    ascii_board = '''  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗
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

def find_square(string: str):
    col = ord(string[0].upper()) - ord('A') + 1
    row = 9 - int(string[1])
    index = 36 + 72 * (row - 1) + 4 * col
    return index 

def replace(square: str, new_char: str):
    global ascii_board
    i = 0
    index = find_square(square)
    new_board = ''
    for char in ascii_board:
        if i == index:
            new_board += new_char
        else:
            new_board += ascii_board[i]
        i += 1
    ascii_board = new_board

def read_in_board(data: str):
  assert isinstance(data, str), 'read_in_board requires a string'
  empty_board()
  for i in range(0, len(data), 4):
      replace(f'{data[i]}{data[i + 1]}', chess_pieces[int(data[i + 2]) * 10 + int(data[i + 3])])

def show_board():
    read_in_board(board_data())
    print(ascii_board)
