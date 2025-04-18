import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Fonts
FONT = pygame.font.SysFont(None, 60)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Game variables
player = "X"
game_over = False

def draw_board():
    screen.fill(BG_COLOR)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                          row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def check_winner():
    global game_over
    # Check rows
    for row in board:
        if row.count(row[0]) == BOARD_COLS and row[0] is not None:
            game_over = True
            return row[0]
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        return board[0][2]
    return None

def check_draw():
    for row in board:
        if None in row:
            return False
    return True

def restart():
    global board, player, game_over
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    draw_board()
    draw_figures()

draw_board()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                player = "O" if player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    draw_board()
    draw_figures()
    winner = check_winner()

    if winner:
        text = FONT.render(f"{winner} wins!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    elif check_draw():
        text = FONT.render("Draw!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        game_over = True

    pygame.display.update()

pygame.quit()
sys.exit()
