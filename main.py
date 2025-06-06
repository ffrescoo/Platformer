import pygame
from level import Level
from player import Player

pygame.init()

# Створення вікна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

tile_img = pygame.image.load("assets/tile.png").convert_alpha()

# Ініціалізація рівня та гравця
level = Level(screen)
player = Player((100, 100))

clock = pygame.time.Clock()
running = True

while running:
    keys = pygame.key.get_pressed()
    level.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 150, 255))  # Фон
    level.draw()
    player.update(keys, level.get_tiles())
    screen.blit(player.image, player.rect)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
