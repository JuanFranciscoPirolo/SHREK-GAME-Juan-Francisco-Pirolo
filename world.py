import pygame
from coin import Coin
from life_getter import Life
from platformm import Platform
# Inicializar Pygame y las fuentes
pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

class World:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()  # Agrega este atributo para almacenar los enemigos
        self.coins = pygame.sprite.Group()  # Agrega este atributo para almacenar las monedas
        self.life = pygame.sprite.Group()
        self.coin_counter = 0  # Counter for collected coins
        self.coin_font = pygame.font.SysFont(None, 30)  # Font for displaying the coin count
        platform1 = Platform(3, screen_height - 80, 60, 20, 'img/fotos/plataforma_roja.png')
        platform2 = Platform(100, screen_height - 140, 150, 20, 'img/fotos/madera.png')
        platform3 = Platform(400, screen_height - 170, 50, 20, 'img/fotos/hielo.png')
        platform4 = Platform(550, screen_height - 250, 50, 20, 'img/fotos/hielo.png')
        platform5 = Platform(400, screen_height - 300, 50, 20, 'img/fotos/hielo.png', move_range_x = 50, is_moving=True)
        platform6 = Platform(100, screen_height - 320, 150, 20, 'img/fotos/madera.png')
        platform7 = Platform(100, screen_height - 500, 150, 20, 'img/fotos/madera.png')
        platform8 = Platform(10, screen_height - 400, 50, 20, 'img/fotos/hielo.png',move_range_y = 50, is_moving_y=True)
        platform9 = Platform(400, screen_height - 520, 50, 20, 'img/fotos/hielo.png')
        platform10 = Platform(500, screen_height - 520, 50, 20, 'img/fotos/hielo.png', move_range_y = 50)


        self.platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9, platform10)
        # Generar monedas con posiciones aleatorias
        num_coins = 5  # Número de monedas que deseas crear
        for _ in range(num_coins):
            coin = Coin(self.platforms)
            coin.generate_random_position()
            self.coins.add(coin)
            
        num_life_getter = 2
        for _ in range(num_life_getter):
            life = Life(self.platforms)
            life.generate_random_position()
            self.life.add(life)