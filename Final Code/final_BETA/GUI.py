import pygame
import os
from sys import exit

OFF_WHITE = (225, 232, 236)
TINT = (255, 178, 102, 128)

class Piece(pygame.sprite.Sprite):
    def __init__(self, path: str, square:str, id: str):
        super().__init__()
        self.path = path
        self.square = square
        self.id = id
        self.pending_unpop = False
        self.pending_placement = False
        self.selected = False

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
        self.kill()
        if self.id[0] == 'L':
            light_pieces.add(self)
        elif self.id[0] == 'D':
            dark_pieces.add(self)
        self.pending_placement = False
        self.selected = False
    
    def update(self):
        if update_state == 'n':
            if self.active_rect.collidepoint(mouse_pos) and not self.pending_unpop:
                self._pop()
                self.pending_unpop = True
            elif self.pending_unpop and not self.active_rect.collidepoint(mouse_pos):
                self.scale_image()
                self.pending_unpop = False
            
        if update_state == 's' and self.selected:
            self.act_selected()

class Tile(pygame.sprite.Sprite):
    def __init__(self, file, rank):
        super().__init__()
        self.file = file
        self.rank = rank

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
    global full_screen, update_state
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if update_state == 'n':
                for sprite in light_pieces.sprites():
                    if sprite.active_rect.collidepoint(event.pos):
                        sprite.selected = True
                        update_state = 's'
                        return True

                for sprite in dark_pieces.sprites():
                    if sprite.active_rect.collidepoint(event.pos):
                        sprite.selected = True
                        update_state = 's'
                        return True

            elif update_state == 's':
                for sprite in tiles.sprites():
                    if sprite.rect.collidepoint(event.pos):
                        selected_piece.sprite.place(sprite.get_square())
                        update_state = 'n'
                        return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if full_screen: 
                    pygame.display.set_mode((board_w, board_h + board_bottom), pygame.RESIZABLE)

                else: 
                    pygame.display.set_mode((current_w, current_h), pygame.FULLSCREEN)

                prep_full_screen()

                for sprite in light_pieces.sprites(): sprite.scale_image()
                for sprite in dark_pieces.sprites(): sprite.scale_image()

                full_screen = not full_screen

            elif event.key == pygame.K_r:
                board_reset()

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

def draw_board():
        screen.fill(OFF_WHITE)
        screen.blit(board_surf, board_rect)
        
        if update_state == 's': tiles.update()
        dark_pieces.update()
        light_pieces.update()
        dark_pieces.draw(screen)
        light_pieces.draw(screen)

        selected_piece.update()
        selected_piece.draw(screen)

        text = font.render(f'{round(fps_clock.get_fps())} FPS', True, OFF_WHITE)
        screen.blit(text, (5, 5))

def board_reset():
    tiles.empty()
    dark_pieces.empty()
    light_pieces.empty()
    selected_piece.empty()

    for file in range(1, 9):
        for rank in range(1, 9):
            tiles.add(Tile(file, rank))
    
    #string c#c# = c(dark/light) #(path number) c(file) #(rank)
    string = 'L5A1L2B1L0C1L4D1L1E1L0F1L2G1L5H1L3A2L3B2L3C2L3D2L3E2L3F2L3G2L3H2D5A8D2B8D0C8D4D8D1E8D0F8D2G8D5H8D3A7D3B7D3C7D3D7D3E7D3F7D3G7D3H7'
    for i in range(0, len(string), 4):
        if string[i] == 'L':
            path = paths[int(string[i + 1]) + 6]
            square = string[i + 2 : i + 4]
            id = 'Light_'
            for char in path:
                if char == '.':
                    break
                else:
                    id += char
            id = id.replace('resources\\Light', '', 1)
            light_pieces.add(Piece(path, square, id))

        elif string[i] == 'D':
            path = paths[int(string[i + 1])]
            square = string[i + 2 : i + 4]
            id = 'Dark_'
            for char in path:
                if char == '.':
                    break
                else:
                    id += char
            id = id.replace('resources\\Dark', '', 1)
            dark_pieces.add(Piece(path, square, id))
    
# initialize enviroment
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Penny GUI')
info = pygame.display.Info()
scale_factor = 1.75
current_w, current_h = round(info.current_w * scale_factor), round(info.current_h * scale_factor)
current_remainder = current_w - current_h
board_bottom = 200

# groups
tiles = pygame.sprite.Group()
light_pieces = pygame.sprite.Group()
dark_pieces = pygame.sprite.Group()

selected_piece = pygame.sprite.GroupSingle()

# load resources
board_surf = pygame.image.load('resources/empty-chess-board.jpg').convert()
board_rect = board_surf.get_rect()
board_w, board_h = board_rect.size
tile_len = board_w // 8
pygame.display.set_mode((board_w, board_h + board_bottom), pygame.RESIZABLE)

paths = [
    'resources\DarkBishop.png',
    'resources\DarkKing.png',
    'resources\DarkKnight.png',
    'resources\DarkPawn.png',
    'resources\DarkQueen.png',
    'resources\DarkRook.png',
    'resources\LightBishop.png',
    'resources\LightKing.png',
    'resources\LightKnight.png',
    'resources\LightPawn.png',
    'resources\LightQueen.png',
    'resources\LightRook.png'
]
board_reset()

font = pygame.font.Font(None, 25)

# runtime variables
run = True
full_screen = False
reset_board = True
update_state = 'n' # n = none selected, s = one selected 
fps_max = 30

# timers
fps_clock = pygame.time.Clock()

while run:

    run = event_loop()
    mouse_pos = pygame.mouse.get_pos()

    draw_board()
    pygame.display.update()
    
    fps_clock.tick(fps_max)

pygame.quit()
exit()