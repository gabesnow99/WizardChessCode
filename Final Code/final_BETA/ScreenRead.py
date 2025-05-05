import pyautogui as pgui
import cv2
import numpy as np
import os

SQUARES = []
TEMPLATES = {}
SIZE = 0
# REGION = [357, 267, 1442, 1442] # for Surface Pro ... bot?
# REGION = [412, 266, 1448, 1448] # for Surface Pro
# REGION = [224, 152, 809, 809] # for left monitor (could be 205)
# REGION = [2144, 152, 809, 809] # for right monitor NOT WORKING
REGION = [234, 153, 928, 928]

BUTTONS = []
TEMPLATES_BUTTONS = {}
REGION_NEW_1_MIN = [488, 552, 131, 39] # for left monitor
CLICK_OFFSET = (REGION_NEW_1_MIN[2] // 2, REGION_NEW_1_MIN[3] // 2)

#############################
#        READ SCREEN        #
#############################

def get_squares_from_screen():
    global SQUARES, SIZE

    screenshot = pgui.screenshot(region=REGION)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    frame[frame > 100] = 255
    # Optional: Show it
    # cv2.imshow("Screenshot", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    SIZE = frame.shape[0] // 8
    SQUARES = [
        [
            frame[rank*SIZE:(rank+1)*SIZE, file*SIZE:(file+1)*SIZE]
            for file in range(8)
        ]
        for rank in range(8)
    ]

    # # optional to show pieces
    # for i in range(8):
    #     for j in range(8):
    #         cv2.imshow(f'{i,j}', SQUARES[i][j])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def load_templates(folder, size):
    global TEMPLATES

    for file in os.listdir(folder):
        name = os.path.splitext(file)[0]  # 'wP', 'bQ', etc.
        path = os.path.join(folder, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img[img < 10] = 255 # this is called a Boolean Mask (clean and powerful NumPy tool)
        img[img > 100] = 255
        img = cv2.resize(img, (size, size))
        TEMPLATES[name] = img
    # # optional to show templates
    #     cv2.imshow(f'{file}', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def match_piece(square, templates, threshold=0.3):
    best_score = 0
    best_match = ''

    for name, template in templates.items():
        result = cv2.matchTemplate(square, template, cv2.TM_CCOEFF_NORMED)
        _, score, _, _ = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_match = name

    # print(f"→ Best: {best_match} ({best_score:.2f})") # shows → how good of a fit

    return best_match if best_score >= threshold else ''

def rank_to_fen(rank):
    # Example: row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    fen = ''
    empty = 0
    for square in rank:
        if square == '':
            empty += 1
        else:
            if empty:
                fen += str(empty)
                empty = 0
            fen += square[1].lower() if square[0] == 'b' else square[1].upper()
    if empty:
        fen += str(empty)
    return fen

def get_fen():
    fen_ranks = []
    for rank in SQUARES:
        rank_fen = []
        for square in rank:
            match = match_piece(square, TEMPLATES)
            rank_fen.append(match)
        fen_ranks.append(rank_fen)

    return '/'.join(rank_to_fen(row) for row in fen_ranks)

#############################
#      READ FOR BUTTON      #
#############################

def get_screen_portion():
    global BUTTONS
    
    screen_portion = pgui.screenshot(region=REGION_NEW_1_MIN)
    frame = cv2.cvtColor(np.array(screen_portion), cv2.COLOR_RGB2GRAY)
    BUTTONS.append(frame)

    # # Optional: Show it
    # cv2.imshow("screen_portion", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def load_button_templates(folder):
    global TEMPLATES_BUTTONS

    for file in os.listdir(folder):
        name = os.path.splitext(file)[0]  # 'wP', 'bQ', etc.
        path = os.path.join(folder, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        TEMPLATES_BUTTONS[name] = img
    # # optional to show templates
    #     cv2.imshow(f'{file}', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def match_button(button, templates, threshold=0.75):
    best_score = 0
    best_match = ''

    for name, template in templates.items():
        result = cv2.matchTemplate(button, template, cv2.TM_CCOEFF_NORMED)
        _, score, _, _ = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_match = name

    # print(f"→ Best: {best_match} ({best_score:.2f})") # shows → how good of a fit

    return best_match if best_score >= threshold else ''

#############################
#      MAIN FUNCTIONS       #
#############################

def read_screen():
    get_squares_from_screen()
    # print("FEN:", get_fen())

    return get_fen()

def poll_buttons():
    global BUTTONS
    BUTTONS = []
    get_screen_portion()

    # TODO give static counter that looks for resignation using pyautogui image search feature
    # NOTE fix this later
    val = False
    for button in BUTTONS:
        val = match_button(button, TEMPLATES_BUTTONS)
    return True if val else False


#############################
#      INITIALIZATION       #
#############################

get_squares_from_screen()
load_templates('resources/pieces/', SIZE)
# print(read_screen())

# TODO below
# load_button_templates('resources/button masks')

# print(poll_buttons())