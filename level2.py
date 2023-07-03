import pygame
from pygame.locals import *
from world_2 import World
from pyvidplayer import Video

pygame.font.init()
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
VIDAS = 5
#vid = Video("audio/nivel_2_video.mp4")
#vid.set_size((700,700))

def mostrar_imagen(imagen):
    image = pygame.image.load(imagen)  # Reemplaza "ruta/imagen.jpg" con la ruta de tu imagen
    image = pygame.transform.scale(image, (screen_width, screen_height))  # Redimensionar la imagen al tamaño de la pantalla
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Salva a Fiona, ha sido secuestrada por el principe!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    # Esperar un tiempo antes de comenzar el juego
    pygame.time.wait(3000)  # Espera 3000 milisegundos (3 segundos)

"""def intro(vid):
    while True:
        if not vid.draw(screen, (0, 0)):
            break
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                return
    vid.close()
        # Mostrar la pantalla con la imagen y la frase"""



def lose_life():
    global VIDAS

    if VIDAS > 0:
        VIDAS -= 1
        
class Level2():
    def __init__(self):
        self.background = pygame.image.load('img/fotos/nivel_2.jpg')
        self.background = pygame.transform.scale(self.background, (800,800))
        #self.init_video = intro()
        #vid.close()
        #self.imagen_video = mostrar_imagen("img/shrek_y_fiona.jpg")
        self.music_bg = pygame.mixer.music.load('audio/X2Download.app - Dirty Deeds Done Dirt Cheap (128 kbps).mp3')
        self.music_bg = pygame.mixer.music.set_volume(0.10)
        self.music_bg = pygame.mixer.music.play(-1)  # Suena
        self.world = self.create_world()
    def create_world(self):
        return World()
    
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, limit_right, limit_left):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.images_hit = []
        self.images_hit_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1
        self.speed = 2
        self.vel_y = 0
        self.gravity = 0.8
        self.player = None
        self.follow_timer = 0
        self.attack_timer = 0  # temporizador para los ataques
        self.attack_delay = 150  # Intervalo de tiempo entre ataques y quite de vida
        self.health = 100  # Valor inicial de la vida
        self.push_duration = 10  # Duración del empuje en fotogramas
        self.push_distance = 10  # Distancia del empuje en píxeles
        self.push_frames = 0  # Fotogramas restantes del empuje
        
        
        for num in range(1, 3):
            img_right = pygame.image.load(f'img/enemigos/{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            
        for num in range(2, 4):
            img_hit = pygame.image.load(f'img/enemigos/{num}.png')
            img_hit = pygame.transform.scale(img_hit, (40, 70))
            img_hit_left = pygame.transform.flip(img_hit, True, False)
            self.images_hit_left.append(img_hit_left)
            self.images_hit.append(img_hit)
            
        self.images_normal = self.images_right
        self.image = self.images_normal[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limit_right = limit_right
        self.limit_left = limit_left

    def update(self):
        if self.push_frames > 0:
            if self.push_frames % 2 == 0:
                self.rect.x -= self.push_distance
            else:
                self.rect.x += self.push_distance
            self.push_frames -= 1
            # Agregar desplazamiento vertical hacia arriba
            self.rect.y -= self.push_distance
            
            
        player_collision = pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(player), False)
        
        if player_collision:
            if self.rect.x < player.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            
            if VIDAS > 0:
                self.rect.x += self.direction * self.speed
                self.speed = 0  # Mantener al enemigo quieto después de colisionar
                
                # Realizar ataque si ha pasado suficiente tiempo desde el último ataque
                if self.attack_timer <= 0:
                    if self.direction == 1:
                        self.image = self.images_hit[self.index]
                    else:
                        self.image = self.images_hit_left[self.index]
                    lose_life()
                    self.attack_timer = self.attack_delay
                    self.index = 0  # Reseteo el index de la animacion
                else:
                    self.attack_timer -= 1
                    if self.direction == 1:
                        self.image = self.images_hit[self.index]
                    else:
                        self.image = self.images_hit_left[self.index]
            else:
                self.speed = 1
                self.rect.x += self.direction * self.speed
                if self.rect.right >= self.limit_right or self.rect.left <= self.limit_left:
                    self.direction *= -1
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
        else:
            self.speed = 2
            self.rect.x += self.direction * self.speed
            if self.rect.right >= self.limit_right or self.rect.left <= self.limit_left:
                self.direction *= -1
            self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
        
        self.rect.y += self.vel_y
        self.vel_y += self.gravity
        
        platform_collision = pygame.sprite.spritecollide(self, world.platforms, False)
        for platform in platform_collision:
            #si esta cayendo
            if self.vel_y > 0:
                #borde inferior del enemigo con la parte superior de la plataforma
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
        
        #Animacion de las imagenes del enemigo.
        self.counter += 1
        #Cuando el contador de imagenes supera las 10 se produce la animacion
        if self.counter >= 10:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
        
        # Verificar si el enemigo y el jugador están superpuestos
        if pygame.sprite.collide_rect(self, player):
            self.speed = 0  # Detener el movimiento del enemigo
        self.draw_health_bar()
        screen.blit(self.image, self.rect)
    def draw_health_bar(self):
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.x + (self.rect.width - bar_width) / 2
        bar_y = self.rect.y - bar_height - 5

        # Calcular la longitud de la barra de vida en función del valor actual de self.health
        health_width = (self.health / 100) * bar_width

        # Dibujar el fondo de la barra de vida
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Dibujar la barra de vida actual
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        
    def reduce_health(self, amount):
        self.health -= amount
        print(self.health)
        if self.health <= 0:
            self.kill()  # Eliminar el enemigo cuando su vida llega a 0 o menos
        else:
            self.push_frames = self.push_duration  # Activar el empuje
class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.images_jump = []
        self.images_stay = []
        self.images_right = []  # Lista vacía para almacenar las imágenes de la animación caminando hacia la derecha
        self.images_left = []  # Lista vacía para almacenar las imágenes de la animación caminando hacia la izquierda
        self.images_punch = [] #Lista vacia para almacener las animaciones delm golpe de Shrek
        self.images_punch_left = [] #golpe a la izquierda
        self.index = 0  # Índice para controlar qué imagen se muestra en la animación
        self.counter = 0  # Contador para controlar la velocidad de la animación
        
        # Carga las imágenes de la animación caminando hacia la derecha y las imágenes espejo para la animación hacia la izquierda
        for num in range(0, 13):
            img_stay = pygame.image.load(f'img/parado/{num}.png')
            img_stay = pygame.transform.scale(img_stay, (40, 70))
            img_right = pygame.image.load(f'img/camina/{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_stay.append(img_stay)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        #animacion para el salto
        for num in range(0, 9):
            img_jump = pygame.image.load(f'img/salta/{num}.png')
            img_jump = pygame.transform.scale(img_jump, (40, 70))
            self.images_jump.append(img_jump)
        #animacion para los golpes de shrek
        for num in range(0, 7):
            img_punch = pygame.image.load(f'img/golpe/{num}.png')
            img_punch = pygame.transform.scale(img_punch, (40, 70))
            self.images_punch.append(img_punch)
        self.dead_image = pygame.image.load('img/pajarito.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (30, 50))
        self.image = self.images_right[self.index]
        self.width = self.image.get_width()
        self.height= self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x  # Establece la posición inicial en el eje x
        self.rect.y = y  # Establece la posición inicial en el eje y
        self.vel_y = 0  # Velocidad vertical inicial del jugador
        self.direction = 0  # Variable para controlar la dirección del jugador (1 para derecha, -1 para izquierda)
        self.jumped = False  # Variable para controlar si el jugador está saltando
        self.punch = False
        self.can_jump = True
    def update(self):
        dx = 0  # Desplazamiento en el eje x
        dy = 0  # Desplazamiento en el eje y
        walk_cooldown = 5  # controla la velocidad de la animación.

        # Obtiene el estado de las teclas presionadas
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            if not self.punch:
                self.punch = True
                self.counter = 0  # Reiniciar el contador para la animación de golpe
                self.index = 0  # Reiniciar el índice para la animación de golpe
        
        if not key[pygame.K_SPACE] and self.can_jump:
            self.jumped = False
        
        if not key[pygame.K_RETURN]:
            self.punch = False
            

        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
            
        if key[pygame.K_RETURN] and not self.punch:
            self.punch = True
            self.check_collision()  # Verifica la colisión con los enemigos

        if key[pygame.K_LEFT]:
            dx -= 4
            self.counter += 1
            self.direction = -1

        if key[pygame.K_RIGHT]:
            dx += 4
            self.counter += 1
            self.direction = 1
        if VIDAS > 0:
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter += 1
                #controlo la velocidad de la animacion
                if self.counter >= walk_cooldown:
                    self.counter = 0
                    self.index += 1

                    if self.index >= len(self.images_stay):
                        self.index = 0
                    self.image = self.images_stay[self.index]

                if self.jumped:
                    if self.index >= len(self.images_jump):
                        self.index = 0
                    if self.direction == -1:
                        self.image = pygame.transform.flip(self.images_jump[self.index], True, False)
                    elif self.direction == 1:
                        self.image = self.images_jump[self.index]
                    self.index += 1  #act

                else:
                    if self.direction == 1:
                        self.image = self.images_stay[self.index]
                    elif self.direction == -1:
                        self.image = pygame.transform.flip(self.images_stay[self.index], True, False)
                    
                
                if self.punch:
                    if self.index >= len(self.images_punch):
                        self.index = 0
                        self.punch = False
                        enemy_collision = pygame.sprite.spritecollide(self, world.enemies, False)
                        for enemy in enemy_collision:
                            enemy.reduce_health(20)
 
                            if enemy.health <= 0:
                                enemy.kill()  # Elimina el enemigo si su vida llega a cero
                            
                    if self.direction == -1:
                        self.image = pygame.transform.flip(self.images_punch[self.index], True, False)
                    elif self.direction == 1:
                        self.image = self.images_punch[self.index]
                else:
                    if self.direction == 1:
                        self.image = self.images_stay[self.index]
                    elif self.direction == -1:
                        self.image = pygame.transform.flip(self.images_stay[self.index], True, False)
                        

            else:
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1

                    # Si se alcanza el final de la animación, vuelve al inicio
                    if self.index >= len(self.images_right):
                        self.index = 0

                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    elif self.direction == -1:
                        self.image = self.images_left[self.index]

            # gravedad
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            #si el jugador se cae
            if self.rect.bottom > screen_height:
                lose_life()
            

            self.rect.x += dx

    # Colisiones en el eje X
            platform_collision = pygame.sprite.spritecollide(self, world.platforms, False)
            for platform in platform_collision:
                if dx > 0:  # se mueve a la derecha
                    self.rect.right = platform.rect.left
                elif dx < 0:  # se mueve a la izquierda
                    self.rect.left = platform.rect.right

                if platform.is_moving and platform.move_range_x != 0:
                    self.rect.x += platform.move_direction_x

                    if dx > 0:
                        self.rect.right = platform.rect.left
                    elif dx < 0:
                        self.rect.left = platform.rect.right
                    

            self.rect.y += dy

            # Colisiones en el eje Y
            platform_collision = pygame.sprite.spritecollide(self, world.platforms, False)
            for platform in platform_collision:
                if dy > 0:  # cayendo
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jumped = False
                    self.can_jump = True  # Permite saltar nuevamente al tocar una plataforma
                elif dy < 0:  # saltando
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

                if platform.is_moving_y and platform.move_range_y != 0:
                    self.rect.y += platform.move_direction_y
                    
                if platform.is_moving and platform.move_range_x != 0:
                    self.rect.x += platform.move_direction_x
                    
            #if not platform_collision:
                #self.can_jump = False  # Modo debugging
                
        #si esta muerto
        else:
            pygame.mixer.music.stop()
            self.image = self.dead_image
            if self.rect.y > 10:
                    self.rect.y -= 3
                    self.rect.x += 5
            else:
                self.kill()
        #pygame.draw.rect(screen, "red", self.rect, 2)
    def check_collision(self):
        self.collided_enemies = pygame.sprite.spritecollide(self, world.enemies, False)

    def apply_damage(self):
        if self.direction == 1:
            self.images_punch = self.images_punch[self.index]
        else:
            self.images_punch = pygame.transform.flip(self.images_punch[self.index], True, False)

        for enemy in self.collided_enemies:
            enemy.reduce_health(20)
            if enemy.health <= 0:
                enemy.kill()  # Elimina el enemigo si su vida llega a cero
        screen.blit(self.image, self.rect)
        self.collided_enemies = []

world = World()
player = Player(30, screen_height - 40 - 70)
enemy = Enemy(200, screen_height - 385, 250, 100)
enemy2 = Enemy(500, screen_height - 500, 250, 100)
world.enemies.add(enemy, enemy2)  # Agrega el enemigo al grupo de enemigos en world