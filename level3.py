import pygame
from pygame.locals import *
from world_3 import World
from pyvidplayer import Video

pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
VIDAS = 5

class Level3():
    def __init__(self):
        self.background = pygame.image.load('img/fotos/castle.jpg')
        self.background = pygame.transform.scale(self.background, (800,800))
        #self.init_video = intro()
        #vid.close()
        #self.imagen_video = mostrar_imagen("img/fotos/shrek_foto_final.jpg")
        self.music_bg = pygame.mixer.music.load('audio/MUSICA PARA SUSPENSO-ACCION - MUSIC FOR SUSPENSE-ACTION (1).mp3')
        self.music_bg = pygame.mixer.music.play(-1)  # Suena
        self.world = self.create_world()
    def create_world(self):
        return World()
