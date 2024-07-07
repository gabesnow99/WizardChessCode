#INTEGRATION BUG_PREVENTION: any division need to be done so that results have no remainders and all products are integers
#--------------------------- Therefore, board_height // num_col AND board_height // num_rows needs to be a whole, EVEN number
#--------------------------- Also, board numbers over 9 will cause an error in the is_occupied() function and perhaps serveral other places
#NOTES: Key errors are likely trying to reference squares outside of the board
#------ May not need Piece attribute is_captured
#------ Piece attributes row and col may be switched out for IUAHEIDJYSGUH
#------ In C++ it may be better to have setup_pieces() initialize Piece instances to the board, instead of create a list of live white/black pieces
#------ If we did this, we would also get rid of the piece_code attribute as well
#------ _find_first_char_and_int() private method should not be needed in C++
#------ move_piece() can return values not yet created. This will update memory and the return values will dictate where the motors ACTUALLY go
#------ move_piece() will run collision detection functions based on the arguments passed in. The values from those functions will be the move_piece() return values

from typing import Dict

class Position:
    def __init__(self, col: str, row: int):
        assert isinstance(col, str), 'col type must be str'
        assert len(col) == 1, 'for now col must be A - Z'
        assert isinstance(row, int), 'row type must be int'
        self.coordinates = {'x': self._convert_x(col), 'y': self._convert_y(row)}

    def move_to(self, col: str, row: int):
        self.coordinates['x'] = self._convert_x(col)
        self.coordinates['y'] = self._convert_y(row)

    def _convert_col(self, col: str):
        return int(ord(col.upper()) - ord('A') + 1)
    
    def _convert_x(self, col: str):
        return half_wall_length + wall_length * (self._convert_col(col) - 1)
    
    def _convert_y(self, row: int):
        return half_wall_length + wall_length * (row - 1)

class Piece:
    def __init__(self, square: str, team: str, type: str, piece_code: str = ''):
        assert team == 'W' or team == 'B'
        assert type == 'king' or type == 'queen' or type == 'bishop' or type == 'knight' or type == 'rook' or type == 'pawn', 'piece type not specified'
        assert piece_code == '' or piece_code.isdigit() and piece_code != '9', 'invalid piece_code'
        assert isinstance(square, str), 'square type must be a string'
        self.team = team
        self.type = type
        self.piece_code = piece_code
        self.type_code = self._determine_type(type)
        self.square = self._find_first_char_and_int(square)
        self.is_captured = False
        self._position = Position(self.square[0], int(self.square[1]))
        occupy(self, self.square)

    def move_to(self, square: str):
        square = self._find_first_char_and_int(square)
        unoccupy(self.square)
        self.square = square
        if is_occupied(square):
            kill(square)
        self._position.move_to(self.square[0], int(self.square[1]))
        occupy(self, square)

    def die(self):
        self.is_captured = True
        col = chr(len(dead_pieces) % 8 + ord('A'))
        row = len(dead_pieces)// 8 + 9
        if self.team == 'W':
            dead_pieces[f'W_{self.type}{self.piece_code}'] = live_white_pieces[f'W_{self.type}{self.piece_code}']
            del live_white_pieces[f'W_{self.type}{self.piece_code}']
        else:
            dead_pieces[f'B_{self.type}{self.piece_code}'] = live_black_pieces[f'B_{self.type}{self.piece_code}']
            del live_black_pieces[f'B_{self.type}{self.piece_code}']
        self._position.move_to(col, row)
        self.square = col + f'{row}'

    def _determine_type(self, piece:str):
        type = 0
        if piece == 'king':
            type = 0
        elif piece == 'queen':
            type = 1
        elif piece == 'rook':
            type = 2
        elif piece == 'bishop':
            type = 3
        elif piece == 'knight':
            type = 4
        elif piece == 'pawn':
            type = 5
        if self.team == 'W':
            type += 6
            if type >= 10:
                return str(type)
            return '0' + str(type)
        elif self.team == 'B':
            return '0' + str(type)
    
    def _find_first_char_and_int(self, square: str):
        first_char = None
        first_int = None
        for char in square:
            if char.isalpha():
                if not first_char:
                    first_char = char
            elif char.isdigit():
                if not first_int:
                    first_int = char
            if first_char and first_int:
                break
        if not first_char and not first_int:
            raise ValueError('no col or row was identified')
        if not first_char:
            raise ValueError('no col was identified')
        if not first_int:
            raise ValueError('no row was identified')
        return first_char.upper() + first_int
    
    @property
    def x(self):
        return self._position.coordinates['x']

    @property
    def y(self):
        return self._position.coordinates['y']
    
    @property
    def info(self):
        if self.team == 'W':
            team = 'White'
        if self.team == 'B':
            team = 'Black'
        return print(f'Captured: {self.is_captured}, Team: {team}'
                f'\npawn.x: {self.x}, pawn.y: {self.y}'
                f'\npawn.square: {self.square}')
    
    # @y.setter
    # def y(self, value: int):
    #     self.current_position['y'] = value
    # TODO WHEN MODIFYING A COORDINATE MODIFY COORDINATE AND ROW OR COLUMN
    
    # @x.setter
    # def x(self, value: int):
    #     self.current_position['x'] = value
    # TODO WHEN MODIFYING A COORDINATE MODIFY COORDINATE AND ROW OR COLUMN 

def create_board(num_cols, num_rows):
    board = {}
    for col in range(0, num_cols):
        board[chr(ord('A') + col)] = {}
        for row in range(1, num_rows + 1):
            board[chr(ord('A') + col)][row] = []
    return board

def setup_pieces():
    piecesW = {}
    piecesB = {}
    back_rank = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
    for i in range(8):
        col = chr(ord('A') + i)
        piecesW[f'W_pawn{i + 1}'] = Piece(f'{col}2', 'W', 'pawn', f'{i + 1}')
        piecesB[f'B_pawn{i + 1}'] = Piece(f'{col}7', 'B', 'pawn', f'{i + 1}')
        piece_code = str(1) if i == 0 or i == 1 or i == 2 else ""
        piece_code2 = str(2) if i == 5 or i == 6 or i == 7 else ""
        piecesW[f'W_{back_rank[i]}{piece_code}{piece_code2}'] = Piece(f'{col}1', 'W', f'{back_rank[i]}', piece_code if piece_code else piece_code2)
        piecesB[f'B_{back_rank[i]}{piece_code}{piece_code2}'] = Piece(f'{col}8', 'B', f'{back_rank[i]}', piece_code if piece_code else piece_code2)
    return piecesW, piecesB

def occupy(piece: Piece, square: str):
    assert isinstance(square, str), 'square type must be a str'
    assert len(square) == 2, 'square length must be 2'
    assert square.isupper(), 'no col identified'
    assert square[1].isdigit(), 'no row identified'
    board[square[0]][int(square[1])] = piece

def unoccupy(square: str):
    assert isinstance(square, str), 'square type must be a str'
    assert len(square) == 2, 'square length must be 2'
    assert square.isupper(), 'no col identified'
    assert square[1].isdigit(), 'no row identified'
    board[square[0]][int(square[1])] = []


def is_occupied(square: str):
    assert isinstance(square, str), 'square type must be a str'
    assert len(square) == 2, 'square length must be 2'
    assert square.isupper(), 'no col identified'
    assert square[1].isdigit(), 'no row identified'
    if board[square[0]][int(square[1])]:
        return True
    return False

def kill(square: str):
    board[square[0]][int(square[1])].die()

board_height = 2000 #int(input('Please enter board hieght: '))
num_cols = 8
num_rows = 8
wall_length = board_height // num_rows
half_wall_length = wall_length // 2 
assert isinstance(wall_length, int), "board_height, num_rows, num_cols must all be integers, OR wall_length isn't calculating properly"
assert board_height // num_rows % 2 == 0, "board_height / num_rows AND board_height / num_cols must be even"
board: Dict[str, Dict[int, Piece]] = create_board(num_cols, num_rows)
live_white_pieces: Dict[str, Piece]
live_black_pieces: Dict[str, Piece]
live_white_pieces, live_black_pieces = setup_pieces()
dead_pieces = {}

def board_data():
    data = ''
    for col in board:
        for row in board[col]:
            if board[f'{col}'][row]:
                data += f'{board[f"{col}"][row].square}{board[f"{col}"][row].type_code}'
    return data

def move_piece(piece_from: str, to: str):
    assert isinstance(piece_from, str), 'invalid coordinate'
    assert isinstance(to, str), 'invalid coordinate'
    assert len(piece_from) == 2 and len(to) == 2, 'invalid coordinate'
    assert piece_from[0].isalpha() and to[0].isalpha(), 'invalid coordinate'
    assert piece_from[1].isdigit() and to[1].isdigit(), 'invalid coordinate'
    piece: Piece = board[piece_from[0].upper()][int(piece_from[1])]
    if not piece:
        raise ValueError('There is no piece here')
    if piece.team == 'W':
        live_white_pieces[f'W_{piece.type}{piece.piece_code}'].move_to(to)
    else:
        live_black_pieces[f'B_{piece.type}{piece.piece_code}'].move_to(to)
