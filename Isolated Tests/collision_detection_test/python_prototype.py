import support #type: ignore

support.cls()

#INTEGRATION BUG_PREVENTION: any division need to be done so that results have no remainders and all products are integers
#--------------------------- Therefore, board_height // num_col AND board_height // num_rows needs to be a whole, EVEN number
#--------------------------- Also, board numbers over 9 will cause an error in the isOccupied() function and perhaps serveral other places
#NOTAS: Key errors are likely trying to reference squares outside of the board

class Position:
    def __init__(self, col: str, row: int):
        assert isinstance(col, str), 'col type must be str'
        assert len(col) == 1, 'for now col must be A - Z'
        assert isinstance(row, int), 'row type must be int'
        self.coordinates = {'x': self._convert_x(col), 'y': self._convert_y(row)}

    def moveTo(self, col: str, row: int):
        self.coordinates['x'] = self._convert_x(col)
        self.coordinates['y'] = self._convert_y(row)

    def _convert_col(self, col: str):
        return int(ord(col.upper()) - ord('A') + 1)
    
    def _convert_x(self, col: str):
        return half_wall_length + wall_length * (self._convert_col(col) - 1)
    
    def _convert_y(self, row: int):
        return half_wall_length + wall_length * (row - 1)

class Piece:
    def __init__(self, square: str, team: str):
        assert team == 'White' or team == 'Black'
        assert isinstance(square, str), 'square type must be a string'
        self.square = self._find_first_char_and_int(square)
        self.col, self.row = self.square
        self.row = int(self.row)
        self.isCaptured = False
        self.team = team
        self._position = Position(self.col, self.row)
        occupy(self, self.square)

    def moveTo(self, square: str):
        square = self._find_first_char_and_int(square)
        unoccupy(self.square)
        self.square = square
        if isOccupied(square):
            kill(square)
        self.col, self.row = square
        self.row = int(self.row)
        self._position.moveTo(self.col, self.row)
        occupy(self, square)

    def die(self):
        print('die function executed!')
    # TODO: MAKE A FUNTION THAT HANDLES BEING CAPTURED
    # THE SQUARE ATTRIBUTE OF THE self._position SHOULD REFLECT BEING OFF THE BOARD 
    # THE COORDINATES ATTRIBUTE OF THE self._position SHOULD PLACE THE PIECE SOMEHWERE OUT OF THE WAY OF ALL OTHER PIECES/SQUARES
    
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
        return (f'Captured: {self.isCaptured}, Team: {self.team}'
                f'\npawn.x: {self.x}, pawn.y: {self.y}'
                f'\npawn.col: {self.col}, pawn.row: {self.row}, pawn.square: {self.square}')
    
    # @y.setter
    # def y(self, value: int):
    #     self.current_position['y'] = value
    # TODO WHEN MODIFYING A COORDINATE MODIFY COORDINATE AND ROW OR COLUMN
    
    # @x.setter
    # def x(self, value: int):
    #     self.current_position['x'] = value
    # TODO WHEN MODIFYING A COORDINATE MODIFY COORDINATE AND ROW OR COLUMN 

def set_up_board(num_cols, num_rows):
    board = {}
    for col in range(0, num_cols):
        board[chr(ord('A') + col)] = {}
        for row in range(1, num_rows + 1):
            board[chr(ord('A') + col)][row] = []
    return board

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


def isOccupied(square: str):
    assert isinstance(square, str), 'square type must be a str'
    assert len(square) == 2, 'square length must be 2'
    assert square.isupper(), 'no col identified'
    assert square[1].isdigit(), 'no row identified'
    if board[square[0]][int(square[1])]:
        return True
    return False

def kill(square: str):
    board[square[0]][int(square[1])].die() # TODO FIND OUT HOW TO MAKE THIS ONE DIE

board_height = 2000 #int(input('Please enter board hieght: '))
num_cols = 8 #int(input('Please enter number of columns: '))
num_rows = 8 #int(input('Please enter number of rows: '))
wall_length = board_height // num_rows
half_wall_length = wall_length // 2 
assert isinstance(wall_length, int), "board_height, num_rows, num_cols must all be integers, OR wall_length isn't calculating properly"
assert board_height // num_rows % 2 == 0, "board_height / num_rows AND board_height / num_cols must be even"
board = set_up_board(num_cols, num_rows)

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