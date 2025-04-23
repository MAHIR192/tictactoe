import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# === Constants ===
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 10
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 20
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 5

# === Colors ===
BG_TOP = (255, 204, 229)
BG_BOTTOM = (204, 255, 229)
LINE_COLOR = (255, 255, 255)
CIRCLE_COLOR = (255, 105, 180)
CROSS_COLOR = (0, 191, 255)
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (200, 255, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)

# === Fonts ===
MAIN_FONT = pygame.font.SysFont("comicsansms", 70, bold=True)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 40, bold=True)
WELCOME_FONT = pygame.font.SysFont("timesnewroman", 50, bold=True)
TITLE_FONT = pygame.font.SysFont("comicsansms", 60, bold=True)

# === Setup ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# === Game State ===
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
player = "X"
game_over = False
welcome_screen = True
start_animation = False
animation_done = False
animation_progress = 0

# === Glow effect tracking ===
glow_cells = []
glow_duration = 15

# === Winning line animation ===
winning_line = None
winning_line_progress = 0

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
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)

def draw_glow_effect():
    for cell in glow_cells:
        row, col, symbol, frame = cell
        if frame < glow_duration:
            alpha = int(255 * (1 - frame / glow_duration))
            glow_color = CROSS_COLOR if symbol == "X" else CIRCLE_COLOR
            glow_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*glow_color, alpha), glow_surface.get_rect(), border_radius=10)
            screen.blit(glow_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            cell[3] += 1
    glow_cells[:] = [cell for cell in glow_cells if cell[3] < glow_duration]

def draw_winner(winner):
    text = MAIN_FONT.render(f"{winner} wins!", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))

def draw_draw():
    text = MAIN_FONT.render("Draw!", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))

def draw_restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=15)
    text = BUTTON_FONT.render("Restart", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (button_rect.centerx - text.get_width() // 2,
                       button_rect.centery - text.get_height() // 2))
    return button_rect

def draw_welcome_screen(glow_phase):
    draw_gradient_background()

    glow = int(127.5 * (1 + math.sin(glow_phase)))
    welcome_color = (glow, 0, glow)
    welcome_text = WELCOME_FONT.render("WELCOME TO", True, welcome_color)
    screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, 150))

    title_text = TITLE_FONT.render("Tic Tac Toe", True, (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 230))

    button_rect = pygame.Rect(WIDTH // 2 - 100, 520, 200, 60)
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=20)
    button_text = BUTTON_FONT.render("Start", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                              button_rect.centery - button_text.get_height() // 2))

    return button_rect

def draw_spinning_xo(progress):
    icons = ['X', 'O', 'X', 'O']
    start_y = 420
    spacing = 110
    for i, symbol in enumerate(icons):
        angle = -progress * 5 + i * 45
        x_pos = 50 + (progress % 200) + i * spacing
        y_offset = 30 * math.sin(progress / 15 + i)
        center = (int(x_pos), int(start_y + y_offset))
        draw_rotated_symbol(symbol, center, angle)

def draw_rotated_symbol(symbol, center, angle):
    surf = pygame.Surface((100, 100), pygame.SRCALPHA)
    if symbol == 'X':
        pygame.draw.line(surf, CROSS_COLOR, (20, 20), (70, 70), 12)
        pygame.draw.line(surf, CROSS_COLOR, (20, 70), (70, 20), 12)
    else:
        pygame.draw.circle(surf, CIRCLE_COLOR, (40, 40), 35, 12)

    rotated = pygame.transform.rotate(surf, angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated, rect.topleft)

def draw_winning_line():
    global winning_line_progress
    if winning_line:
        (start_col, start_row), (end_col, end_row) = winning_line
        x1 = start_col * SQUARE_SIZE + SQUARE_SIZE // 2
        y1 = start_row * SQUARE_SIZE + SQUARE_SIZE // 2
        x2 = end_col * SQUARE_SIZE + SQUARE_SIZE // 2
        y2 = end_row * SQUARE_SIZE + SQUARE_SIZE // 2

        progress = min(winning_line_progress / 30, 1)
        current_x = x1 + (x2 - x1) * progress
        current_y = y1 + (y2 - y1) * progress

        color1 = (255, 0, 255)
        color2 = (0, 255, 255)
        blend = lambda c1, c2, t: tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        animated_color = blend(color1, color2, math.sin(winning_line_progress / 5) * 0.5 + 0.5)

        pygame.draw.line(screen, animated_color, (x1, y1), (current_x, current_y), 15)
        winning_line_progress += 1

# === Game Logic ===
def check_winner():
    global game_over, winning_line
    for i, row in enumerate(board):
        if row.count(row[0]) == COLS and row[0] is not None:
            game_over = True
            winning_line = ((0, i), (2, i))
            return row[0]
    for col in range(COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            winning_line = ((col, 0), (col, 2))
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        winning_line = ((0, 0), (2, 2))
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        winning_line = ((2, 0), (0, 2))
        return board[0][2]
    return None

def check_draw():
    return all(None not in row for row in board)

def restart_game():
    global board, player, game_over, glow_cells, winning_line, winning_line_progress
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    player = "X"
    game_over = False
    glow_cells = []
    winning_line = None
    winning_line_progress = 0

# === Main Loop ===
running = True
glow_phase = 0

while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    glow_phase += 0.05

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif welcome_screen and not start_animation and event.type == pygame.MOUSEBUTTONDOWN:
            start_button_rect = draw_welcome_screen(glow_phase)
            if start_button_rect.collidepoint(event.pos):
                start_animation = True

        elif not welcome_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                restart_button = draw_restart_button()
                if restart_button.collidepoint(event.pos):
                    restart_game()
                elif not game_over:
                    mouseX, mouseY = event.pos
                    if mouseY < SQUARE_SIZE * ROWS:
                        row = mouseY // SQUARE_SIZE
                        col = mouseX // SQUARE_SIZE
                        if board[row][col] is None:
                            board[row][col] = player
                            glow_cells.append([row, col, player, 0])
                            player = "O" if player == "X" else "X"

    if welcome_screen:
        start_button_rect = draw_welcome_screen(glow_phase)
        if start_animation:
            draw_spinning_xo(animation_progress)
            animation_progress += 1
            if animation_progress > 120:
                welcome_screen = False
    else:
        draw_board()
        draw_glow_effect()
        draw_figures()

        winner = check_winner()
        if winner:
            draw_winner(winner)
            draw_winning_line()
        elif check_draw():
            draw_draw()
            game_over = True
        draw_restart_button()

    pygame.display.update()

pygame.quit()
sys.exit()
