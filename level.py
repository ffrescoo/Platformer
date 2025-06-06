import pygame
from tile import Tile
from spritesheet import SpriteSheet

class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.tile_size = 32  # Розмір тайла на екрані
        self.tiles = pygame.sprite.Group()
        
        # Завантаження тайлсету
        self.spritesheet = SpriteSheet("assets/tile.png")
        
        # Розмір оригінальних тайлів у спрайтшіті
        self.original_tile_size = 16
        self.scale = 2  # Масштаб для збільшення тайлів
        
       
        # Перший ряд (y=0) - різні варіанти землі/трави
        self.grass_tile = self.spritesheet.get_image(
            226, 88, self.original_tile_size, self.original_tile_size, self.scale
        )  # Зелена трава з другої позиції
        
        # Другий ряд (y=16) - платформи
        self.platform_left = self.spritesheet.get_image(
            160, 32, self.original_tile_size, self.original_tile_size, self.scale
        )
        self.platform_middle = self.spritesheet.get_image(
            180, 32, self.original_tile_size, self.original_tile_size, self.scale
        )
        self.platform_right = self.spritesheet.get_image(
            190, 32, self.original_tile_size, self.original_tile_size, self.scale
        )
        
        # Третій ряд (y=32) - земля під травою
        self.dirt_tile = self.spritesheet.get_image(
            170, 16, self.original_tile_size, self.original_tile_size, self.scale
        )
        
        # Четвертий ряд (y=48) - камінь
        self.stone_tile = self.spritesheet.get_image(
            16, 48, self.original_tile_size, self.original_tile_size, self.scale
        )
        
        # Простий рівень з одним типом блоків
        level_map = [
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "         XXXX                           ",
            "                                        ",
            "     XXXX          XX       XXXXXX      ",
            "                                        ",
            "  XX         XX                         ",
            "                            XX          ",
            "XXXX      XXXXX      XXX    XXXX        ",        
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]
        
        self.create_level(level_map)

    def create_level(self, level_map):
        """Створення рівня з карти з розумними платформами"""
        for row_index, row in enumerate(level_map):
            col_index = 0
            while col_index < len(row):
                if row[col_index] == "X":
                    # Знаходимо довжину платформи
                    platform_start = col_index
                    platform_length = 0
                    
                    # Рахуємо довжину послідовних X
                    while (col_index < len(row) and row[col_index] == "X"):
                        platform_length += 1
                        col_index += 1
                    
                    # Створюємо платформу з правильними краями
                    self.create_platform(platform_start, row_index, platform_length)
                else:
                    col_index += 1

    def create_platform(self, start_col, row, length):
        """Створення платформи з правильними лівими, середніми та правими частинами"""
        for i in range(length):
            x = (start_col + i) * self.tile_size
            y = row * self.tile_size
            
            # Вибираємо правильний тайл в залежності від позиції
            if length == 1:
                # Одинокий блок - використовуємо середній тайл
                tile_image = self.grass_tile
            elif i == 0:
                # Лівий край платформи
                tile_image = self.platform_left
            elif i == length - 1:
                # Правий край платформи
                tile_image = self.platform_right
            else:
                # Середина платформи
                tile_image = self.platform_middle
            
            tile = Tile(x, y, tile_image)

            self.tiles.add(tile)

    def create_simple_level(self):
        """Створення простого рівня з одним типом тайлів для тестування"""
        self.tiles.empty()  # Очищуємо існуючі тайли
        
        # Простий рівень тільки з травою
        simple_map = [
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "         XXXX                           ",
            "                                        ",
            "     XXXX          XX                   ",
            "                                        ",
            "  XX         XX                         ",
            "                            XX          ",
            "XXXX      XXXXX      XX                 ",        
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]
        
        for row_index, row in enumerate(simple_map):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    tile = Tile(self.grass_tile, x, y)
                    self.tiles.add(tile)

    def check_collision(self, player):
        """Перевірка колізій з тайлами"""
        collisions = []
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                collisions.append(tile)
        return collisions

    def handle_collision(self, player):
        """Обробка колізій гравця з тайлами"""
        # Перевіряємо колізії після руху
        collisions = self.check_collision(player)
        
        for tile in collisions:
            # Вертикальні колізії (приземлення та удар головою)
            if player.vel_y > 0:  # Падіння вниз
                player.rect.bottom = tile.rect.top
                player.vel_y = 0
                player.on_ground = True
            elif player.vel_y < 0:  # Стрибок вгору
                player.rect.top = tile.rect.bottom
                player.vel_y = 0

    def draw(self):
        """Відображення всіх тайлів"""
        self.tiles.draw(self.display_surface)

    def get_tiles(self):
        """Отримання групи тайлів"""
        return self.tiles

    def toggle_platform_style(self):
        """Перемикання між розумними платформами та простими блоками"""
        if hasattr(self, '_simple_mode'):
            self._simple_mode = not self._simple_mode
        else:
            self._simple_mode = True
            
        if self._simple_mode:
            self.create_simple_level()
        else:
            self.__init__(self.display_surface)