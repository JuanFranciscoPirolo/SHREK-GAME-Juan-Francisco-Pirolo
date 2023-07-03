import pygame
from pygame.locals import *
from world_3 import World
from pyvidplayer import Video
from jugador import Player
from jugador import Enemy

pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
VIDAS = 5
#vid = Video("audio/Vídeo sin título ‐ Hecho con Clipchamp (1).mp4")
#vid.set_size((700,700))
"""def intro():
    while True:
        if not vid.draw(screen, (0, 0)):
            break
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                return
    
        # Mostrar la pantalla con la imagen y la frase
def mostrar_imagen(imagen):
    image = pygame.image.load(imagen)  # Reemplaza "ruta/imagen.jpg" con la ruta de tu imagen
    image = pygame.transform.scale(image, (screen_width, screen_height))  # Redimensionar la imagen al tamaño de la pantalla
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Haz salvado a Fiona, gracias por tu ayuda!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    # Esperar un tiempo antes de comenzar el juego
    pygame.time.wait(3000)  # Espera 3000 milisegundos (3 segundos)"""

def lose_life():
    global VIDAS

    if VIDAS > 0:
        VIDAS -= 1
class Level3():
    def __init__(self):
        self.background = pygame.image.load('img/fotos/castle.jpg')
        self.background = pygame.transform.scale(self.background, (800,800))
        #self.init_video = intro()
        #vid.close()
        #self.imagen_video = mostrar_imagen("img/fotos/shrek_foto_final.jpg")
        self.music_bg = pygame.mixer.music.load('audio/MUSICA PARA SUSPENSO-ACCION - MUSIC FOR SUSPENSE-ACTION (1).mp3')
        self.music_bg = pygame.mixer.music.set_volume(0.10)
        self.music_bg = pygame.mixer.music.play(-1)  # Suena
        self.world = self.create_world()
    def create_world(self):
        return World()

world = World()
player = Player(30, screen_height - 40 - 70)
enemy = Enemy(200, screen_height - 385, 250, 100)
enemy2 = Enemy(500, screen_height - 500, 250, 100)
world.enemies.add(enemy, enemy2)  # Agrega el enemigo al grupo de enemigos en world