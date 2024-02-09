import pygame
import pygame_gui
import random
import time

# Constants
GRID_SIZE = 4
CELL_SIZE = 150
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
FPS = 60

# Colors
BACKGROUND_COLOR = (250, 248, 239)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)
GRID_LINE_COLOR = (187, 173, 160)

# Initialize Pygame
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Global variables
score = 0
high_score = 0
start_screen = True
game_over = False

class Button:
    def __init__(self, text, position, size):
        self.rect = pygame.Rect(position, size)
        self.text = text
        self.clicked = False
        self.hovered = False
        self.default_color = (187, 173, 160)
        self.hover_color = (150, 150, 150)
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def draw_gradient_background():
    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    colors = [(250, 248, 239), (244, 240, 228), (250, 248, 239)]
    pygame.draw.rect(gradient_surface, colors[0], (0, 0, WIDTH, HEIGHT))
    for i in range(HEIGHT // 2):
        color = [(a * (HEIGHT // 2 - i) + b * i) // (HEIGHT // 2) for a, b in zip(colors[0], colors[1])]
        pygame.draw.rect(gradient_surface, color, (0, i, WIDTH, 1))
    screen.blit(gradient_surface, (0, 0))

def draw_grid():
    screen.fill(BACKGROUND_COLOR)  # Fill the screen with background color
    draw_gradient_background()  # Draw gradient background
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

def draw_tile(row, col, value):
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.rect(screen, TILE_COLORS[value], (x, y, CELL_SIZE, CELL_SIZE))
    if value != 0:
        text = font.render(str(value), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
        screen.blit(text, text_rect)

def initialize_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

def move(board, direction):
    global score
    if direction == 'up':
        for col in range(GRID_SIZE):
            column = [board[row][col] for row in range(GRID_SIZE)]
            merged_column, merged_score = merge(column)
            score += merged_score
            for row in range(GRID_SIZE):
                board[row][col] = merged_column[row] if row < len(merged_column) else 0
    elif direction == 'down':
        for col in range(GRID_SIZE):
            column = [board[row][col] for row in range(GRID_SIZE - 1, -1, -1)]
            merged_column, merged_score = merge(column)
            score += merged_score
            for row in range(GRID_SIZE - 1, -1, -1):
                if merged_column:
                    board[row][col] = merged_column.pop(0)
                else:
                    board[row][col] = 0
    elif direction == 'left':
        for row in range(GRID_SIZE):
            merged_row, merged_score = merge(board[row])
            score += merged_score
            for col in range(GRID_SIZE):
                board[row][col] = merged_row[col] if col < len(merged_row) else 0
    elif direction == 'right':
        for row in range(GRID_SIZE):
            merged_row, merged_score = merge(board[row][::-1])
            score += merged_score
            for col in range(GRID_SIZE):
                board[row][col] = merged_row[col] if col < len(merged_row) else 0

def merge(line):
    merged_line = []
    line = [value for value in line if value != 0]
    merged_score = 0
    for i in range(len(line)):
        if i < len(line) - 1 and line[i] == line[i + 1]:
            merged_line.append(line[i] * 2)
            merged_score += line[i] * 2
            line[i + 1] = 0
        elif line[i] != 0:
            merged_line.append(line[i])
    while len(merged_line) < len(line):
        merged_line.append(0)
    return merged_line, merged_score

def is_game_over(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 2048:
                return True

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            if board[row][col] == board[row][col + 1] or board[col][row] == board[col + 1][row]:
                return False

    return True

def draw_opening_screen(image_path):
    # Load the opening image
    opening_image = pygame.image.load(image_path)
    opening_image = pygame.transform.scale(opening_image, (WIDTH, HEIGHT))
    
    # Blit the opening image onto the screen
    screen.blit(opening_image, (0, 0))
    
    pygame.display.flip()
    
    # Delay for 3 seconds
    time.sleep(3)

def draw_game_start_screen():
    screen.fill(BACKGROUND_COLOR)

    # Add a stylish title
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("2048 Game", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    # Create and draw the start button
    start_button = Button("Start", (WIDTH // 2 - 75, HEIGHT // 2), (150, 50))
    start_button.draw(screen)

    pygame.display.flip()

def draw_game_over_screen():
    global score, high_score
    if score > high_score:
        high_score = score

    screen.fill(BACKGROUND_COLOR)

    # Add a stylish game over title
    game_over_title_font = pygame.font.SysFont(None, 60)
    game_over_text = game_over_title_font.render("Game Over!", True, TEXT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4 - game_over_text.get_height() // 2))

    # Display scores
    score_text = font.render("Your Score: " + str(score), True, TEXT_COLOR)
    high_score_text = font.render("High Score: " + str(high_score), True, TEXT_COLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 30))

    # Create and draw the retry button
    retry_button = Button("Retry", (WIDTH // 2 - 75, HEIGHT // 2 + 80), (150, 50))
    retry_button.draw(screen)

    pygame.display.flip()

def draw_grid_lines():
    # Draw horizontal grid lines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
    
    # Draw vertical grid lines
    for j in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT), 2)

def main():
    global score, high_score, start_screen, game_over

    # Path to the opening image
    opening_image_path = "img/opening_image.png"

    # Draw the opening screen
    draw_opening_screen(opening_image_path)
    
    # Draw the game start screen
    draw_game_start_screen()

    # Create buttons
    start_button = Button("Start", (WIDTH // 2 - 75, HEIGHT // 2), (150, 50))
    retry_button = Button("Retry", (WIDTH // 2 - 75, HEIGHT // 2 + 80), (150, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.rect.collidepoint(event.pos):
                        start_screen = False
                        score = 0
                        board = initialize_board()
                        draw_grid()

            elif game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_button.rect.collidepoint(event.pos):
                        game_over = False
                        score = 0
                        board = initialize_board()
                        draw_grid()

                        # Add a delay before starting the game to enhance user experience
                        pygame.time.delay(500)

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move(board, 'up')
                    elif event.key == pygame.K_DOWN:
                        move(board, 'down')
                    elif event.key == pygame.K_LEFT:
                        move(board, 'left')
                    elif event.key == pygame.K_RIGHT:
                        move(board, 'right')
                    add_new_tile(board)

        if not start_screen and not game_over:
            screen.fill(BACKGROUND_COLOR)  # Fill the screen with background color
            draw_gradient_background()  # Draw gradient background

            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    draw_tile(i, j, board[i][j])  # Draw the tiles

            draw_grid_lines()  # Draw the grid lines

            score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

            if is_game_over(board):
                game_over = True
                draw_game_over_screen()

        elif start_screen:
            # Draw the start button
            start_button.draw(screen)

        elif game_over:
            # Draw the retry button
            retry_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
