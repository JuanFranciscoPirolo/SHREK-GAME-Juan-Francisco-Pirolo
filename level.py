import pygame
from pygame.locals import *
from world import World
from jugador import Player
from enemy import Enemy
from main_principal import screen,clock,fps,pos_vidas,coin_image,bg_img,player,world,coin_sound,life_sound,VIDAS,vida_img,gate,all_sprites,screen_height

class Nivel:
    def __init__(self,bg_img):
        self.bg_img = pygame.image.load(bg_img)
        
        
    
    def update():
        
        clock.tick(fps)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Verificar las colisiones entre el jugador y las monedas
        collisions = pygame.sprite.spritecollide(player, world.coins, True)
        for coin in collisions:
            world.coin_counter += 1
            coin_sound.play()
            coin_sound.set_volume(0.30)

        collisions = pygame.sprite.spritecollide(player, world.life, True)
        for life in collisions:
            if VIDAS < 5:
                VIDAS += 1
            life_sound.play()
            life_sound.set_volume(0.30)
        # Actualizar las plataformas
        world.platforms.update()
        
        # Dibujar en la pantalla
        screen.blit(self.bg_img, (-100, -60))
        for i in range(VIDAS):
            screen.blit(vida_img, (pos_vidas[0] + i * (vida_img.get_width() + 5), pos_vidas[1]))
        world.platforms.draw(screen)
        world.coins.draw(screen)
        world.life.draw(screen)
        gate.check_collision(player)
        gate.draw(screen)  # Dibujar la compuerta en la ventana
        # Actualizar y dibujar el contador de monedas
        screen.blit(coin_image, (590, 5))
        coin_text = world.coin_font.render("X"+ " " +str(world.coin_counter), True, (255, 255, 255))
        screen.blit(coin_text, (coin_image.get_width() + 600, 20))
        

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()