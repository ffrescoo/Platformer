import pygame
from tile import Tile
from coin import Coin
from spritesheet import SpriteSheet

class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.tile_size = 32
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.coins_collected = 0

        self.spritesheet = SpriteSheet("assets/tile.png")
        self.original_tile_size = 16
        self.scale = 2

        # Завантаження платформ
        self.grass_tile = self.spritesheet.get_image(226, 88, 16, 16, self.scale)
        self.platform_left = self.spritesheet.get_image(160, 32, 16, 16, self.scale)
        self.platform_middle = self.spritesheet.get_image(180, 32, 16, 16, self.scale)
        self.platform_right = self.spritesheet.get_image(190, 32, 16, 16, self.scale)
        self.dirt_tile = self.spritesheet.get_image(170, 16, 16, 16, self.scale)
        self.stone_tile = self.spritesheet.get_image(16, 48, 16, 16, self.scale)

        # Завантаження кадрів монети
        self.coin_frames = []
        for i in range(9):
            frame = self.spritesheet.get_image(i * 16, 0, 16, 16, self.scale)
            self.coin_frames.append(frame)


        # Рівень
        self.level_map = [
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                            $           ",
            "                           XXX          ",
            "               XXXX                     ",
            "      $                                 ",        
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]
        self.level_width = len(self.level_map[0]) * self.tile_size
        self.level_height = len(self.level_map) * self.tile_size
        self.create_level(self.level_map)

    def create_level(self, level_map):
        for row_index, row in enumerate(level_map):
            col_index = 0
            while col_index < len(row):
                char = row[col_index]
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                if char == "X":
                    # Знаходимо довжину платформи
                    platform_start = col_index
                    length = 0
                    while col_index < len(row) and row[col_index] == "X":
                        length += 1
                        col_index += 1
                    self.create_platform(platform_start, row_index, length)
                    continue
                elif char == "$":
                    coin = Coin(x, y)
                    self.coins.add(coin)
                

                col_index += 1

    def create_platform(self, start_col, row, length):
        for i in range(length):
            x = (start_col + i) * self.tile_size
            y = row * self.tile_size

            if length == 1:
                tile_image = self.grass_tile
            elif i == 0:
                tile_image = self.platform_left
            elif i == length - 1:
                tile_image = self.platform_right
            else:
                tile_image = self.platform_middle
            

            tile = Tile(tile_image, x, y)
            self.tiles.add(tile)

    def update(self):
        self.coins.update()

    def draw(self, camera):
        for tile in self.tiles:
            self.display_surface.blit(tile.image, camera.apply(tile.rect))
        for coin in self.coins:
            self.display_surface.blit(coin.image, camera.apply(coin.rect))

    def handle_collision(self, player):
        collisions = []
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                collisions.append(tile)

        for tile in collisions:
            if player.vel_y > 0:
                player.rect.bottom = tile.rect.top
                player.vel_y = 0
                player.on_ground = True
            elif player.vel_y < 0:
                player.rect.top = tile.rect.bottom
                player.vel_y = 0

        # Монети: перевірка зіткнення
        for coin in self.coins:
            if player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.coins_collected += 1
                # (тут можеш додати звук або +1 монета)

        

    def get_tiles(self):
        return self.tiles
