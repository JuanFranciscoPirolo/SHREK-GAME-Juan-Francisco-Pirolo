import pygame
import random

class Life(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.image.load('img/vendas.png')
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.platforms = platforms  # Almacena las plataformas disponibles

    def generate_random_position(self):
        platform = random.choice(self.platforms.sprites())  # Elige una plataforma al azar
        self.rect.centerx = random.randint(platform.rect.left, platform.rect.right)  # Genera una posición x aleatoria dentro de la plataforma
        self.rect.bottom = platform.rect.top  # La parte inferior de la moneda coincide con la parte superior de la plataforma

