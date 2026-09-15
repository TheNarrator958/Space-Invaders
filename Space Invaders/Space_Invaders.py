import sys
import random
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
round_number = 1
game_over = False
invulnerable_timer = 0 # brief invincibility after losing a life
#endregion

# player
# region
player_start_x = SCREEN_WIDTH // 2
player_start_y = (SCREEN_HEIGHT // 2) + 325
player_x = player_start_x
player_y = player_start_y
player_radius = 20
player_speed = 5
player_lives = 3
#endregion

# bullet
#region
bullet_radius = 5
bullet_speed = 10
bullets = []
#endregion

# enemy bullets
enemy_bullet_radius = 5
enemy_bullet_speed = 7
enemy_bullets = []
enemy_shoot_chance = 0.003 # per enemy, per frame

# enemies
#region
enemy_rows = 4
enemy_columns = 3

enemy_radius = 15
enemy_spacing_x = 80
enemy_spacing_y = 60
enemy_start_x = 200
enemy_start_y = 80

def make_enemy_grid():
    grid = []
    for row in range(enemy_rows):
        for col in range(enemy_columns):
            ex = enemy_start_x + col * enemy_spacing_x
            ey = enemy_start_y + row * enemy_spacing_y
            grid.append([ex, ey])
    return grid

enemies = make_enemy_grid()
enemy_base_speed = 2
enemy_speed_x = enemy_base_speed
enemy_direction = 1 # 1 = right, -1 = left
enemy_drop_amount = 30
#endregion

# generic
space_was_pressed = False
running = True

def reset_after_hit():
    global player_x, bullets, enemy_bullets, invulnerable_timer
    player_x = player_start_x
    bullets = []
    enemy_bullets = []
    invulnerable_timer = FPS * 1    # 1 second

def start_new_round():
    global enemies, enemies_speed_x, enemy_direction, round_number, bullets, enemy_bullets
    round_number += 1
    enemies = make_enemy_grid()
    enemy_speed_x = enemy_base_speed + (round_number - 1) * 0.5
    enemy_direction = 1
    bullets = []
    enemy_bullets = []

def full_reset():
    global player_x, player_lives, bullets, enemy_bullets, enemies
    global enemy_speed_x, enemy_direction, score, round_number, game_over, invulnerable_timer
    player_x = player_start_x
    player_lives = 3
    bullets = []
    enemy_bullets = []
    enemies = make_enemy_grid
    enemy_direction = 1
    score = 0
    round_number = 1
    game_over = False
    invulnerable_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    if not game_over:
        if invulnerable_timer > 0:
            invulnerable_timer -= 1

        # player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        player_x = max(player_radius, min(SCREEN_WIDTH - player_radius, player_x))
        player_y = max(player_radius, min(SCREEN_HEIGHT - player_radius, player_y))

        # player shooting
        if keys[pygame.K_SPACE] and not space_was_pressed:
            bullets.append([player_x, player_y - 20])
        space_was_pressed = keys[pygame.K_SPACE]

        # move player bullets | check enemy hits
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

        # move enemy swarm
        hit_edge = False
        for enemy in enemies:
            enemy[0] += enemy_speed_x * enemy_direction
            if enemy[0] <= enemy_radius or enemy[0] >= SCREEN_WIDTH - enemy_radius:
                hit_edge = True

        if hit_edge:
            enemy_direction *= -1
            for enemy in enemies:
                enemy[1] += enemy_drop_amount

        # enemies shoot back
        for enemy in enemies:
            if random.random() < enemy_shoot_chance:
                enemy_bullets.append([enemy[0], enemy[1] + enemy_radius])

        # draw enemies | check if they have reached the player
        reached_player = False
        for enemy in enemies:
            pygame.draw.circle(screen, (50, 255, 50), (enemy[0], enemy[1]), enemy_radius)
            if enemy[1] + enemy_radius >= player_y - player_radius:
                game_over = True

        # move enemy bullets | check player hits
        for ebullet in enemy_bullets[:]:
            ebullet[1] += enemy_bullet_speed
            pygame.draw.circle(screen, (255, 200, 50), (ebullet[0], ebullet[1]), enemy_bullet_radius)

            if ebullet[1] > SCREEN_HEIGHT:
                enemy_bullets.remove(ebullet)
                continue

            if invulnerable_timer <= 0:
                dx = ebullet[0] - player_x
                dy = ebullet[1] - player_y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < enemy_bullet_radius + player_radius:
                    enemy_bullets.remove(ebullet)
                    plaer_lives -= 1
                    if player_lives <= 1:
                        game_over = True
                    else:
                        reset_after_hit()
                    break

        # losing a life if enemies reach the player row
        if reached_player and not game_over:
            player_lives -= 1
            if player_lives <= 0:
                game_over = True
            else:
                reset_after_hit()
                enemies = make_enemy_grid() # push the wave back

        # round clear -> next round
        if len(enemies) == 0 and not game_over:
            start_new_round()

        # draw player (flicker while invulnerable)
        if invulnerable_timer <= 0 or invulnerable_timer % 10 < 5:
            pygame.draw.circle(screen, (255, 50, 50), (player_x, player_y), player_radius)
    else:
        text_surface = font_large.render("GAME OVER", True, (255, 50, 50))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(text_surface, text_rect)

        final_surface = font_small.render(
            f"Final Score: {score}   Reached Round: {round_number}", True, (255, 255, 255)
        )
        final_rect = final_surface.get_rect(center=(SCREEN_WDITH // 2, SCREEN_HEIGHT // 2))
        screen.blit(final_surface, final_rect)

        if keys[pygame.K_r]:
            full_reset
    
    # HUD
    score_surface = font_small.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (20, 20))

    lives_surface = font_small.render(f"Lives: {player_lives}", True, (255, 255, 255))
    screen.blit(lives_surface, (20, 60))

    round_surface = font_small.render(f"Round: {round_number}", True, (255, 255, 255))
    screen.blit(round_surface, (20, 100))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()