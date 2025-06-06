import pygame

class Camera:
    def __init__(self, screen_width, screen_height, level_width, level_height):
        self.offset = pygame.Vector2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_width = level_width
        self.level_height = level_height

    def update(self, target_rect):
        # Центруємо камеру на об'єкті (гравці)
        self.offset.x = target_rect.centerx - self.screen_width // 2
        self.offset.y = target_rect.centery - self.screen_height // 2

        # Обмеження камери, щоб не виходила за межі рівня
        self.offset.x = max(0, min(self.offset.x, self.level_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.level_height - self.screen_height))

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)
