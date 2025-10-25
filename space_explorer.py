import pygame
import random
import sys
import math

pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Adventure")

# Load background
bg_img = pygame.image.load("space_bg.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bg_x = 0
bg_speed = 2

# Load images
rocket_img = pygame.image.load("rocket.png").convert_alpha()
rocket_img = pygame.transform.scale(rocket_img, (60, 60))
asteroid_img = pygame.image.load("asteroid.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
planet_img = pygame.image.load("planet.png").convert_alpha()
planet_img = pygame.transform.scale(planet_img, (60, 60))
saturn_img = pygame.image.load("saturn.png").convert_alpha()
saturn_img = pygame.transform.scale(saturn_img, (60, 60))
shootingstar_img = pygame.image.load("shootingstar.png").convert_alpha()
shootingstar_img = pygame.transform.scale(shootingstar_img, (50, 50))
coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
lives = 3
rocket_x, rocket_y = WIDTH//2, HEIGHT - 120
rocket_speed = 7
floating_objects = []

# Spawn event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 500)

# Fonts
score_font = pygame.font.SysFont("Century Gothic", 28, bold=True)
lives_font = pygame.font.SysFont("Georgia", 28, bold=True)
gameover_font = pygame.font.SysFont("Orbitron", 60, bold=True)  # Elegant futuristic font
button_font = pygame.font.SysFont("Verdana", 28, bold=True)

# Colors
gameover_color = (0, 255, 255)  # neon cyan
button_bg = (70, 0, 120)         # deep purple
button_hover = (120, 0, 200)     # brighter purple
button_text = (255, 255, 255)

# Helper: draw glowing text
def draw_glow_text(text, font, base_color, glow_color, x, y):
    for offset in range(1, 4):
        shadow = font.render(text, True, glow_color)
        screen.blit(shadow, (x - offset, y - offset))
        screen.blit(shadow, (x + offset, y - offset))
        screen.blit(shadow, (x - offset, y + offset))
        screen.blit(shadow, (x + offset, y + offset))
    screen.blit(font.render(text, True, base_color), (x, y))

# Helper: 360° movement
def move_object(obj):
    angle = obj[3]
    speed = obj[2]
    obj[0] += math.cos(angle) * speed
    obj[1] += math.sin(angle) * speed
    if obj[0] < -100: obj[0] = WIDTH + 50
    if obj[0] > WIDTH + 100: obj[0] = -50
    if obj[1] < -100: obj[1] = HEIGHT + 50
    if obj[1] > HEIGHT + 100: obj[1] = -50

# Draw button with equal width
def draw_button(text, font, center_x, y, mouse_pos, width=None):
    label = font.render(text, True, button_text)
    padding_x = 20
    padding_y = 10
    w = width if width else label.get_width() + padding_x
    h = label.get_height() + padding_y
    rect = pygame.Rect(center_x - w//2, y, w, h)
    color = button_hover if rect.collidepoint(mouse_pos) else button_bg
    pygame.draw.rect(screen, color, rect, border_radius=15)
    screen.blit(label, (rect.x + (rect.width - label.get_width())//2, rect.y + (rect.height - label.get_height())//2))
    return rect, w

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Background
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    # Draw original background
    screen.blit(bg_img, (bg_x, 0))
    # Draw flipped background for smooth blending
    bg_img_flipped = pygame.transform.flip(bg_img, True, False)
    screen.blit(bg_img_flipped, (bg_x + WIDTH, 0))


    # Spawn floating objects
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_EVENT:
            obj_choice = random.choices(
                [asteroid_img, planet_img, saturn_img, shootingstar_img, coin_img],
                weights=[1,1,1,1,1.25], k=1
            )[0]
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            speed = random.uniform(0.5, 2.0)
            angle = random.uniform(0, 2*math.pi)
            floating_objects.append([x, y, speed, angle, obj_choice])

    # Rocket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_x > 0: rocket_x -= rocket_speed
    if keys[pygame.K_RIGHT] and rocket_x < WIDTH - 60: rocket_x += rocket_speed
    if keys[pygame.K_UP] and rocket_y > 0: rocket_y -= rocket_speed
    if keys[pygame.K_DOWN] and rocket_y < HEIGHT - 60: rocket_y += rocket_speed

    rocket_rect = pygame.Rect(rocket_x, rocket_y, 60, 60)
    screen.blit(rocket_img, (rocket_x, rocket_y))

    # Update floating objects
    for obj in floating_objects[:]:
        move_object(obj)
        screen.blit(obj[4], (obj[0], obj[1]))
        if obj[4] == coin_img and rocket_rect.colliderect(pygame.Rect(obj[0], obj[1], 40, 40)):
            score += 10
            floating_objects.remove(obj)
        elif obj[4] != coin_img and rocket_rect.colliderect(pygame.Rect(obj[0], obj[1], obj[4].get_width(), obj[4].get_height())):
            lives -= 1
            floating_objects.remove(obj)

    # Display lives & score
    draw_glow_text(f"Lives: {lives}", lives_font, (0, 255, 200), (0, 100, 100), 10, 10)
    draw_glow_text(f"Score: {score}", score_font, (255, 255, 0), (255, 150, 0), WIDTH - 180, 10)

    # Game over
    if lives <= 0:
        center_x = WIDTH // 2
        y_start = HEIGHT // 2 - 120

        # Centered text
        draw_glow_text("GAME OVER", gameover_font, gameover_color, (0, 128, 255), center_x - 110, y_start)
        draw_glow_text(f"Final Score: {score}", score_font, (255, 255, 0), (255, 150, 0), center_x - 80, y_start + 80)

        # Buttons stacked vertically
        mouse_pos = pygame.mouse.get_pos()
        restart_button, btn_width = draw_button("Restart", button_font, center_x, y_start + 150, mouse_pos)
        quit_button, _ = draw_button("Quit", button_font, center_x, y_start + 230, mouse_pos, width=btn_width)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        score = 0
                        lives = 3
                        floating_objects.clear()
                        rocket_x, rocket_y = WIDTH//2, HEIGHT - 120
                        waiting = False
                    if quit_button.collidepoint(event.pos):
                        waiting = False
                        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
