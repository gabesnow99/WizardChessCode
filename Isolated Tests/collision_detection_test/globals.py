import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Route Tester')

FPS = 27

FILL = (207, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (20, 61, 18)
BROWN = (51, 31, 31)

COUNTER_FONT = pygame.font.SysFont('comicsans', 15)
RANK_FILE_FONT = pygame.font.SysFont('comicsans', 25)

BOARD_WIDTH = 816
assert BOARD_WIDTH % 16 == 0, 'BOARD_WIDTH % 4 != 0'
WALL_LENGTH = BOARD_WIDTH // 8
HALF_WALL_LENGTH = WALL_LENGTH // 2
assert HALF_WALL_LENGTH % 2 == 1, 'HALF_WALL_LENGTH % 2 != 1'
BOARD = pygame.Rect((WIDTH - BOARD_WIDTH) // 2,(HEIGHT - BOARD_WIDTH) // 5, BOARD_WIDTH, BOARD_WIDTH)
RANK_POSITIONS = [(BOARD.x - HALF_WALL_LENGTH, HALF_WALL_LENGTH // 2 + BOARD.y + WALL_LENGTH * i) for i in range(8)]
FILE_POSITIONS = [(HALF_WALL_LENGTH + BOARD.x + i * WALL_LENGTH, BOARD.y + WALL_LENGTH * 8 + HALF_WALL_LENGTH // 2) for i in range(8)]
BOARDER = pygame.Rect(BOARD.x - 10, BOARD.y - 10, BOARD.width + 20, BOARD.height + 20)
