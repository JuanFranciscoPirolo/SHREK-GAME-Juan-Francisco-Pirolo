import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, move_range_x=None, move_range_y=None, is_moving=False, is_moving_y = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter_x = 0
        self.move_direction_x = 1
        self.move_range_x = move_range_x
        self.move_counter_y = 0
        self.move_direction_y = 1
        self.move_range_y = move_range_y
        self.is_moving = is_moving  # Identificador de plataforma móvil
        self.is_moving_y = is_moving_y
    def update(self):
        if self.move_range_x and self.is_moving:
            self.rect.x += self.move_direction_x
            self.move_counter_x += 1
            
            if abs(self.move_counter_x) > self.move_range_x:
                self.move_direction_x *= -1
                self.move_counter_x *= -1
        
        if self.move_range_y and self.is_moving_y:
            self.rect.y += self.move_direction_y
            self.move_counter_y += 1
            
            if abs(self.move_counter_y) > self.move_range_y:
                self.move_direction_y *= -1
                self.move_counter_y *= -1