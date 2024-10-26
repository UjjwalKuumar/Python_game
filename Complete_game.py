import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen and Level Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LEVEL_WIDTH, LEVEL_HEIGHT = 2400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player Settings
player = pygame.Rect(100, SCREEN_HEIGHT - 50, 50, 50)  # Player rect
player_health = 100
player_speed = 5
bullets = []
bullet_speed = 10
bullets_fired = 0
score = 0

# Enemy Settings
enemies = []
enemy_spawn_rate = 1000  # milliseconds
enemy_health = 20
enemy_damage = 5

# Game State
clock = pygame.time.Clock()
running = True
game_started = False
start_button_rect = pygame.Rect(350, 250, 100, 50)

def draw_start_button():
    pygame.draw.rect(screen, GREEN, start_button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, WHITE)
    screen.blit(text, (start_button_rect.x + 10, start_button_rect.y + 10))

def spawn_enemy():
    enemy_x = random.randint(LEVEL_WIDTH, LEVEL_WIDTH + 200)  # Spawn off-screen
    enemy_y = SCREEN_HEIGHT - 60  # Above the ground
    enemies.append(pygame.Rect(enemy_x, enemy_y, 50, 50))

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def move_enemies():
    for enemy in enemies:
        enemy.x -= 2  # Move enemies to the left
        if enemy.x < 0:  # Remove off-screen enemies
            enemies.remove(enemy)

def draw_health_bar():
    pygame.draw.rect(screen, GREEN, (10, 10, player_health, 20))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 40))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet)

# Main Game Loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k and game_started:  # Jump
                pass  # Jumping not implemented yet
            elif event.key == pygame.K_l and game_started:  # Shoot
                bullet = pygame.Rect(player.x + 25, player.y, 10, 5)
                bullets.append(bullet)
                bullets_fired += 1
            elif event.key == pygame.K_j and game_started:  # Run
                player.x += player_speed

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                game_started = True

    if game_started:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < LEVEL_WIDTH - player.width:
            player.x += player_speed

        # Spawn enemies
        if pygame.time.get_ticks() % enemy_spawn_rate < 30:  # Roughly once per second
            spawn_enemy()

        # Move enemies
        move_enemies()

        # Check for bullet collisions
        for bullet in bullets[:]:
            bullet.x += bullet_speed
            if bullet.x > SCREEN_WIDTH:  # Remove off-screen bullets
                bullets.remove(bullet)

            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    score += 1
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Draw everything
        draw_enemies()
        draw_health_bar()
        draw_score()
        draw_bullets()

    else:
        draw_start_button()

    pygame.draw.rect(screen, BLUE, player)  # Draw the player
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
