import pygame
from pygame.locals import *
from world_1 import World

pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
VIDAS = 5



class Level1():
    def __init__(self):
        self.background = pygame.image.load('img/fotos/shrekfondo.jpg')
        self.background = pygame.transform.scale(self.background, (800,800))
        pygame.mixer.music.load('audio/ACDC - Highway To Hell.mp3')
        pygame.mixer.music.play(-1)  # Suena
        self.world = self.create_world()
    def create_world(self):
        return World()


