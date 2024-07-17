import pygame
import sys
import python_prototype

pygame.init()

# Define constants
# Some constants are defined in python_prototype
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Define colors
BG = (102, 178, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    print(f'Route entered so far: {squares}')

# Create a display simulation state function
def simulation_state():
    global squares
    global route

    # Fill background
    screen.fill(BG)

    # Draw Board

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
