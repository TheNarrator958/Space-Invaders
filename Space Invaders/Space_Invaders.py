import sys
import pygame

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()
FPS = 60

# player
# region
player_x = SCREEN_WIDTH // 2
player_y = (SCREEN_HEIGHT // 2) + 400
player_radius = 20
player_speed = 5
#endregion

# bullet
bullet_radius = 5
bullet_speed = 10
bullets = []

space_was_pressed = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

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

    pygame.draw.circle(screen, (255, 50, 50), (player_x, player_y), player_radius)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()