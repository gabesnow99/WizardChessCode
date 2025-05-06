import pygame
import Stock_and_Gary as sg
from os import environ
from sys import exit
from time import time

WHITE = (255, 255, 255)
OFF_WHITE = (225, 232, 236)
TINT = (255, 178, 102, 128)

class Piece(pygame.sprite.Sprite):
    def __init__(self, path: str, square:str, id: str):
        super().__init__()
        #initiate attributes
        self.path = path
        self.square = square
        self.id = id
        self.pending_unpop = False
        self.pending_placement = False
        self.selected = False

        #initiate image
        x, y = self._convert_square(self.square)
        self.rect = pygame.Rect(x, y, tile_len, tile_len)
        self.active_rect = pygame.Rect(x, y, tile_len * .65, tile_len * .65)
        self.active_rect.center = self.rect.center
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, self.rect.size)

    def _convert_square(self, square: str):
        file = ord(square[0]) - ord('A') + 1
        rank = int(square[1])
        x = (file - 1) * tile_len
        y = tile_len * (8 - rank) + 1
        return x, y
    
    def _pop(self):
        self.rect.x, self.rect.y = self.rect.x - 5, self.rect.y - 5
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.rect.width + 10, self.rect.height + 10))
    
    def scale_image(self):
        self.rect.x, self.rect.y = self._convert_square(self.square)
        self.rect.width, self.rect.height = tile_len, tile_len
        self.active_rect.width, self.active_rect.height = tile_len * .65, tile_len * .65
        self.active_rect.center = self.rect.center
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, self.rect.size)

    def act_selected(self):
        self.rect.center = mouse_pos
        if not self.pending_placement:
            self.kill()
            selected_piece.add(self)
            self.pending_placement = True

    def place(self, square):
        self.square = square
        self.rect.x, self.rect.y = self._convert_square(square)
        self.kill()
        if self.id[0] == 'L':
            light_pieces.add(self)
        elif self.id[0] == 'D':
            dark_pieces.add(self)
        self.pending_placement = False
        self.selected = False
    
    def update(self):
        global force_pop
        if update_state == 'n':
            # pop
            if self.active_rect.collidepoint(mouse_pos) and not self.pending_unpop:
                self._pop()
                self.pending_unpop = True
            # unpop
            elif self.pending_unpop and (not self.active_rect.collidepoint(mouse_pos) or force_pop):
                self.scale_image()
                self.pending_unpop = False
                force_pop = False
            
        if update_state == 's' and self.selected:
            self.act_selected()

    def die(self):
        die.play()
        self.kill()

class Tile(pygame.sprite.Sprite):
    def __init__(self, file, rank):
        super().__init__()
        self.file = file
        self.rank = rank
        self.is_occupied = False
        self.tile = None

        x = tile_len * (self.file - 1)
        y = tile_len * (8 - self.rank)
        self.rect = pygame.Rect(x, y, tile_len, tile_len)
        self.image = pygame.Surface((tile_len, tile_len), pygame.SRCALPHA)
        self.image.fill(TINT)

    def scale_rect(self):
        x = tile_len * (self.file - 1)
        y = tile_len * (8 - self.rank)
        
        self.rect = pygame.Rect(x, y, tile_len, tile_len)
        self.image = pygame.Surface((tile_len, tile_len), pygame.SRCALPHA)
        self.image.fill(TINT)

    def get_square(self):
        return chr(ord('A') - 1 + self.file) + str(self.rank)

    def update(self):
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image, self.rect)

def event_loop():
    global run_stock, stock_move_state, moves_i, stock_color, update_state

    for event in pygame.event.get():

        
        # check quit
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        
        # doesn't ignore the first click after the screen looses focus
        elif event.type == pygame.WINDOWFOCUSGAINED:
            pos = pygame.mouse.get_pos()
            simulated_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                'pos': pos, 
                'button': 1})
            pygame.event.post(simulated_click)

        # check for click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if update_state == 'n' and moves_i == len(moves) - 1: # checks not peice is selected nor are we looking at past moves
                select_piece(event)

            elif update_state == 's': # if we have already selected a peice
                deselect_piece(event)
        
        # user events
        if event.type == move_timer:
            # try:
            #     stock_v_gary() # when this is executing, mouse will not work
            # except:
            #     print('problem')
            ...

        # check key press
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1: # 1st top move
                stock_push_next_move(stock_top_move=1)
                
            if event.key == pygame.K_2: # 2nd top move
                stock_push_next_move(stock_top_move=2)
                
            if event.key == pygame.K_3: # 3rd top move
                stock_push_next_move(stock_top_move=3)
                
            if event.key == pygame.K_4: # 4th top move
                stock_push_next_move(stock_top_move=4)

            if event.key == pygame.K_5: # random choice 1-5 of top moves
                stock_push_next_move(stock_top_move=None, stock_chance=5)

            if event.key == pygame.K_c: # clear the board
                board_clear(noise=True)
                
            if event.key == pygame.K_f: # toggle fullscreen
                toggle_fullscreen()

            if event.key == pygame.K_g: # push Gary's move #BUG
                gary_push_next_move()

            if event.key == pygame.K_m: # pause/play music
                change_music('toggle music')

            if event.key == pygame.K_p: # toggle auto stock move
                stock_move_state = not stock_move_state

            if event.key == pygame.K_q: # toggle QUICK auto stock move
                run_stock = not run_stock

            if event.key == pygame.K_r: # reset board
                board_reset()
            
            if event.key == pygame.K_s: # switch stock color
                stock_color = 'white' if stock_color == 'black' else 'black' 

            if event.key == pygame.K_t: # flip board #BUG
                flip_board()

            if event.key == pygame.K_u: # undo last move
                undo_last_move()

            if event.key == pygame.K_v: # toggle vocals
                change_music('toggle vocals')

            if event.key == pygame.K_LEFT: # view previous move
                if moves_i != 0:
                    update_state = 'n'
                    moves_i -= 1
                    board_set(fen_to_string(moves[moves_i]))

            if event.key == pygame.K_RIGHT: # view following move
                if moves_i != len(moves) - 1:
                    moves_i += 1
                    board_set(fen_to_string(moves[moves_i]))

    return True

def prep_full_screen():
    global board_surf, board_rect, tile_len
    
    if not full_screen:
        if current_remainder < 400:
            return
        width = current_h / scale_factor
        height = width
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = round(info.current_h / 8)
        for sprite in tiles.sprites():
            sprite.scale_rect()

    else:
        width = board_w
        height = board_h
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = board_w // 8
        for sprite in tiles.sprites():
            sprite.scale_rect()

def toggle_fullscreen():
    global full_screen

    if full_screen: 
        pygame.display.set_mode((board_w, board_h + board_bottom), pygame.RESIZABLE)

    else: 
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    prep_full_screen()

    for sprite in light_pieces.sprites(): sprite.scale_image()
    for sprite in dark_pieces.sprites(): sprite.scale_image()

    full_screen = not full_screen

def draw_board(): # TODO
        # screen
        screen.fill(OFF_WHITE)
        screen.blit(board_surf, board_rect)
        
        # pieces and tiles
        if update_state == 's': tiles.update()
        dark_pieces.update()
        light_pieces.update()
        dark_pieces.draw(screen)
        light_pieces.draw(screen)

        selected_piece.update()
        selected_piece.draw(screen)

        # fps
        text = font.render(f'{round(fps_clock.get_fps())} FPS', True, OFF_WHITE)
        screen.blit(text, (5, 5))

        # menu
        # new sprite for sliders and toggles button "circle"
        # toggle music/vocals
        # slider for volume
        # maybe a bar that shows Penny's reactions
        #   and a command buttons that allows commmands to be entered (A2-A4, random peice...)

def change_music(string):
    global music_state, vocals_state

    if string == 'toggle music':
        pygame.mixer_music.pause() if music_state else pygame.mixer_music.unpause()
        music_state = not music_state
        # BUG tiny bug. After pause/unpause, if you toggle vocals the first toggle 
        #     isn't synced, but the second and on toggles will syn until paused again
        
    elif string == 'toggle vocals':
        music_pos = (time() - music_time) % 92.75 # this is the exact length of the song
        pygame.mixer_music.load('resources/danya-the-engine-king.mp3' if not vocals_state else 'resources/danya-the-engine-king[music only].mp3')
        pygame.mixer_music.play(loops=-1)
        pygame.mixer_music.set_pos(music_pos)
        vocals_state = not vocals_state

def select_piece(event, square = None):
    global update_state, move

    event_pos = (-1000,-1000)
    if event: event_pos = event.pos

    # remove piece from tile
    for tile in tiles.sprites():
        if tile.get_square().lower() == square or tile.rect.collidepoint(event_pos):
            tile.is_occupied = False
            break

    # select piece on turn
    for piece in light_pieces.sprites() if white_to_go else dark_pieces.sprites():
        if piece.square.lower() == square or piece.active_rect.collidepoint(event_pos):
            move = piece.id + ' from ' + piece.square
            select.play()
            piece.selected = True
            update_state = 's'
            piece.update()
            return

    # select piece out of turn 
    if not check_turn: 
        for piece in light_pieces.sprites() if not white_to_go else dark_pieces.sprites():
            if piece.square.lower() == square or piece.active_rect.collidepoint(event_pos):
                move = piece.id + ' from ' + piece.square
                select.play()
                piece.selected = True
                update_state = 's'
                piece.update()
                return 

def deselect_piece(event, square = None): # BUG piece freezes when thinking about Stock/Gary next move
    global update_state, move, force_pop, white_to_go, moves_i

    event_pos = (-1000,-1000)
    if event: event_pos = event.pos

    for tile in tiles.sprites():
        if tile.get_square().lower() == square or tile.rect.collidepoint(event_pos):

            # check if move is the same square
            if selected_piece.sprite.square == tile.get_square():
                selected_piece.sprite.place(selected_piece.sprite.square)
                tile.is_occupied = True
                update_state = 'n'
                force_pop = True
                deselect.play()
                return

            # create temporary move and check move
            temp_move = move + ' to ' + chr(tile.file + ord('A') - 1) + str(tile.rank)
            if check_move and not sg.check_move(move_to_san(temp_move)):
                print('Illegal Move, try again')
                print('Are you trying to flip the board? right now the pieces switched but it\'s as if the board never was. meaning you can\'t move any pawn "backwards"')
                print(f'{temp_move}', f'{sg.board.legal_moves}')
                uhuhuh.play()
                return

            # commence deselection
            move += ' to ' + chr(tile.file + ord('A') - 1) + str(tile.rank)
            square = tile.get_square()
            if tile.is_occupied: kill_piece(square)
            selected_piece.sprite.place(square)
            tile.is_occupied = True
            deselect.play()
            force_pop = False
            update_state = 'n'
            white_to_go = not white_to_go
            if check_move: sg.board.push_san(move_to_san(move))
            moves.append(sg.board.fen())
            moves_i += 1
            serial_out()

            return
    
def program_move(san):
    select_piece(event=False, square=san[0:2])
    deselect_piece(event=False, square=san[2:])

def board_clear(noise = False):
    global white_to_go

    white_to_go = True
    tiles.empty()
    dark_pieces.empty()
    light_pieces.empty()
    selected_piece.empty()
    sg.initialize()
    print('reset')
    print(sg.board, '\n')
    if noise: select.play()

def board_set(string, noise=False):
    tiles.empty()
    dark_pieces.empty()
    light_pieces.empty()
    selected_piece.empty()

    for file in range(1, 9):
        for rank in range(1, 9):
            tiles.add(Tile(file, rank))

    #string c#c# = c(dark/light) #(path number) c(file) #(rank)
    for i in range(0, len(string), 4):
        if string[i] == 'L':
            path = image_paths[int(string[i + 1]) + 6]
            square = string[i + 2 : i + 4]
            id = 'Light '
            for char in path:
                if char == '.':
                    break
                else:
                    id += char
            id = id.replace('resources/pieces/Light', '', 1) # bug, verify in terminal after every move
            light_pieces.add(Piece(path, square, id))

        elif string[i] == 'D':
            path = image_paths[int(string[i + 1])]
            square = string[i + 2 : i + 4]
            id = 'Dark '
            for char in path:
                if char == '.':
                    break
                else:
                    id += char
            id = id.replace('resources/pieces/Dark', '', 1) # bug, verify in terminal after every move
            dark_pieces.add(Piece(path, square, id))

        for tile in tiles.sprites():
            if tile.get_square() == string[i + 2:i + 4]:
                tile.is_occupied = True
                break

    if noise: deselect.play() # BUG clear and reset seem to play the same sound effect

def board_reset():
    global game_state, game_active, moves, moves_i

    game_active = True
    game_state = None

    board_clear()

    string = 'L5A1L2B1L0C1L4D1L1E1L0F1L2G1L5H1L3A2L3B2L3C2L3D2L3E2L3F2L3G2L3H2D5A8D2B8D0C8D4D8D1E8D0F8D2G8D5H8D3A7D3B7D3C7D3D7D3E7D3F7D3G7D3H7'
    board_set(string, noise = True)

    moves.append(sg.board.fen())
    moves_i = len(moves) - 1

    fight.play()

def fen_to_string(fen):
    # Split the FEN into board and other information
    board = fen.split()[0]
    
    # Prepare a string to hold the final output
    result = []
    
    # Rank numbers go from 8 (top) to 1 (bottom) for a chessboard
    rank = 8
    piece_num = {'b':'D0', 'k':'D1', 'n':'D2', 'p':'D3', 'q':'D4', 'r':'D5',
                  'B':'L0', 'K':'L1', 'N':'L2', 'P':'L3', 'Q':'L4', 'R':'L5'}

    for rank_str in board.split('/'):  # Split by ranks
        file = 'A'
        for char in rank_str:
            if char.isdigit():  # Empty squares
                file = chr(ord(file) + int(char))  # Skip forward by the number of empty squares
            else:  # Chess pieces
                result.append(piece_num[char] + file + str(rank))  # Add the piece at that position
                file = chr(ord(file) + 1)  # Move to the next file
        rank -= 1  # Move to the next rank

    string = ''
    for element in result:
        string += element
    return string

def flip_board():
    # Split the FEN into board and other information
    board = sg.board.fen().split()[0].split('/')

    # Prepare a string to hold the final output
    new_board = ''

    # flip each row
    for rank in range(7, -1, -1):
        for file in range(len(board[rank]) - 1, -1, -1):
            new_board += board[rank][file]
        new_board += '/'
    new_board = new_board[:-1]
    
    sg.board.set_board_fen(new_board)
    sg.stockfish.set_fen_position(new_board)
    board_set(fen_to_string(new_board))

def move_to_san(string):
    part1 = string[-8:-6]
    part2 = string[-2:]
    return (part1 + part2).lower()

def kill_piece(square): # TODO
        print('kill') 
        for tile in tiles.sprites():
            if tile.get_square() == square:
                for piece in light_pieces:
                    if piece.square == square:
                        piece.die()
                        return
                for piece in dark_pieces:
                    if piece.square == square:
                        piece.die()
                        return
    # when a piece takes another piece level one fire, level two fire, level three whole piece is on flames
    # also, count pieces captured at the bottom of the screen

def serial_out(): # TODO
    print(move)
    print(sg.board, '\n')
    # print(f"Stock's next move: {sg.get_Stocks_move()}")
    # print(f"Gary's next move: {sg.get_Garys_move(previous_move=move_to_san(move), color='black')[0]}")

def stock_push_next_move(stock_top_move=1, stock_chance=1):
    global white_to_go, moves_i

    response = sg.get_Stocks_move(top_move=stock_top_move, chance=stock_chance)
    sg.board.push_san(response)
    print(sg.board)

    board_set(fen_to_string(sg.board.fen()))
    white_to_go = not white_to_go
    moves.append(sg.board.fen())
    moves_i += 1
    deselect.play()

def gary_push_next_move(): # TODO
    global white_to_go

    response = sg.get_Garys_move()
    sg.board.push_san(response[0])
    print(sg.board)

    board_set(fen_to_string(sg.board.fen()))
    white_to_go = not white_to_go
    deselect.play()

def undo_last_move():
    global moves_i, white_to_go, moves

    if moves_i == 0 or moves_i != len(moves) - 1: return
    moves.pop()
    moves_i -= 1
    white_to_go = not white_to_go
    sg.board.set_fen(moves[moves_i])
    board_set(fen_to_string(moves[moves_i]))

def stock_v_gary(): # BUG need to add last_fen for each sg.get_garys_move() call
    global is_first_move, chat_to_go

    # first move
    if is_first_move:
        response = sg.get_Garys_move(is_first_move=True, fen_mem=True, color='white')[0]
        sg.board.push_san(response)
        is_first_move = False

    # following moves
    elif chat_to_go:
        print(3)
        response = sg.get_Garys_move(fen_mem=sg.board.fen())[0]
        sg.board.push_san(response)
    else:
        print(4)
        response = sg.get_Stocks_move(stock_chance)
        sg.board.push_san(response)

    print(sg.board)
    board_set(fen_to_string(sg.board.fen()))
    chat_to_go = not chat_to_go
    
def play_stock(stock_color):
    if (stock_color == 'white' and white_to_go) or (stock_color == 'black' and not white_to_go):
        stock_push_next_move()

def mod_stock(elo=None, depth=None):
    if depth: sg.stockfish.set_depth(depth)
    if elo: sg.stockfish.set_elo_rating(elo)

def check_for_end():
    global game_active, game_state

    if sg.board.is_checkmate():
        if white_to_go:
            game_state = 'b'
            game_active = False
            print('CHECKMATE!! Black Wins')
        else:
            game_state = 'w'
            game_active = False
            print('CHECKMATE!! White Wins')

    elif sg.board.is_stalemate() or sg.board.is_insufficient_material() or not sg.board.legal_moves:
        game_state = 's'
        game_active = False
        print('STALEMATE!!')

    draw_board()
    pygame.display.update()


# initialize enviroment
environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Penny GUI')
info = pygame.display.Info()
scale_factor = 1.75
current_w, current_h = round(info.current_w * scale_factor), round(info.current_h * scale_factor)
current_remainder = current_w - current_h
board_bottom = 200
board_datum = (0, 0)

# groups
tiles = pygame.sprite.Group()
light_pieces = pygame.sprite.Group()
dark_pieces = pygame.sprite.Group()

selected_piece = pygame.sprite.GroupSingle()

# load resources
gameover_surf = pygame.image.load('resources/GameOver.png').convert_alpha()
gameover_surf = pygame.transform.smoothscale(gameover_surf, (screen.get_width() // 3, screen.get_height() // 5))
gameover_rect = gameover_surf.get_rect()
gameover_rect.center = (screen.get_width() // 2, screen.get_height() // 4)
board_surf = pygame.image.load('resources/empty-chess-board.jpg').convert()
board_rect = board_surf.get_rect()
board_w, board_h = board_rect.size
tile_len = board_w // 8
pygame.display.set_mode((board_w, board_h + board_bottom), pygame.RESIZABLE)

select = pygame.mixer.Sound('resources/select.mp3')
select.set_volume(.1)
deselect = pygame.mixer.Sound('resources/deselect.mp3')
die = pygame.mixer.Sound('resources/Die.mp3')
fight = pygame.mixer.Sound('resources/Fight.mp3')
uhuhuh = pygame.mixer.Sound('resources/UhUhUh.mp3')
gameover = pygame.mixer.Sound('resources/GameOver.mp3')

pygame.mixer_music.load('resources/danya-the-engine-king[music only].mp3')
pygame.mixer_music.get_pos()
pygame.mixer_music.play(loops=-1)
music_time = time()

font = pygame.font.Font(None, 25)

image_paths = [
    'resources/pieces/bB.png',
    'resources/pieces/bK.png',
    'resources/pieces/bN.png',
    'resources/pieces/bP.png',
    'resources/pieces/bQ.png',
    'resources/pieces/bR.png',
    'resources/pieces/wB.png',
    'resources/pieces/wK.png',
    'resources/pieces/wN.png',
    'resources/pieces/wP.png',
    'resources/pieces/wQ.png',
    'resources/pieces/wR.png'
]

# runtime variables
run = True
full_screen = False # TODO state
music_state = True
vocals_state = False
white_to_go = True
chat_to_go = True
is_first_move = True
check_move = True # make off this work with stock
check_turn = True # make off this work with stock
force_pop = False
run_stock = False
stock_move_state = False
stock_color = 'black'
game_active = True
update_state = 'n' # n = none selected, s = one selected
game_state = None # s = stalemate, w = white wins, b = black wins
fps_max = 30
stock_chance = 3
stock_top_move = 1
move = ''
moves = [sg.board.fen()]
moves_i = 0

# timers
fps_clock = pygame.time.Clock()
move_timer = pygame.USEREVENT + 1
pygame.time.set_timer(move_timer, 1500)

# run once
board_reset()
mod_stock(depth=10, elo=3500) # modify skill/elo or depth. Normally I do 5 or 10 depth, 3500 is the highest ELO
# board_set(fen_to_string('k7/8/K7/P7/8/8/8/8'))
# sg.board.set_board_fen('k7/8/K7/P7/8/8/8/8')

pregame_query = False
if pregame_query:
    ... # this is where we can ask for a change in settings before game begins

while run:

    run = event_loop()
    mouse_pos = pygame.mouse.get_pos()

    # sg.stockfish.set_fen_position(sg.board.fen())
    # print(sg.stockfish.get_top_moves())

    if game_active:
        draw_board()
        pygame.display.update()
        
        if run_stock: stock_push_next_move()

        elif stock_move_state: play_stock(stock_color) # assign stock to 'white'/'black' or None
        #you can disable the stock v gary in the event loop under user events

        check_for_end()

    else: # TODO change end to tell who won / add history (see past moves) / add start screen with tally of wins
        screen.blit(gameover_surf, gameover_rect)
        pygame.display.update()

    fps_clock.tick(fps_max)

pygame.quit()
exit()