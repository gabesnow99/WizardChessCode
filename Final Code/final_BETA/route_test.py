import sys
from globals import *

def event_handler():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def draw_blank_board():
    WIN.fill(FILL)
    pygame.draw.rect(WIN, BROWN, BOARD)
    pygame.draw.rect(WIN, BLACK, BOARDER, 10)

    index = 0
    for file in 'ABCDEFGH':
        rank_text = RANK_FILE_FONT.render(str(file), 1, DARK_GREEN)
        WIN.blit(rank_text, RANK_POSITIONS[index])
        index += 1
    index = 0
    for rank in range(1, 9):
        file_text = RANK_FILE_FONT.render(str(rank), 1, DARK_GREEN)
        WIN.blit(file_text, FILE_POSITIONS[index])
        index += 1

    for i in range(8, 64):
        x = BOARD.x + i // 8 * WALL_LENGTH
        start_y = BOARD.y + i % 8 * WALL_LENGTH
        end_y = BOARD.y + (i % 8 + 1) * WALL_LENGTH - 1
        pygame.draw.line(WIN, BLACK, (x, start_y), (x, end_y), 3)
    for i in range(8, 64):
        start_x = BOARD.x + i % 8 * WALL_LENGTH
        end_x = BOARD.x + (i % 8 + 1) * WALL_LENGTH - 1
        y = BOARD.y + i // 8 * WALL_LENGTH
        pygame.draw.line(WIN, BLACK, (start_x, y), (end_x, y), 3)

    fps_counter_text = COUNTER_FONT.render('number of frames: ' + str(fps_counter), 1, BLACK)
    fps_counter_rectangle = fps_counter_text.get_rect()
    WIN.blit(fps_counter_text, (WIDTH - fps_counter_rectangle.width - 15, HEIGHT - 30))

def highlight_wall_collisions():
    pass

def draw_window():
    draw_blank_board()
    highlight_wall_collisions()

    pygame.display.update()

def main():
    global fps_counter
    global running
    global update

    update = True
    clock = pygame.time.Clock()
    fps_counter = 0
    running = True
    while running:
        clock.tick(FPS)
        event_handler()
        if update:
            fps_counter += 1
            draw_window()
            update = False

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
