import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y): 
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
