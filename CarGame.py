import pygame
import random
import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
CAR_WIDTH = 50
CAR_HEIGHT = 100
ENEMY_WIDTH = int(50 * 1)  # Original width was 50
ENEMY_HEIGHT = int(100 * 1)  # Original height was 100

# Load background image
road_image = pygame.image.load(resource_path("assets/road.png"))
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen

# Load player car image
player_car_image = pygame.image.load(resource_path("assets/playercar.png"))
player_car_image = pygame.transform.scale(player_car_image, (CAR_WIDTH, CAR_HEIGHT))  # Scale to fit the car dimensions

# Load enemy car images
enemy_car_images = [
    pygame.image.load(resource_path("assets/Random_car1.png")),
    pygame.image.load(resource_path("assets/Random_car2.png")),
    pygame.image.load(resource_path("assets/Random_car3.png")),
    pygame.image.load(resource_path("assets/Random_car4.png"))  # Add the new car image
]

# Scale enemy car images to match the new dimensions
scaled_enemy_car_images = []
for i, image in enumerate(enemy_car_images):
    if i == 3:  # Random_car4 (index 3)
        # Scale Random_car4 by 25% larger
        scaled_image = pygame.transform.scale(image, (int(ENEMY_WIDTH * 1.25), int(ENEMY_HEIGHT * 1.25)))
    else:
        # Scale other cars normally
        scaled_image = pygame.transform.scale(image, (ENEMY_WIDTH, ENEMY_HEIGHT))
    scaled_enemy_car_images.append(scaled_image)

enemy_car_images = scaled_enemy_car_images

# Player car
player_car = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Enemy cars with random images
enemy_cars = []
enemy_car_sprites = []  # To store the corresponding image for each enemy

# Initialize score, high score, and level
score = 0
level = 1  # Start at level 1
font = pygame.font.Font(None, 36)

# Track the start time
start_time = pygame.time.get_ticks()

# File to store the high score
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    """Load the high score from a file."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(high_score):
    """Save the high score to a file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(high_score))

# Initialize high score
high_score = load_high_score()

def update_score_and_level():
    global score, level
    # Calculate the score based on the elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds
    score = elapsed_time
    # Update the level based on the score
    level = 1 + score // 10  # Increase the level every 10 seconds

# Variables for background movement
background_y = 0
background_speed = 5

def generate_enemy_cars():
    global enemy_cars, enemy_car_sprites
    enemy_cars = []
    enemy_car_sprites = []
    num_enemies = int(5 * (1 + (level - 1) * 0.10))  # Increase enemies by 10% per level

    for _ in range(num_enemies):
        while True:
            # Restrict spawning to the middle 70% of the screen
            spawn_x_min = int(SCREEN_WIDTH * 0.15)
            spawn_x_max = int(SCREEN_WIDTH * 0.85 - ENEMY_WIDTH)
            enemy_x = random.randint(spawn_x_min, spawn_x_max)
            enemy_y = random.randint(-600, -100)
            new_enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

            # Ensure no overlap with existing enemies
            if not any(new_enemy.colliderect(existing_enemy) for existing_enemy in enemy_cars):
                enemy_cars.append(new_enemy)
                # Assign a random image to this enemy
                enemy_car_sprites.append(random.choice(enemy_car_images))
                break

# Generate initial enemy cars
generate_enemy_cars()

def draw_objects():
    global background_y
    # Move the background
    background_y += background_speed
    if background_y >= SCREEN_HEIGHT:
        background_y = 0

    # Draw the moving background
    screen.blit(road_image, (0, background_y))
    screen.blit(road_image, (0, background_y - SCREEN_HEIGHT))
    
    # Draw the player car using the image
    screen.blit(player_car_image, (player_car.x, player_car.y))
    
    # Draw the enemy cars with their respective images
    for i, enemy in enumerate(enemy_cars):
        screen.blit(enemy_car_sprites[i], (enemy.x, enemy.y))  # Draw only the image, no rectangle
    
    # Draw the score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(level_text, (10, 70))

def move_enemies():
    global enemy_cars, enemy_car_sprites
    enemy_speed = 5 * (1 + (level - 1) * 0.10)  # Increase speed by 10% per level

    for enemy in enemy_cars:
        enemy.y += int(enemy_speed)  # Move the enemy car down
        if enemy.y > SCREEN_HEIGHT:  # If the car moves off the screen
            # Remove the car and its sprite
            index = enemy_cars.index(enemy)
            enemy_cars.pop(index)
            enemy_car_sprites.pop(index)

            # Generate a new enemy car
            spawn_x_min = int(SCREEN_WIDTH * 0.15)
            spawn_x_max = int(SCREEN_WIDTH * 0.85 - ENEMY_WIDTH)
            enemy_x = random.randint(spawn_x_min, spawn_x_max)
            enemy_y = random.randint(-600, -100)
            new_enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
            enemy_cars.append(new_enemy)
            enemy_car_sprites.append(random.choice(enemy_car_images))

def check_collision():
    for enemy in enemy_cars:
        if player_car.colliderect(enemy):
            return True
    return False

# Global variable to store the volume level
current_volume = 0.5  # Default volume level (50%)

def game_over_screen():
    global high_score, score, current_volume

    # Pause the ambient music
    pygame.mixer.music.pause()

    if score > high_score:
        high_score = score
        save_high_score(high_score)  # Save the new high score to the file

    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, BLUE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    pygame.mixer.music.unpause()  # Resume ambient music
                    return  # Exit the game over screen

def menu_screen():
    global running, current_volume
    paused = True

    # Pause the ambient music
    pygame.mixer.music.pause()

    # Load the special music file
    special_music = pygame.mixer.Sound(resource_path("assets/Dacinestiesaconduce.mp3"))
    special_music_playing = False  # Track if the special music is playing

    while paused:
        screen.fill(BLACK)
        menu_text = font.render("Game Paused", True, RED)
        resume_text = font.render("Press R to Resume", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)
        volume_text = font.render(f"Volume: {int(current_volume * 100)}%", True, WHITE)
        volume_up_text = font.render("Press UP to Increase Volume", True, WHITE)
        volume_down_text = font.render("Press DOWN to Decrease Volume", True, WHITE)
        special_music_text = font.render("Press S to Toggle Special Music", True, WHITE)

        # Display menu options
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        screen.blit(volume_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(volume_up_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        screen.blit(volume_down_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        screen.blit(special_music_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume the game
                    paused = False
                    pygame.mixer.music.unpause()  # Resume ambient music
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:  # Increase volume
                    current_volume = min(current_volume + 0.1, 1.0)  # Cap at 100%
                    pygame.mixer.music.set_volume(current_volume)
                elif event.key == pygame.K_DOWN:  # Decrease volume
                    current_volume = max(current_volume - 0.1, 0.0)  # Minimum 0%
                    pygame.mixer.music.set_volume(current_volume)
                elif event.key == pygame.K_s:  # Toggle special music
                    if not special_music_playing:
                        special_music.play(-1)  # Play special music in a loop
                        pygame.mixer.music.stop()  # Stop ambient noise
                        special_music_playing = True
                    else:
                        special_music.stop()  # Stop special music
                        pygame.mixer.music.play(-1)  # Resume ambient noise
                        special_music_playing = False

# Load and play ambient noise
pygame.mixer.init()  # Initialize the mixer
pygame.mixer.music.load(resource_path("assets/ambience.mp3"))  # Load the ambient noise file
pygame.mixer.music.set_volume(0.5)  # Set the volume (adjust as needed)
pygame.mixer.music.play(-1)  # Play the sound in a loop

# Load honk sound (MP3)
honk_sound = pygame.mixer.Sound(resource_path("assets/honk.mp3"))  # Load the honk sound

def draw_radio_interface(special_music_playing):
    """Draw the radio interface in the bottom-left corner."""
    radio_width = 150
    radio_height = 50
    radio_x = 10
    radio_y = SCREEN_HEIGHT - radio_height - 10

    # Draw the radio background
    pygame.draw.rect(screen, BLACK, (radio_x, radio_y, radio_width, radio_height))
    pygame.draw.rect(screen, WHITE, (radio_x, radio_y, radio_width, radio_height), 2)  # Border

    # Display the radio text
    radio_text = font.render("Radio: ON" if special_music_playing else "Radio: OFF", True, WHITE)
    screen.blit(radio_text, (radio_x + 10, radio_y + 10))


def handle_radio_click(mouse_pos, special_music_playing, special_music):
    """Handle clicks on the radio interface."""
    radio_width = 150
    radio_height = 50
    radio_x = 10
    radio_y = SCREEN_HEIGHT - radio_height - 10

    # Check if the click is within the radio area
    if radio_x <= mouse_pos[0] <= radio_x + radio_width and radio_y <= mouse_pos[1] <= radio_y + radio_height:
        if special_music_playing:
            special_music.stop()  # Stop the special music
            pygame.mixer.music.play(-1)  # Resume ambient noise
            return False  # Toggle off
        else:
            pygame.mixer.music.stop()  # Stop ambient noise
            special_music.play(-1)  # Play special music
            return True  # Toggle on
    return special_music_playing


# Load the special music file
special_music = pygame.mixer.Sound(resource_path("assets/Dacinestiesaconduce.mp3"))
special_music_playing = False  # Track if the special music is playing

# Game loop
running = True
player_speed = 5  # Default player speed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # Check if the 'H' key is pressed
                honk_sound.play()  # Play the honk sound
            if event.key == pygame.K_m:  # Open the menu
                menu_screen()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                special_music_playing = handle_radio_click(pygame.mouse.get_pos(), special_music_playing, special_music)

    # Adjust speed based on W and S keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Fast-forward movement
        player_speed = 10  # Increase speed
    elif keys[pygame.K_s]:  # Slow down movement
        player_speed = 2  # Decrease speed
    else:
        player_speed = 5  # Default speed

    # Player movement
    if keys[pygame.K_a] and player_car.x > 0:  # Move left
        player_car.x -= player_speed
    if keys[pygame.K_d] and player_car.x < SCREEN_WIDTH - CAR_WIDTH:  # Move right
        player_car.x += player_speed

    # Move enemies
    move_enemies()

    # Update the score and level based on survival time
    update_score_and_level()

    # Check for collisions
    if check_collision():
        game_over_screen()
        # Reset game state
        score = 0
        level = 1
        player_car.x = SCREEN_WIDTH // 2
        player_car.y = SCREEN_HEIGHT - CAR_HEIGHT - 10
        generate_enemy_cars()
        start_time = pygame.time.get_ticks()  # Reset the timer

    # Draw everything
    draw_objects()
    draw_radio_interface(special_music_playing)  # Draw the radio interface

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
