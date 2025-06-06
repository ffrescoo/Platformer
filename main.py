import pygame
from level import Level
from player import Player
from camera import Camera

pygame.init()

# Створення вікна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Ініціалізація рівня та гравця
level = Level(screen)
level_width = level.level_width
level_height = level.level_height
background_image = pygame.image.load("assets/background.png").convert()

camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
player = Player((100, 100))

clock = pygame.time.Clock()
running = True

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення логіки - передаємо розміри рівня замість екрану
    player.update(keys, level.get_tiles(), level_width, level_height)
    level.update()
    camera.update(player.rect)

    # Малювання
    screen.blit(background_image, (0, 0))
    level.draw(camera)
    screen.blit(player.image, camera.apply(player.rect))

    pygame.display.update()
    clock.tick(60)

pygame.quit()