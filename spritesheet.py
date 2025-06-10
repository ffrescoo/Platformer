import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scale=1):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), pygame.Rect(x, y, width, height))
        if scale != 1:
            image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
