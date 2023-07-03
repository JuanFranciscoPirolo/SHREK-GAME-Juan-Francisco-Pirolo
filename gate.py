import pygame
from main_principal import intro
class Gate:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    #Si el jugador pasa el final, y toca la compuerta.
    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            pygame.mixer.music.stop()
            all_sprites.remove(player)