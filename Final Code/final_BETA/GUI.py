import pygame
import os
from sys import exit

OFF_WHITE = (225, 232, 236)

class Dark_Piece(pygame.sprite.Sprite):
    def __init__(self, id, square):
        super().__init__()
        self.id = id
        self.square = square
        self.image = ...
        self.rect = ...

class Light_Piece(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ...
        self.rect = ...

def event_loop():
    global full_screen
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if full_screen: 
                pygame.display.set_mode((board_w, board_h), pygame.RESIZABLE)
            else: 
                pygame.display.set_mode((current_w, current_h), pygame.FULLSCREEN)
            board_resize()
            full_screen = not full_screen

        # if TODO USER EVENT for reseting the board 

    return True

def board_resize():
    global board_surf, board_rect, tile_len
    if not full_screen:
        width = current_h / scale_factor #TODO check for room to have UI on side
        height = width
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = round(info.current_h / 8)
    else:
        width = board_w
        height = board_h
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = board_w // 8

def draw_board():
    if full_screen:
        screen.fill(OFF_WHITE)
        screen.blit(board_surf, board_rect)
    else:
        screen.fill(OFF_WHITE)
        screen.blit(board_surf, board_rect)


# initialize enviroment
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Penny GUI')
info = pygame.display.Info()
scale_factor = 1.75
current_w, current_h = round(info.current_w * scale_factor), round(info.current_h * scale_factor)

# load resources
board_surf = pygame.image.load('resources/empty-chess-board.jpg').convert()
board_rect = board_surf.get_rect()
board_w, board_h = board_rect.size
tile_len = board_w // 8
pygame.display.set_mode((board_w, board_h), pygame.RESIZABLE)

dark_bishop_surf = pygame.image.load('resources\DarkRook.png').convert_alpha()
dark_bishop_rect = dark_bishop_surf.get_rect()
#TODO all need to be resized along with the screen to fit the tile

dark_king_surf = pygame.image.load('resources\DarkKing.png').convert_alpha()
dark_king_rect = dark_bishop_surf.get_rect()

dark_knight_surf = pygame.image.load('resources\DarkKnight.png').convert_alpha()
dark_knight_rect = dark_bishop_surf.get_rect()

dark_pawn_surf = pygame.image.load('resources\DarkPawn.png').convert_alpha()
dark_pawn_rect = dark_bishop_surf.get_rect()

dark_queen_surf = pygame.image.load('resources\DarkQueen.png').convert_alpha()
dark_queen_rect = dark_bishop_surf.get_rect()

dark_rook_surf = pygame.image.load('resources\DarkRook.png').convert_alpha()
dark_rook_rect = dark_bishop_surf.get_rect()

light_bishop_surf = pygame.image.load('resources\LightBishop.png').convert_alpha()
light_bishop_rect = dark_bishop_surf.get_rect()

light_king_surf = pygame.image.load('resources\LightKing.png').convert_alpha()
light_king_rect = dark_bishop_surf.get_rect()

light_knight_surf = pygame.image.load('resources\LightKnight.png').convert_alpha()
light_knight_rect = dark_bishop_surf.get_rect()

light_pawn_surf = pygame.image.load('resources\LightPawn.png').convert_alpha()
light_pawn_rect = dark_bishop_surf.get_rect()

light_queen_surf = pygame.image.load('resources\LightQueen.png').convert_alpha()
light_queen_rect = dark_bishop_surf.get_rect()

light_rook_surf = pygame.image.load('resources\LightRook.png').convert_alpha()
light_rook_rect = dark_bishop_surf.get_rect()

font = pygame.font.Font(None, 30)

# groups
light_pieces = pygame.sprite.Group()
dark_pieces = pygame.sprite.Group()

# runtime variables
run = True
full_screen = False
reset_board = True
fps_max = 30

# timers
fps_clock = pygame.time.Clock()

while run:

    run = event_loop()

    draw_board()
    text = font.render(f'{round(fps_clock.get_fps())}', True, OFF_WHITE)
    screen.blit(text, (5, 5))
    pygame.display.update()
    
    fps_clock.tick(fps_max)

pygame.quit()
exit()