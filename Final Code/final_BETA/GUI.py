import pygame
import os
from sys import exit

def event_loop():
    global full_screen
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if full_screen: pygame.display.set_mode((board_w, board_h), pygame.RESIZABLE)
            else: pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            board_resize()
            full_screen = not full_screen

    return True

def board_resize():
    global board_surf, board_rect, tile_len
    if not full_screen:
        width = info.current_h
        height = width
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = round(info.current_h / 8)
        print(info.current_h, info.current_w)
    else:
        width = board_w
        height = board_h
        board_rect.width, board_rect.height = (width, height)
        board_surf = pygame.transform.scale(board_surf, board_rect.size)
        tile_len = board_w // 8

def draw_board():
    if full_screen:
        screen.fill((235, 255, 242))
        screen.blit(board_surf, board_rect)
    else:
        screen.fill((235, 255, 242))
        screen.blit(board_surf, board_rect)


# initialize enviroment
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Penny GUI')
info = pygame.display.Info()

# load resources
board_surf = pygame.image.load('resources/empty-chess-board.jpg').convert()
board_rect = board_surf.get_rect()
board_w, board_h = board_rect.size
tile_len = board_w // 8
pygame.display.set_mode((board_w, board_h), pygame.RESIZABLE)

# runtime variables
run = True
full_screen = False
fps_max = 30

# timers
fps_clock = pygame.time.Clock()

while run:

    run = event_loop()

    draw_board()
    pygame.display.update()
    
    fps_clock.tick(fps_max)

pygame.quit()
exit()