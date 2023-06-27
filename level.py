import pygame
import sys
from pygame.locals import *
from world import World
from jugador import Player

class Nivel:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Configuración de pantalla
        self.screen_width = 700
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Salva a Fiona")
        
        # Inicialización de sonidos
        self.fire_sound = pygame.mixer.Sound("audio/Efecto de Sonido - Fuego (Incendio).mp3")
        self.death_sound = pygame.mixer.Sound("audio/Sonido de muerte de Fortnite-Death Fortnite sound.mp3")
        self.life_sound = pygame.mixer.Sound("audio/Sonido de experiencia en minecraft.mp3")
        self.coin_sound = pygame.mixer.Sound("audio/coin.wav")
        self.punch_sound = pygame.mixer.Sound("audio/Efecto de sonido- Golpe.mp3")
        
        # Jugabilidad
        self.player = Player(30, self.screen_height - 40 - 70)
        self.bg_img = pygame.image.load("img/fotos/fondo1.jpg")
        
        # Creación del mundo
        self.world = World()

    def update(self):
        self.screen.blit(self.player.image)

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

            # Renderizar los elementos en la pantalla
            self.screen.blit(self.bg_img, (0, 0))
            self.update()
            pygame.display.update()

        pygame.quit()
        sys.exit()

nivel = Nivel()
nivel.jugar()
