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
        self.coin_font = pygame.font.SysFont(None, 30)  # Font for displaying the coin coun

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