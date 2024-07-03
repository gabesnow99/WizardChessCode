import support

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

def setup_game():
    global ascii_board
    empty_board()
    for i in range(8):
        replace(f'{chr(i + ord("A"))}7', chess_pieces[5])
        replace(f'{chr(i + ord("A"))}2', chess_pieces[11])
    replace('A8', chess_pieces[2])
    replace('H8', chess_pieces[2])
    replace('C8', chess_pieces[3])
    replace('F8', chess_pieces[3])
    replace('G8', chess_pieces[4])
    replace('B8', chess_pieces[4])
    replace('D8', chess_pieces[0])
    replace('E8', chess_pieces[1])

    replace('D1', chess_pieces[6])
    replace('E1', chess_pieces[7])
    replace('A1', chess_pieces[8])
    replace('H1', chess_pieces[8])
    replace('C1', chess_pieces[9])
    replace('F1', chess_pieces[9])
    replace('G1', chess_pieces[10])
    replace('B1', chess_pieces[10])

def print_board():
    support.cls()
    print(ascii_board)

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
  global ascii_board
  for i in range():
      pass
  return board

# setup_game()
# print_board()
