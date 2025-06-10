import pygame
from spritesheet import SpriteSheet
from settings import PLAYER_SPEED, GRAVITY, JUMP_STRENGTH
import pygame.mixer

class Player(pygame.sprite.Sprite):
    pygame.mixer.init()
    jump_sound = pygame.mixer.Sound("assets/jump.wav")
    jump_sound.set_volume(0.1)
    def __init__(self, pos):
        super().__init__()
        self.sprite_sheet = SpriteSheet("assets/characters.png")
        self.frame_width = 32
        self.frame_height = 32
        self.scale = 2
        
        # Анімація з 8 кадрами з третього ряду (індекс 2)
        self.frames_right = [
            self.sprite_sheet.get_image(x * self.frame_width, 2 * self.frame_height, 
                                      self.frame_width, self.frame_height, self.scale)
            for x in range(8)
        ]
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]
        
        # Кадри простою
        self.idle_frame_right = self.frames_right[0]
        self.idle_frame_left = self.frames_left[0]
        
        # Стан спрайту
        self.current_frame = 0
        self.image = self.idle_frame_right
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = "right"
        self.frame_timer = 0
        self.animation_speed = 6
        self.is_moving = False
        
        
        self.vel_x = 0  # Горизонтальна швидкість
        self.vel_y = 0  # Вертикальна швидкість
        self.on_ground = False
        self.friction = 0.8  # Тертя для зупинки
        self.acceleration = 0.5  # Прискорення руху
        self.max_speed = PLAYER_SPEED  # Максимальна швидкість
        
        # Стан клавіш для правильної обробки
        self.moving_left = False
        self.moving_right = False

    def handle_input(self, keys):
        """Обробка введення з клавіатури"""
        # Оновлюємо стан клавіш
        self.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Горизонтальний рух з прискоренням
        if self.moving_left:
            self.vel_x -= self.acceleration
            self.direction = "left"
            self.is_moving = True
        elif self.moving_right:
            self.vel_x += self.acceleration
            self.direction = "right"
            self.is_moving = True
        else:
            # Застосовуємо тертя коли клавіші не натиснуті
            self.vel_x *= self.friction
            self.is_moving = False
            
            # Зупиняємо при дуже малій швидкості
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0

        # Обмежуємо максимальну швидкість
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        elif self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed
            
        # Стрибок
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False
            self.jump_sound.play()
            



    def apply_physics(self):
        """Застосування фізики руху"""
        # Горизонтальний рух
        self.rect.x += self.vel_x
        
        
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Вертикальний рух
        self.rect.y += self.vel_y

    def check_horizontal_collisions(self, tiles):
        """Перевірка горизонтальних колізій"""
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collisions.append(tile)
        
        for tile in collisions:
            if self.vel_x > 0:  # Рух вправо
                self.rect.right = tile.rect.left
                self.vel_x = 0
            elif self.vel_x < 0:  # Рух вліво
                self.rect.left = tile.rect.right
                self.vel_x = 0

    def check_vertical_collisions(self, tiles):
        """Перевірка вертикальних колізій"""
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collisions.append(tile)
        
        for tile in collisions:
            if self.vel_y > 0:  # Падіння вниз
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:  # Стрибок вгору
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

    def check_ground_contact(self, tiles):
        """Перевірка чи персонаж стоїть на землі"""
        # Створюємо невеликий прямокутник під персонажем для перевірки
        ground_check_rect = pygame.Rect(
            self.rect.x + 5, 
            self.rect.bottom,
            self.rect.width - 10,  
            5  # Висота перевірки
        )
        
        self.on_ground = False
        for tile in tiles:
            if ground_check_rect.colliderect(tile.rect):
                self.on_ground = True
                break

    def animate(self):
        """Анімація персонажа"""
        if self.is_moving and abs(self.vel_x) > 0.5:  # Анімуємо тільки при реальному русі
            self.frame_timer += 1
            if self.frame_timer >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames_right)
                self.frame_timer = 0
            
            if self.direction == "right":
                self.image = self.frames_right[self.current_frame]
            else:
                self.image = self.frames_left[self.current_frame]
        else:
            # Кадр простою
            self.current_frame = 0
            self.frame_timer = 0
            if self.direction == "right":
                self.image = self.idle_frame_right
            else:
                self.image = self.idle_frame_left

    def check_level_boundaries(self, level_width, level_height):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        elif self.rect.right > level_width:
            self.rect.right = level_width
            self.vel_x = 0
            
        # Перевірка вертикальних меж
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        elif self.rect.bottom > level_height:
            # Якщо персонаж впав за межі рівня, повертаємо його на останню безпечну позицію
            self.reset_position((100,100))
            

    def update(self, keys, tiles, level_width=1280, level_height=384):
        """Головний цикл оновлення персонажа"""
        # 1. Обробка введення
        self.handle_input(keys)
        
        # 2. Застосування горизонтального руху
        old_x = self.rect.x
        self.rect.x += self.vel_x
        self.check_horizontal_collisions(tiles)
        
        # 3. Застосування вертикального руху та гравітації
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        old_y = self.rect.y
        self.rect.y += self.vel_y
        self.check_vertical_collisions(tiles)
        
        # 4. Перевірка контакту з землею
        self.check_ground_contact(tiles)
        
        # 5. Перевірка меж РІВНЯ
        self.check_level_boundaries(level_width, level_height)
        
        # 6. Анімація
        self.animate()

    def reset_position(self, pos):
        self.rect.topleft = pos
        self.vel_y = 0
        self.on_ground = False


    def get_debug_info(self):
        """Інформація для дебагу"""
        return {
            "pos": (self.rect.x, self.rect.y),
            "vel": (round(self.vel_x, 2), round(self.vel_y, 2)),
            "on_ground": self.on_ground,
            "moving": self.is_moving
        }
