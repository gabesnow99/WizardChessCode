#INTEGRATION BUG_PREVENTION: any division need to be done so that results have no remainders and all products are integers
#--------------------------- Therefore, board_height // num_col AND board_height // num_rows needs to be a whole, EVEN number
#--------------------------- Also, board numbers over 9 will cause an error in the is_occupied() function and perhaps serveral other places
#NOTES: Key errors are likely trying to reference squares outside of the board
#------ May not need Piece attribute is_captured
#------ In C++ it may be better to have setup_pieces() initialize Piece instances to the board, instead of create a list of live white/black pieces
#------ If we did this, we would also get rid of the piece_code attribute as well
#------ _find_first_char_and_int() private method should not be needed in C++
#------ move_piece() can return values not yet created. This will update memory and the return values will dictate where the motors ACTUALLY go
#------ move_piece() will run collision detection functions based on the arguments passed in. The values from those functions will be the move_piece() return values

# GABE!! I'M SORRY THIS IS SO MESSY! I HAVE LEARNED TOO MUCH. NOW I KNOW WHY PYTHON IS THE WAY IT IS. AND I THINK YOU WERE RIGHT. WASN'T IT YOU
# WHO SAID WE SHOULD MAKE A GAME CALSS??? I AM SORRY!! YOU KNOW BETTER

from typing import Dict
from collision_detection import gcode

BOARD_HEIGHT = 2000
NUM_COLS = 8
NUM_ROWS = 8
WALL_LENGTH = BOARD_HEIGHT // NUM_ROWS
HALF_WALL_LENGTH = WALL_LENGTH // 2 
assert isinstance(WALL_LENGTH, int), "board_height, num_rows, num_cols must all be integers, OR wall_length isn't calculating properly"
assert BOARD_HEIGHT // NUM_ROWS % 2 == 0, "board_height / num_rows AND board_height / num_cols must be even"

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
        return HALF_WALL_LENGTH + WALL_LENGTH * (self._convert_col(col) - 1)
    
    def _convert_y(self, row: int):
        return HALF_WALL_LENGTH + WALL_LENGTH * (row - 1)

class Piece:
        def __init__(self, game: 'Game', square: str, team: str, type: str, piece_code: str = ''):
            assert team == 'W' or team == 'B'
            assert type in ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn'], 'piece type not specified'
            assert piece_code == '' or piece_code.isdigit() and piece_code != '9', 'invalid piece_code'
            assert isinstance(square, str), 'square type must be a string'
            self.game = game
            self.team = team
            self.type = type
            self.piece_code = piece_code
            self.type_code = self._determine_type(type)
            self.square = self._find_first_char_and_int(square)
            self.is_captured = False
            self.self2 = self
            self._position = Position(self.square[0], int(self.square[1]))
            print(self.square)
            Game._occupy(self.game, self, self.square)

        def move_to(self, square: str):
            square = self._find_first_char_and_int(square)
            Game._unoccupy(self.game, self.square)
            self.square = square
            if Game._is_occupied(square):
                Game._kill(square)
            self._position.move_to(self.square[0], int(self.square[1]))
            Game._occupy(self.game, self, self.square)

        def die(self):
            self.is_captured = True
            col = chr(len(Game.dead_pieces) % 8 + ord('A'))
            row = len(Game.dead_pieces)// 8 + 9
            if self.team == 'W':
                Game.dead_pieces[f'W_{self.type}{self.piece_code}'] = Game.live_white_pieces[f'W_{self.type}{self.piece_code}']
                del Game.live_white_pieces[f'W_{self.type}{self.piece_code}']
            else:
                Game.dead_pieces[f'B_{self.type}{self.piece_code}'] = Game.live_black_pieces[f'B_{self.type}{self.piece_code}']
                del Game.live_black_pieces[f'B_{self.type}{self.piece_code}']
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
        
        @y.setter
        def y(self, value: int):
            self._position.coordinates['y'] = value
        
        @x.setter
        def x(self, value: int):
            self._position.coordinates['x'] = value

class Game:
    def __init__(self):
        self.self2 = self
        self.var = 'var'
        self.board: Dict[str, Dict[int, Game.Piece]] = self._create_board(NUM_COLS, NUM_ROWS)
        self.live_white_pieces: Dict[str, Game.Piece]
        self.live_black_pieces: Dict[str, Game.Piece]
        self.live_white_pieces, self.live_black_pieces = self._setup_pieces()
        self.dead_pieces: Dict[str, Game.Piece] = {}
        self.pgn: str = 'Portable Game Notation:\n' #TODO ADD TO THIS STRING EVERYTIME move_piece() IS CALLED. MOVE FORMAT FOUND AT: https://www.chess.com/terms/chess-notation
                           #---- FORMAT FOR THE FIRST PART OF THE PGN IS FOUND AT: https://www.chess.com/terms/chess-pgn

    ######################################################## PRIVATE FUNCTIONS ################################################################
    def _create_board(self, num_cols, num_rows):
        board = {}
        for col in range(0, num_cols):
            board[chr(ord('A') + col)] = {}
            for row in range(1, num_rows + 1):
                board[chr(ord('A') + col)][row] = []
        return board

    def _setup_pieces(self):
        piecesW = {}
        piecesB = {}
        back_rank = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
        for i in range(8):
            col = chr(ord('A') + i)
            piecesW[f'W_pawn{i + 1}'] = Piece(self, f'{col}2', 'W', 'pawn', f'{i + 1}')
            piecesB[f'B_pawn{i + 1}'] = Piece(self, f'{col}7', 'B', 'pawn', f'{i + 1}')
            piece_code = str(1) if i == 0 or i == 1 or i == 2 else ""
            piece_code2 = str(2) if i == 5 or i == 6 or i == 7 else ""
            piecesW[f'W_{back_rank[i]}{piece_code}{piece_code2}'] = Piece(self, f'{col}1', 'W', f'{back_rank[i]}', piece_code if piece_code else piece_code2)
            piecesB[f'B_{back_rank[i]}{piece_code}{piece_code2}'] = Piece(self, f'{col}8', 'B', f'{back_rank[i]}', piece_code if piece_code else piece_code2)
        return piecesW, piecesB
    
    def _occupy(self, piece: Piece, square: str):
        assert isinstance(square, str), 'square type must be a str'
        assert len(square) == 2, 'square length must be 2'
        assert square.isupper(), 'no col identified'
        assert square[1].isdigit(), 'no row identified'
        self.board[square[0]][int(square[1])] = piece

    def _unoccupy(self, square: str):
        assert isinstance(square, str), 'square type must be a str'
        assert len(square) == 2, 'square length must be 2'
        assert square.isupper(), 'no col identified'
        assert square[1].isdigit(), 'no row identified'
        self.board[square[0]][int(square[1])] = []


    def _is_occupied(self, square: str) -> bool:
        assert isinstance(square, str), 'square type must be a str'
        assert len(square) == 2, 'square length must be 2'
        assert square[1].isdigit(), 'no row identified'
        if self.board[square[0].upper()][int(square[1])]:
            return True
        return False

    def _kill(self, square: str):
        self.board[square[0]][int(square[1])].die()

    ######################################################## PUBLIC FUNCTIONS ################################################################
    def new_game(self):
        self.board = {}

    def clear_off_pieces(self):
        self.board = self._create_board(NUM_COLS, NUM_ROWS)
        dict1, dict2 = self._setup_pieces()
        self.board = {}
        self.live_white_pieces = {}
        self.live_black_pieces = {}
        dead_pieces = {}

        for piece_name, piece in dict1.items():
            dead_pieces[piece_name] = piece

        for piece_name2, piece2 in dict2.items():
            dead_pieces[piece_name2] = piece2
        print('clear_off_pieces EXECUTED')

    def board_data(self):
        data = ''
        for col in self.board:
            for row in self.board[col]:
                if self.board[f'{col}'][row]:
                    data += f'{self.board[f"{col}"][row].square}{self.board[f"{col}"][row].type_code}'
        return data

    def move_piece(self, piece_from: str, destination: str) -> tuple[str, str, bool]: #TODO FINISH FUNCTION IN COLLISION_DETECTION.PY
        while not isinstance(piece_from, str):
            piece_from = input('invalid coordinate. Try first coordinate again: ').upper()
        while not isinstance(destination, str):
            destination = input('invalid coordinate. Try second coordinate again: ').upper()
        while not len(piece_from) == 2 or not len(destination) == 2:
            piece_from = input('invalid coordinate. Try the first coordinate again: ').upper()
            destination = input('Now the second: ').upper()
        while not piece_from[0].isalpha() or not destination[0].isalpha():
            piece_from = input('invalid coordinate. Try the first coordinate again: ').upper()
            destination = input('Now the second: ').upper()
        while not piece_from[1].isdigit() or not destination[1].isdigit():
            piece_from = input('invalid coordinate. Try the first coordinate again: ').upper()
            destination = input('Now the second: ').upper()
        while piece_from[0] == destination[0] and piece_from[1] == destination[1]:
            destination = input('Cannot move to the same coordinate. Try second coordinate again: ').upper()
        piece: self.Piece = self.board[piece_from[0].upper()][int(piece_from[1])]
        while not piece:
            piece_from = input(f'There is no piece at {piece_from}. Try first coordinate again: ').upper()
            piece: self.Piece = self.board[piece_from[0].upper()][int(piece_from[1])]    
        is_kill = self._is_occupied(destination)
        # code: str = gcode(piece_from, destination, is_kill) #BUG
        if piece.team == 'W':
            self.live_white_pieces[f'W_{piece.type}{piece.piece_code}'].move_to(destination)
        else:
            self.live_black_pieces[f'B_{piece.type}{piece.piece_code}'].move_to(destination)
        return piece_from, destination, True if is_kill else False
    