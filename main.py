import pygame, sys, math, random

# === Initialization ===
pygame.init()
pygame.mixer.init()

# === Sound ===
pygame.mixer.music.load("Background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
start_sound = pygame.mixer.Sound("game-start-and-reset-_-final.wav")
x_sound = pygame.mixer.Sound("select-sound-xxx.wav")
o_sound = pygame.mixer.Sound("select-sound-ooo.wav")
win_sound = pygame.mixer.Sound("success-1-fiinal.wav")
draw_sound = pygame.mixer.Sound("draw-4-_final.wav")

# === Constants ===
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 10
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH, CROSS_WIDTH = 20, 20
SPACE = SQUARE_SIZE // 5

# Colors
BG_TOP, BG_BOTTOM = (255, 204, 229), (204, 255, 229)
LINE_COLOR, BUTTON_COLOR = (255, 255, 255), (255, 255, 255)
BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR = (200, 255, 200), (0, 0, 0)
CIRCLE_COLOR, CROSS_COLOR = (255, 105, 180), (0, 191, 255)

# Fonts
MAIN_FONT = pygame.font.SysFont("Courier New", 96, bold=True)
BUTTON_FONT = pygame.font.SysFont("Berlin Sans FB Demi", 54, bold=True)
WELCOME_FONT = pygame.font.SysFont("timesnewroman", 54, bold=True)
TITLE_FONT = pygame.font.SysFont("Berlin Sans FB Demi", 84, bold=True)

# === Setup ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# === Game State ===
board = [[None]*COLS for _ in range(ROWS)]
player = "X"
win_sound_played = draw_sound_played = game_over = welcome_screen = confetti_spawned = False
welcome_screen, start_animation, animation_done = True, False, False
animation_progress, glow_phase = 0, 0
confetti_particles, glow_cells = [], []
winning_line, winning_line_progress = None, 0
GLOW_DURATION = 15

# === Classes ===
class ConfettiParticle:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.size = random.randint(5, 10)
        self.color = random.choice([(255, 105, 180), (0, 191, 255), (255, 215, 0), (144, 238, 144)])
        self.speed_x = random.uniform(1, 3) * direction
        self.speed_y = random.uniform(-2, 2)
        self.gravity = 0.1

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

# === Functions ===
def draw_gradient_background():
    for y in range(HEIGHT):
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_board():
    draw_gradient_background()
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, ROWS*SQUARE_SIZE), LINE_WIDTH)

def draw_figures():
    for r in range(ROWS):
        for c in range(COLS):
            center = (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2)
            if board[r][c] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
                pygame.draw.circle(screen, LINE_COLOR, center, CIRCLE_RADIUS-10, 5)
            elif board[r][c] == "X":
                offset = SPACE
                pygame.draw.line(screen, CROSS_COLOR, (c*SQUARE_SIZE+offset, r*SQUARE_SIZE+offset), (c*SQUARE_SIZE+SQUARE_SIZE-offset, r*SQUARE_SIZE+SQUARE_SIZE-offset), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (c*SQUARE_SIZE+offset, r*SQUARE_SIZE+SQUARE_SIZE-offset), (c*SQUARE_SIZE+SQUARE_SIZE-offset, r*SQUARE_SIZE+offset), CROSS_WIDTH)

def draw_glow_effect():
    for cell in glow_cells:
        r, c, sym, frame = cell
        if frame < GLOW_DURATION:
            alpha = int(255 * (1 - frame / GLOW_DURATION))
            color = CROSS_COLOR if sym == "X" else CIRCLE_COLOR
            surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, (*color, alpha), surf.get_rect(), border_radius=10)
            screen.blit(surf, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            cell[3] += 1
    glow_cells[:] = [c for c in glow_cells if c[3] < GLOW_DURATION]

def draw_restart_button():
    rect = pygame.Rect(WIDTH//2-100, HEIGHT-80, 200, 50)
    color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=15)
    text = BUTTON_FONT.render("Restart", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
    return rect

def draw_welcome_screen(glow_phase):
    draw_gradient_background()
    glow = int(127.5*(1+math.sin(glow_phase)))
    welcome_color = (glow, 0, glow)
    text1 = WELCOME_FONT.render("WELCOME TO", True, welcome_color)
    text2 = TITLE_FONT.render("Tic Tac Toe", True, (26, 214, 26))
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 80))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 215))
    rect = pygame.Rect(WIDTH//2-130, HEIGHT//2+160, 260, 80)
    color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=20)
    btn_text = BUTTON_FONT.render("Start", True, BUTTON_TEXT_COLOR)
    screen.blit(btn_text, (rect.centerx - btn_text.get_width()//2, rect.centery - btn_text.get_height()//2))
    return rect

def draw_spinning_xo(progress):
    icons = ['X', 'O', 'X', 'O']
    for i, sym in enumerate(icons):
        angle = -progress*5 + i*45
        x = 50 + (progress%200) + i*110
        y = 420 + 30*math.sin(progress/15+i)
        draw_rotated_symbol(sym, (x, y), angle)

def draw_rotated_symbol(symbol, center, angle):
    surf = pygame.Surface((100, 100), pygame.SRCALPHA)
    if symbol == 'X':
        pygame.draw.line(surf, CROSS_COLOR, (20,20), (70,70), 12)
        pygame.draw.line(surf, CROSS_COLOR, (20,70), (70,20), 12)
    else:
        pygame.draw.circle(surf, CIRCLE_COLOR, (40,40), 35, 12)
    rotated = pygame.transform.rotate(surf, angle)
    screen.blit(rotated, rotated.get_rect(center=center))

def draw_winning_line():
    global winning_line_progress
    if winning_line:
        (sc, sr), (ec, er) = winning_line
        x1, y1 = sc*SQUARE_SIZE+SQUARE_SIZE//2, sr*SQUARE_SIZE+SQUARE_SIZE//2
        x2, y2 = ec*SQUARE_SIZE+SQUARE_SIZE//2, er*SQUARE_SIZE+SQUARE_SIZE//2
        p = min(winning_line_progress/30, 1)
        cx, cy = x1 + (x2-x1)*p, y1 + (y2-y1)*p
        c1, c2 = (255, 0, 255), (0, 255, 255)
        t = math.sin(winning_line_progress/5)*0.5+0.5
        color = tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
        pygame.draw.line(screen, color, (x1, y1), (cx, cy), 15)
        winning_line_progress += 1

# === Game Logic ===
def check_winner():
    global game_over, winning_line
    for i in range(ROWS):
        if board[i].count(board[i][0]) == COLS and board[i][0]:
            game_over, winning_line = True, ((0,i),(2,i))
            return board[i][0]
    for i in range(COLS):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            game_over, winning_line = True, ((i,0),(i,2))
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        game_over, winning_line = True, ((0,0),(2,2))
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        game_over, winning_line = True, ((2,0),(0,2))
        return board[0][2]

def check_draw():
    return all(all(row) for row in board)

def restart_game():
    global board, player, game_over, glow_cells, winning_line, winning_line_progress
    global win_sound_played, draw_sound_played, confetti_particles, confetti_spawned
    board = [[None]*COLS for _ in range(ROWS)]
    player, game_over = "X", False
    glow_cells.clear()
    winning_line, winning_line_progress = None, 0
    win_sound_played = draw_sound_played = confetti_spawned = False
    confetti_particles.clear()
    start_sound.play()

# === Main Loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    glow_phase += 0.05

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if welcome_screen and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_welcome_screen(glow_phase).collidepoint(event.pos):
                start_animation = True
                start_sound.play()
        elif not welcome_screen and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_restart_button().collidepoint(event.pos):
                restart_game()
            elif not game_over:
                mx, my = event.pos
                if my < ROWS * SQUARE_SIZE:
                    r, c = my//SQUARE_SIZE, mx//SQUARE_SIZE
                    if not board[r][c]:
                        board[r][c] = player
                        glow_cells.append([r, c, player, 0])
                        (x_sound if player=="X" else o_sound).play()
                        player = "O" if player=="X" else "X"

    if welcome_screen:
        draw_welcome_screen(glow_phase)
        if start_animation:
            draw_spinning_xo(animation_progress)
            animation_progress += 1
            if animation_progress > 120:
                welcome_screen = False
                pygame.mixer.music.stop()
    else:
        draw_board()
        draw_glow_effect()
        for particle in confetti_particles:
            particle.update()
            particle.draw(screen)
        draw_figures()

        winner = check_winner()
        if winner:
            screen.blit(MAIN_FONT.render(f"{winner} wins!", True, (55,204,85)), (WIDTH//2-150, HEIGHT//2-40))
            draw_winning_line()
            if not confetti_spawned:
                for _ in range(50):
                    confetti_particles += [ConfettiParticle(0, random.randint(0, HEIGHT//2), 1),
                                           ConfettiParticle(WIDTH, random.randint(0, HEIGHT//2), -1)]
                confetti_spawned = True
            if not win_sound_played:
                win_sound.play()
                win_sound_played = True
        elif check_draw():
            screen.blit(MAIN_FONT.render("Draw!", True, (255,165,0)), (WIDTH//2-120, HEIGHT//2-90))
            if not draw_sound_played:
                draw_sound.play()
                draw_sound_played = True

        draw_restart_button()

    pygame.display.update()

pygame.quit()
sys.exit()
