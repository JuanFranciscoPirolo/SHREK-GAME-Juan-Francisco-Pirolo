import pygame
import sys
from pygame.locals import *
from world import World
from jugador import Player
from enemy import Enemy
from platformm import Platform
from level import Nivel

screen_width = 700
screen_height = 700

class Level1(Nivel):
    def __init__(self):
        super().__init__()  # Llama al constructor de la clase base Nivel
        pygame.mixer.init()

        # Configuración de pantalla
        self.screen_width = 700
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Inicialización de sonidos
        self.fire_sound = pygame.mixer.Sound("audio/Efecto de Sonido - Fuego (Incendio).mp3")
        self.death_sound = pygame.mixer.Sound("audio/Sonido de muerte de Fortnite-Death Fortnite sound.mp3")
        self.life_sound = pygame.mixer.Sound("audio/Sonido de experiencia en minecraft.mp3")
        self.coin_sound = pygame.mixer.Sound("audio/coin.wav")
        self.punch_sound = pygame.mixer.Sound("audio/Efecto de sonido- Golpe.mp3")

        pygame.display.set_caption("Level 1")

        # Creación del mundo y los personajes
        self.world = World(self.screen)
        self.player = Player(100, 100)
        self.enemies = [Enemy(200, 200), Enemy(400, 200)]
        self.platforms = [
            Platform(3, screen_height - 80, 60, 20, 'img/fotos/plataforma_roja.png'),
            Platform(100, screen_height - 140, 150, 20, 'img/fotos/madera.png'),
            Platform(400, screen_height - 170, 50, 20, 'img/fotos/hielo.png'),
            Platform(550, screen_height - 250, 50, 20, 'img/fotos/hielo.png'),
            Platform(400, screen_height - 300, 50, 20, 'img/fotos/hielo.png', move_range_x=50, is_moving=True),
            Platform(100, screen_height - 320, 150, 20, 'img/fotos/madera.png'),
            Platform(100, screen_height - 500, 150, 20, 'img/fotos/madera.png'),
            Platform(10, screen_height - 400, 50, 20, 'img/fotos/hielo.png', move_range_y=50, is_moving_y=True),
            Platform(400, screen_height - 520, 50, 20, 'img/fotos/hielo.png'),
            Platform(500, screen_height - 520, 50, 20, 'img/fotos/hielo.png', move_range_y=50),
            Platform(650, screen_height - 600, 100, 20, 'img/fotos/hielo.png', move_range_y=50)
        ]

        self.VIDAS = 5
        self.pos_vidas = (10, 10)  # Coordenadas (x, y) de la esquina superior izquierda donde se mostrarán las vidas

    def jugar(self):
        clock = pygame.time.Clock()
        fps = 60
        game_running = True

        while game_running:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False  # Salir del bucle principal cuando se recibe el evento QUIT

            # Procesar la lógica del juego
            self.player.update()
            for enemy in self.enemies:
                enemy.update()

            # Renderizar los elementos en la pantalla
            self.screen.blit(self.world.bg_img, (0, 0))

            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)

            for platform in self.platforms:
                platform.draw(self.screen)

            pygame.display.update()

        pygame.quit()
        sys.exit()
