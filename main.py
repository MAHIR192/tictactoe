import pygame
import sys

# Initialize Pygame
pygame.init()

# === Constants ===
WIDTH, HEIGHT = 600, 700  # Extra height for Restart Button
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 10
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 20
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 5

# === Colors ===
BG_TOP = (255, 204, 229)       # Light Pink
BG_BOTTOM = (204, 255, 229)    # Mint Green
LINE_COLOR = (255, 255, 255)
CIRCLE_COLOR = (255, 105, 180)  # Hot Pink
CROSS_COLOR = (0, 191, 255)     # Deep Sky Blue
BUTTON_COLOR = (255, 255, 255)
BUTTON_TEXT_COLOR = (0, 0, 0)

# === Fonts ===
MAIN_FONT = pygame.font.SysFont("comicsansms", 70, bold=True)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 40, bold=True)

# === Setup ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# === Game State ===
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
player = "X"
game_over = False

# === Drawing Functions ===
def draw_gradient_background():
    for y in range(HEIGHT):
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_board():
    draw_gradient_background()
    for row in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, SQUARE_SIZE * ROWS), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            centerX = col * SQUARE_SIZE + SQUARE_SIZE // 2
            centerY = row * SQUARE_SIZE + SQUARE_SIZE // 2

            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (centerX, centerY), CIRCLE_RADIUS, CIRCLE_WIDTH)
                pygame.draw.circle(screen, (255, 255, 255), (centerX, centerY), CIRCLE_RADIUS - 10, 5)
            elif board[row][col] == "X":
                # Descending diagonal
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                # Ascending diagonal
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)

def draw_winner(winner):
    text = MAIN_FONT.render(f"{winner} wins!", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))

def draw_draw():
    text = MAIN_FONT.render("Draw!", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))

def draw_restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=15)
    text = BUTTON_FONT.render("Restart", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (button_rect.centerx - text.get_width() // 2,
                       button_rect.centery - text.get_height() // 2))
    return button_rect

# === Game Logic ===
def check_winner():
    global game_over
    # Rows
    for row in board:
        if row.count(row[0]) == COLS and row[0] is not None:
            game_over = True
            return row[0]
    # Columns
    for col in range(COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            return board[0][col]
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        return board[0][2]
    return None

def check_draw():
    return all(None not in row for row in board)

def restart_game():
    global board, player, game_over
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    player = "X"
    game_over = False

# === Main Loop ===
running = True
while running:
    draw_board()
    draw_figures()

    winner = check_winner()
    if winner:
        draw_winner(winner)
    elif check_draw():
        draw_draw()
        game_over = True

    restart_button = draw_restart_button()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Click to restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                restart_game()
            elif not game_over:
                mouseX, mouseY = event.pos
                if mouseY < SQUARE_SIZE * ROWS:
                    row = mouseY // SQUARE_SIZE
                    col = mouseX // SQUARE_SIZE
                    if board[row][col] is None:
                        board[row][col] = player
                        player = "O" if player == "X" else "X"

pygame.quit()
sys.exit()
