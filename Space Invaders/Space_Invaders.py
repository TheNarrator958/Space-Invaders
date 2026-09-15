import sys
import pygame

# pygame setup
#region
pygame.init()

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()
FPS = 60

font_large = pygame.font.SysFont(None, 80)
font_small = pygame.font.SysFont(None, 40)
#endregion

# game state
#region
score = 0
game_over = False
game_won = False
#endregion

# player
# region
player_x = SCREEN_WIDTH // 2
player_y = (SCREEN_HEIGHT // 2) + 325
player_radius = 20
player_speed = 5
#endregion

# bullet
#region
bullet_radius = 5
bullet_speed = 10
bullets = []

space_was_pressed = False
#endregion

# enemies
#region
enemy_rows = 4
enemy_columns = 3

enemy_radius = 15
enemy_spacing_x = 80
enemy_spacing_y = 60
enemy_start_x = 200
enemy_start_y = 80

enemies = []
for row in range(enemy_rows):
    for col in range(enemy_columns):
        ex = enemy_start_x + col * enemy_spacing_x
        ey = enemy_start_y + row * enemy_spacing_y
        enemies.append([ex, ey])

enemy_speed_x = 2
enemy_direction = 1 # 1 = right, -1 = left
enemy_drop_amount = 30
#endregion

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    if not game_over and not game_won:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        player_x = max(player_radius, min(SCREEN_WIDTH - player_radius, player_x))
        player_y = max(player_radius, min(SCREEN_HEIGHT - player_radius, player_y))

        if keys[pygame.K_SPACE] and not space_was_pressed:
            bullets.append([player_x, player_y - 20])
        space_was_pressed = keys[pygame.K_SPACE]

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            pygame.draw.circle(screen, (255, 255, 255), (bullet[0], bullet[1]), bullet_radius)

            if bullet[1] < 0:
                bullets.remove(bullet)

            for enemy in enemies[:]:
                dx = bullet[0] - enemy[0]
                dy = bullet[1] - enemy[1]
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < bullet_radius + enemy_radius:
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 10
                    break

        hit_edge = False
        for enemy in enemies:
            enemy[0] += enemy_speed_x * enemy_direction
            if enemy[0] <= enemy_radius or enemy[0] >= SCREEN_WIDTH - enemy_radius:
                hit_edge = True

        if hit_edge:
            enemy_direction *= -1
            for enemy in enemies:
                enemy[1] += enemy_drop_amount

        for enemy in enemies:
            pygame.draw.circle(screen, (50, 255, 50), (enemy[0], enemy[1]), enemy_radius)

        for enemy in enemies:
            if enemy[1] + enemy_radius >= player_y - player_radius:
                game_over = True

        if len(enemies) == 0 and not game_over:
            game_won = True

        pygame.draw.circle(screen, (255, 50, 50), (player_x, player_y), player_radius)
    else:
        message = "YOU WIN" if game_won else "GAME OVER"
        color = (50, 255, 50) if game_won else (255, 50, 50)
        text_surface = font_large.render(message, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(text_surface, text_rect)

        restart_surface = font_small.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(restart_surface, restart_rect)

        if keys[pygame.K_r]:
            player_x = SCREEN_WIDTH // 2
            bullets.clear()
            enemies.clear()
            for row in range(enemy_rows):
                for col in range(enemy_columns):
                    ex = enemy_start_x + col * enemy_spacing_x
                    ey = enemy_start_y + row * enemy_spacing_y
                    enemies.append([ex, ey])
            enemy_direction = 1
            score = 0
            game_over = False
            game_won = False

    score_surface = font_small.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (20, 20))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()