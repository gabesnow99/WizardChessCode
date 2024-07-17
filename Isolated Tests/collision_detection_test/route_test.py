import pygame
import sys
import python_prototype

pygame.init()

# Define constants
# Some constants are defined in python_prototype
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Define colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE2 = (102, 178, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREY = (152, 152, 152)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Route Test')

# Define lists for board by lines
outside_lines = []
inside_lines = []

# Define squares and route
squares = ''
route = []

# Create a request input state function
def request_state():
    global run
    global squares

    while len(squares) != 4:

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return
                elif event.key == pygame.K_RETURN:
                    print(f'Route entered so far: {squares}')
                else:
                    squares += (pygame.key.name(event.key))
    print(f'Route: {squares}')

# Create a display simulation state function
def simulation_state():
    global squares
    global route

    # Fill background
    screen.fill(BLUE2)

    # Draw Board
    board = pygame.Rect(100, 50, 400, 400)
    pygame.draw.rect(screen, GREY, board)
    boarder = pygame.Rect(100, 50, 400, 400)
    pygame.draw.rect(screen, BLACK, boarder, 7)
    pygame.draw.line(screen, BROWN, (0, 0), (600, 600), 5)

    # Update display
    pygame.display.flip()

    # Reset route
    squares = ''

# Run game
run = True
while run:
    simulation_state()
    request_state()

pygame.quit()
sys.exit()
