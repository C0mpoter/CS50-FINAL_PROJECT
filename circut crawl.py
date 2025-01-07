import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circuit Crawl")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Snake initialization
snake = [(WIDTH // 2, HEIGHT // 2)]  # Snake starts in the center
direction = "RIGHT"
grow = False

# Energy node
energy = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE, 
          random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

# Obstacles
obstacles = []

# Score
score = 0
high_score = 0  # Initialize high score

# Fonts
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)
button_font = pygame.font.SysFont("Arial", 36)

# Game loop flag
running = True
move_delay = 50  # Delay between snake movements (in milliseconds)
last_move_time = pygame.time.get_ticks()  # Time when the snake last moved

# Function to create and handle buttons
def draw_button(text, rect, color, hover_color):
    # Draw the button
    pygame.draw.rect(screen, color, rect)
    # Draw the text on the button
    button_text = button_font.render(text, True, WHITE)
    screen.blit(button_text, (rect.centerx - button_text.get_width() // 2, rect.centery - button_text.get_height() // 2))
    
    # Check if the mouse is hovering over the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, rect, 5)  # Highlight the button when hovered
    return rect.collidepoint(mouse_x, mouse_y)

# Game over screen
def game_over():
    screen.fill(BLACK)
    
    # Draw the "You Died" text
    death_text = large_font.render("You Died", True, WHITE)
    screen.blit(death_text, (WIDTH // 2 - death_text.get_width() // 2, HEIGHT // 3))
    
    # Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 60))
    
    # Draw the high score
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 3 + 100))
    
    # Move the buttons lower so they don't overlap with the score and high score
    replay_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 50)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 220, 300, 50)
    
    replay_hover = draw_button("Replay", replay_button_rect, BLUE, GREEN)
    quit_hover = draw_button("Quit", quit_button_rect, RED, GREEN)
    
    pygame.display.flip()
    
    return replay_hover, quit_hover, replay_button_rect, quit_button_rect


# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control the snake's movement speed
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time >= move_delay:
        last_move_time = current_time

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        if keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        if keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        if keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        # Move the snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Check for collision with energy
        if new_head == energy:
            score += 10
            grow = True
            energy = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE, 
                      random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            # Add a new obstacle
            obstacles.append((random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE, 
                              random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE))
        
        if not grow:
            snake.pop()
        else:
            grow = False

        # Check for collisions with walls or itself
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake[1:]):
            running = False

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if new_head == obstacle:
                running = False

        # Draw everything
        screen.fill(BLACK)

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Draw energy
        pygame.draw.rect(screen, BLUE, (*energy, CELL_SIZE, CELL_SIZE))

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (*obstacle, CELL_SIZE, CELL_SIZE))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # If the game ends, show the death screen
    if not running:
        # Update the high score if necessary
        if score > high_score:
            high_score = score
        
        replay_hover, quit_hover, replay_button_rect, quit_button_rect = game_over()
        
        # Wait for the user to either play again or quit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    running = False  # Quit the game
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for button clicks
                    if replay_button_rect.collidepoint(event.pos):
                        # Reset the game
                        snake = [(WIDTH // 2, HEIGHT // 2)]
                        direction = "RIGHT"
                        grow = False
                        obstacles.clear()
                        score = 0
                        running = True
                        waiting_for_input = False
                    
                    elif quit_button_rect.collidepoint(event.pos):
                        # Quit the game
                        waiting_for_input = False
                        running = False
        
        continue

    # Control frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
