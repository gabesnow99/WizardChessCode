import winsound
import time
import Stock_and_Gary as sg
import pyautogui as pgui
from ScreenRead import read_screen, poll_buttons, SIZE, REGION, CLICK_OFFSET, REGION_NEW_1_MIN
from keyboard import add_hotkey, wait
#https://github.com/zhelyabuzhsky/stockfish/blob/master/stockfish/models.py

TILES = {}
BOT_COLOR = 'WHITE'
MOVE_LEVEL = 1
NEW_FEN = ''
LAST_FEN = ''
GAME_ACTIVE = True
PAUSE = False
PLAY_SELF = False
CLICKK_DELAY = .01 # seconds
TICK = .01 # seconds

def ask_color():
    global BOT_COLOR

    print('The game will begin after entering your color.')
    response = input('Will you be white or black?: ')
    response = ''.join(response.split())

    if response in ['w', 'W', 'white', 'White', 'WHITE']:
        return
    elif response in ['b', 'B', 'black', 'Black', 'BLACK']:
        BOT_COLOR = 'BLACK'
        return
    else:
        print('INCORRECT: please indicate white or black...')
        ask_color() # this is not great practice, but I've never used recursion like this before haha

def on_esc():
    global GAME_ACTIVE
    GAME_ACTIVE = False

def on_p():
    global PAUSE
    winsound.Beep(500, 500)
    time.sleep(.1)
    PAUSE = not PAUSE

def on_s():
    global BOT_COLOR
    winsound.Beep(500, 500)
    if BOT_COLOR == 'WHITE': BOT_COLOR = 'BLACK'
    else: BOT_COLOR = 'WHITE'

def on_t():
    global PLAY_SELF
    if PLAY_SELF:
        winsound.Beep(600, 250)
        winsound.Beep(500, 250)
    else:
        winsound.Beep(500, 250)
        winsound.Beep(600, 250)
    PLAY_SELF = not PLAY_SELF

def initialize_hotkeys():
    add_hotkey('esc', on_esc)
    add_hotkey('p', on_p)
    add_hotkey('s', on_s)
    add_hotkey('t', on_t)

def poll_pause():
    while PAUSE: time.sleep(.1)

#############################
#        GAME FUNCS         #
#############################

def check_for_opponent_move():
    global NEW_FEN, LAST_FEN

    NEW_FEN = read_screen()
    if NEW_FEN == LAST_FEN: return
    else:
        LAST_FEN = NEW_FEN
        sg.board.set_board_fen(NEW_FEN)
        sg.board.turn = not sg.board.turn
        print(sg.board, f'\n{"Black" if sg.board.turn else "White"} just moved.\n')
    
def check_for_bot_move(): # BUG Stock needs some help using the black pieces
    global BOT_COLOR

    # if it's not the BOT's turn
    if BOT_COLOR == 'WHITE' and not sg.board.turn:
        return
    elif BOT_COLOR == 'BLACK' and sg.board.turn:
        return
    
    # if it is the BOT's turn
    else:
        poll_pause()
        move = sg.get_Stocks_move(top_move=MOVE_LEVEL)
        # sg.preview_moves(4)
        if not move: 
            # on_esc() # turned off for playing over and over
            time.sleep(10) # turn off for NOT playing over and over
            return
        
        # Select Piece
        poll_pause()
        sq1 = TILES[move[:2]]
        pgui.click(sq1[0], sq1[1]) 
        time.sleep(CLICKK_DELAY)
        try:
            sq2 = TILES[move[2:]]
        except:
            ## vv this handles promotion vv ##
            sq2 = move[-1]
            if sq2 in ['q', 'Q']:
                pgui.click(sq1[0], sq1[1] - SIZE)
                time.sleep(CLICKK_DELAY)
                sq2 = (sq1[0], sq1[1] - SIZE)
            if sq2 in ['n', 'N']:
                pgui.click(sq1[0], sq1[1] - SIZE)
                time.sleep(CLICKK_DELAY)
                sq2 = (sq1[0], sq1[1])
            if sq2 in ['r', 'R']:
                pgui.click(sq1[0], sq1[1] - SIZE)
                time.sleep(CLICKK_DELAY)
                sq2 = (sq1[0], sq1[1] + SIZE)
            if sq2 in ['b', 'B']:
                pgui.click(sq1[0], sq1[1] - SIZE)
                time.sleep(CLICKK_DELAY)
                sq2 = (sq1[0], sq1[1] + (2*SIZE))
            else: 
                print('failed promotion')
            ## ^^ this handles promotion ^^ ##

        # deselect the peice (or select promotion)
        pgui.click(sq2[0], sq2[1])
        if PLAY_SELF: BOT_COLOR = not BOT_COLOR
        
def check_for_end():
    if sg.board.is_checkmate():
        if sg.board.turn:
            print('CHECKMATE!! Black Wins')
            return True
        else:
            print('CHECKMATE!! White Wins')
            return True

    elif sg.board.is_stalemate() or sg.board.is_insufficient_material() or not sg.board.legal_moves:
        print('STALEMATE!!')
        return True
    else:
        return False
    
#############################
#        INITIALIZE         #
#############################

# mod Stockfish
sg.stockfish.set_depth(10)
sg.stockfish.set_skill_level(20) # 20 is the highest
sg.stockfish.set_elo_rating(3500)

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
for rank in range (8):
    for file in range(8):
        name = f'{files[file]}{rank+1}'
        x = REGION[0] + int(SIZE*(.5+file))
        y = REGION[1] + int(SIZE*(7.5-rank))
        TILES[name] = (x, y)

ask_color()
initialize_hotkeys()
LAST_FEN = read_screen()
sg.board.set_board_fen(LAST_FEN)
sg.board.turn = False

# Handle Color
if BOT_COLOR == 'BLACK':
    while LAST_FEN == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR':
        time.sleep(.5)
        LAST_FEN = read_screen()
        
    sg.board.set_board_fen(LAST_FEN)
    sg.board.turn = True

# Wait for start
wait('space')
winsound.Beep(700, 250)
time.sleep(.05)
winsound.Beep(700, 250)
time.sleep(.05)
winsound.Beep(700, 250)

#############################
#         RUN GAME          #
#############################

count = 0
while GAME_ACTIVE:
    # Handle timing
    poll_pause()
    start_time = time.time()
    count += 1
    print(count)

    # Handle new game
    if poll_buttons(): 
        pgui.click(REGION_NEW_1_MIN[0] + CLICK_OFFSET[0], REGION_NEW_1_MIN[1] + CLICK_OFFSET[1])
        time.sleep(5)

    # Handle game
    check_for_opponent_move()
    if check_for_end(): break
    check_for_bot_move()

    # ⏱ Wait only if we're goin too fast
    elapsed = time.time() - start_time
    if elapsed < TICK:
        print('rested')
        time.sleep(TICK - elapsed)

#############################
#         GAME OVER         #
#############################

print(sg.board)
winsound.Beep(900, 1000)
