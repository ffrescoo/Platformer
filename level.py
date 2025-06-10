import pygame
from tile import Tile
from coin import Coin
from spritesheet import SpriteSheet
from portal import Portal
from level_data import levels
from player import Player
import pygame.mixer

class Level:
    pygame.mixer.init()
    pygame.font.init()
    coin_sound = pygame.mixer.Sound("assets/coin.wav")
    coin_sound.set_volume(0.1)
    teleport_sound = pygame.mixer.Sound("assets/teleport.wav")
    teleport_sound.set_volume(0.1)
    def __init__(self, surface):
        self.display_surface = surface
        self.tile_size = 32
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.coins_collected = 0
        self.portals = pygame.sprite.Group()
        self.current_level = 0
        self.levels = levels
        self.show_collect_all_message = False
        self.message_timer = 0
    

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

        self.load_level(self.current_level)
        # Рівень
        

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
                elif char == "P":
                    portal = Portal(x,y)
                    self.portals.add(portal)

                

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
        self.portals.update()

        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.show_collect_all_message = False

    def draw(self, camera):
        for tile in self.tiles:
            self.display_surface.blit(tile.image, camera.apply(tile.rect))
        for coin in self.coins:
            self.display_surface.blit(coin.image, camera.apply(coin.rect))
        for portal in self.portals:
            self.display_surface.blit(portal.image, camera.apply(portal.rect))

        if hasattr(self, 'show_collect_all_message') and self.show_collect_all_message:
            self.font = pygame.font.SysFont('Sans', 30)
            message_text = self.font.render("Зібрано не всі монети на рівні!", True, (255, 0, 0))

            self.screen_width = self.display_surface.get_width()
            self.screen_height = self.display_surface.get_height()
            self.text_width = message_text.get_width()
            self.text_height = message_text.get_height()

            x = (self.screen_width - self.text_width ) // 2
            y = (self.screen_height - self.text_height) // 2

            self.display_surface.blit(message_text, (x,y))
            
    
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
                self.coin_sound.play()
                self.coins_collected += 1
                

        for portal in self.portals:
            if player.rect.colliderect(portal.rect):
                if len(self.coins) == 0:
                    self.next_level(player)
                    self.teleport_sound.play()
                else:
                    self.show_collect_all_message = True  
                    self.message_timer = 120



        

    def get_tiles(self):
        return self.tiles
    
    def next_level(self, player):
        self.current_level += 1
        self.load_level(self.current_level)
        player.reset_position((100,100))

    def load_level(self, index):
        if index >= len(self.levels):
            self.show_end_screen()
            return

        self.tiles.empty()
        self.coins.empty()
        self.portals.empty()

        if index < len(self.levels):
            self.current_level = index
            level_map = self.levels[index]
            self.level_width = len(level_map[0]) * self.tile_size
            self.level_height = len(level_map) * self.tile_size
            self.create_level(level_map)
    
    def show_end_screen(self):
        font = pygame.font.SysFont("Arial", 48)
        small_font = pygame.font.SysFont("Arial", 30)
        clock = pygame.time.Clock()

        while True:
            self.display_surface.fill((0, 0, 0))
            text = font.render("Вітаємо! Ви пройшли гру!", True, (255, 255, 255))
            button_text = small_font.render("Натисніть ENTER, щоб почати знову", True, (255, 255, 255))

            self.display_surface.blit(text, (self.display_surface.get_width() // 2 - text.get_width() // 2, 200))
            self.display_surface.blit(button_text, (self.display_surface.get_width() // 2 - button_text.get_width() // 2, 300))

            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.current_level = 0
                        self.load_level(self.current_level)
                        return
                    
            clock.tick(60)