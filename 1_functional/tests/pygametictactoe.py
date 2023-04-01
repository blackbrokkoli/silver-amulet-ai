import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_WIDTH = 10
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 3
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
BG_COLOR = (255, 255, 255)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

# Game variables
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'X'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

def draw_board():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, SCREEN_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (SCREEN_WIDTH, CELL_SIZE * i), LINE_WIDTH)

def draw_mark(x, y, mark):
    if mark == 'X':
        pygame.draw.line(screen, X_COLOR, (x * CELL_SIZE + 10, y * CELL_SIZE + 10), ((x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10), LINE_WIDTH)
        pygame.draw.line(screen, X_COLOR, ((x + 1) * CELL_SIZE - 10, y * CELL_SIZE + 10), (x * CELL_SIZE + 10, (y + 1) * CELL_SIZE - 10), LINE_WIDTH)
    elif mark == 'O':
        pygame.draw.circle(screen, O_COLOR, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10, LINE_WIDTH)

def check_win(mark):
    for row in range(GRID_SIZE):
        if all(cell == mark for cell in grid[row]):
            return True
    for col in range(GRID_SIZE):
        if all(grid[row][col] == mark for row in range(GRID_SIZE)):
            return True
    if all(grid[i][i] == mark for i in range(GRID_SIZE)):
        return True
    if all(grid[i][GRID_SIZE - i - 1] == mark for i in range(GRID_SIZE)):
        return True
    return False

def check_draw():
    return all(all(cell is not None for cell in row) for row in grid)

def main():
    global turn
    running = True
    draw_board()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if grid[row][col] is None:
                    grid[row][col] = turn
                    draw_mark(col, row, turn)

                    if check_win(turn):
                        print(f"{turn} wins!")
                        running = False
                    elif check_draw():
                        print("Draw!")
                        running = False
                    else:
                        turn = 'O' if turn == 'X' else 'X'

        pygame.display.flip()

    pygame.time.delay(3000)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
