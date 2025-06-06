import pygame
import os

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames("assets")
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_frames(self, folder_path):
        frames = []
        for i in range(1, 10):  # goldCoin1.png до goldCoin9.png
            filename = f"goldCoin{i}.png"
            path = os.path.join(folder_path, filename)
            image = pygame.image.load(path).convert_alpha()
            frames.append(pygame.transform.scale(image, (32, 32)))  # масштабуй якщо треба
        return frames

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
