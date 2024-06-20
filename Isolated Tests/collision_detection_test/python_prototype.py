import support #type: ignore

#INTEGRATION BUG_PREVENTION: any division need to be done so that results have no remainders and all products are integers
#--------------------------- Therefore, board_height // num_col AND board_height // num_rows needs to be a whole, EVEN number

support.cls()

board_height = 2000 #int(input('Please enter board hieght: '))
num_cols = 8 #int(input('Please enter number of columns: '))
num_rows = 8 #int(input('Please enter number of rows: '))
wall_length = board_height // num_rows
half_wall_length = wall_length // 2 
messages = []
assert num_cols == num_rows, "for now, num_rows and num_cols must be equal"
assert isinstance(wall_length, int), "board_height, num_rows, num_cols must all be integers, OR wall_length isn't calculating properly"
assert board_height / num_rows % 2 == 0, "board_height / num_rows AND board_height / num_cols must be even"

class Square:
    def __init__(self, col: str, row: int):
        self.col = col
        self.row = row
        self.isOccupiedBy = []

class Position:
    def __init__(self, square: str):
        assert isinstance(square, str), 'invalid square type (str)'
        first_char, first_int = self._find_first_char_and_int(square)
        col_num = int(ord(first_char.upper()) - ord('A') + 1)
        self.square = first_char.upper() + first_int
        x = half_wall_length + wall_length * (col_num - 1)
        y = half_wall_length + wall_length * (int(first_int) - 1)
        self.coordinates = {'x': x, 'y': y}

    def moveTo(self, square: str):
        assert isinstance(square, str), 'invalid square type (str)'
        assert len(square) == 2, 'invalid string'
        assert isinstance(square[0], str), 'no col was identified'
        assert isinstance(square[1], int), 'no row was identified'
        new_col, new_row = self._find_first_char_and_int(square)
        # TODO 

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
        return first_char, first_int

class Piece:
    def __init__(self, square: Position): # TODO CHANGE THIS TO ONLY ACCEPT A STRING
        assert isinstance(square, Position), 'invalid position object'
        self.col = square.square[0]
        self.row = square.square[1]
        self.isCaputered = False
        self._col_num = self._convertCol(self.col)
        self._position = Position(self.col + str(self.row))

    def moveTo(self, square: str):
        self._position.moveTo(square)
            
    # TODO: WHEN MOVING A PIECE, send coordinates to the position class

    def _convertCol(self, string):
        return int(ord(string.upper()) - ord('A') + 1)
    
    # TODO: MAKE A FUNTION THAT HANDLES BEING CAPTURED
    # THE SQUARE ATTRIBUTE OF THE 
    
    @property
    def x(self):
        return self._position.coordinates['x']

    @property
    def y(self):
        return self._position.coordinates['y']
    
    @property
    def square(self):
        return self._position.square
    
    @property # TODO FIGURE OUT IF WE EVEN NEED THIS
    def coordinates(self):
        return self._position.coordinates
    
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
    for col in range(num_cols):
        for row in range(num_rows):
            board[(col), (row)] = Square(col, row)
    return board

def printm():
    for message in messages: print(message)

board = set_up_board(num_cols, num_rows)

start = input('Please enter the starting location: ')
support.cls()
pawn = Piece(start)
messages.append(f'\npawn.x: {pawn.x}, pawn.y: {pawn.y}, pawn.coordinates: {pawn.coordinates}\npawn.col: {pawn.col}, pawn.row: {pawn.row}, pawn.square: {pawn.square}')
printm()

new_square = Position(input('\nPlease enter the new location: '))
support.cls()
messages.append(f'\nMoved pawn to ')
pawn.moveTo(new_square)
printm()
