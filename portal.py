import pygame
import os

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=2):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        self.animation_speed = 0.15

        # Завантажуємо спрайтшіт порталу
        portal_sheet = pygame.image.load(os.path.join("assets", "portal.png")).convert_alpha()

        frame_width, frame_height = 32, 32
        for i in range(5):
            frame = portal_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
