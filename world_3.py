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
        platform1 = Platform(230, 600, 500, 25, 'img/fotos/platform.png' )
        platform2 = Platform(260, 480, 350, 25, 'img/fotos/platform.png')
        platform3 = Platform(80, 550, 50, 20, 'img/fotos/crumbling_platforms_c.png', move_range_y= 50, is_moving_y = True)
        platform4 = Platform(650, 380, 50, 20, 'img/fotos/crumbling_platforms_c.png', move_range_y= 95, is_moving_y = True)
        platform5 = Platform(260, 350, 320, 25, 'img/fotos/platform.png')
        platform6 = Platform(80, 300, 50, 20, 'img/fotos/crumbling_platforms_c.png', move_range_y= 50, is_moving_y = True)
        platform7 = Platform(250, 230, 50, 20, 'img/fotos/crumbling_platforms_c.png')
        platform8 = Platform(0, 150, 50, 20, 'img/fotos/crumbling_platforms_c.png')
        platform9 = Platform(430, 180, 100, 20, 'img/fotos/crumbling_platforms_c.png')


        self.platforms.add(platform1, platform2,platform3,platform4,platform5,platform6,platform7,platform8,platform9)
        # Generar monedas con posiciones aleatorias
        num_coins = 8  # Número de monedas que deseas crear
        for _ in range(num_coins):
            coin = Coin(self.platforms)
            coin.generate_random_position()
            self.coins.add(coin)
            
        num_life_getter = 3
        for _ in range(num_life_getter):
            life = Life(self.platforms)
            life.generate_random_position()
            self.life.add(life)