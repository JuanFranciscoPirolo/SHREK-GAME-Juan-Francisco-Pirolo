import pygame
import pygame.mixer
from pygame.locals import *
from enemy import Enemy
from world import World
from jugador import Player
from level1 import Level1
from level2 import Level2
from level3 import Level3
from pyvidplayer import Video
from temporizador import Timer

#solucionar error dragon
#agregar sonido nivel 3
#agregar projectiles shrek
#que los enemigos se generen aleatoriamente.
#agregar cronometro, bajar puntos si tarda mas.
#trampa
#niveles
#agregar sonido cuando se muere el enemigo
# settings, efectos de sonido, on y off musica ambiental on y off, guardar partida, no necesaria.
#para interfaz de usuario pantalla principal, pantalla de pausa, settings, puntuaciones, pantalla win lose
#manejo de archivos: info niveles en archivo.  guardar settings.

pygame.init()

#Configuracion de musica
fire_sound = pygame.mixer.Sound("audio/Efecto de Sonido - Fuego (Incendio).mp3")
death_sound = pygame.mixer.Sound("audio/Sonido de muerte de Fortnite-Death Fortnite sound.mp3")
life_sound = pygame.mixer.Sound("audio/Sonido de experiencia en minecraft.mp3")
coin_sound = pygame.mixer.Sound("audio/coin.wav")
punch_sound = pygame.mixer.Sound("audio/Efecto de sonido- Golpe.mp3")

#FPS
clock = pygame.time.Clock()
fps = 60

# Configuración de pantalla
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
#Muestro el video del inicio


#pygame.mixer.music.load('audio/X2Download.app - Dirty Deeds Done Dirt Cheap (128 kbps).mp3')  # Cargo la musica de fondo.
#pygame.mixer.music.set_volume(0.10)
#pygame.mixer.music.play(-1)  # Suena

# Imágenes cargadas
coin_image = pygame.image.load("img/coin.png")
coin_image = pygame.transform.scale(coin_image,(40,40))
vida_img = pygame.image.load('img/life.png')
vida_img = pygame.transform.scale(vida_img, (40, 35))
game_over_image = pygame.image.load("img/game_over.jpg").convert()
game_over_image = pygame.transform.scale(game_over_image, (screen_height,screen_width))
# Fuente
font = pygame.font.Font(None, 30)
VIDAS = 5
pos_vidas = (10, 10)  # Coordenadas (x, y) de la esquina superior izquierda donde se mostrarán las vidas

pygame.display.set_caption("Salva a Fiona")
#Perder una vida
def mostrar_imagen(imagen,texto):
    pygame.mixer.music.pause()  # Pausar la música
    image = pygame.image.load(imagen)  # Reemplaza "ruta/imagen.jpg" con la ruta de tu imagen
    image = pygame.transform.scale(image, (screen_width, screen_height))  # Redimensionar la imagen al tamaño de la pantalla
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render(texto, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    # Esperar un tiempo antes de comenzar el juego
    pygame.time.wait(3000)  # Espera 3000 milisegundos (3 segundos)

def lose_life():
    global VIDAS

    if VIDAS > 0:
        VIDAS -= 1
nivel1 = Level1()
nivel2 = Level2()
nivel3 = Level3()
def blit_level_background(nivel):
    if nivel == 1:
        screen.blit(nivel1.background, (-100, -60))
    elif nivel == 2:
        screen.blit(nivel2.background, (-100, -60))
    elif nivel == 3:
        screen.blit(nivel3.background, (-100, -60))
    # Agrega más casos según los niveles adicionales que tengas
def intro(vid):
    pygame.mixer.music.pause()  # Pausar la música
    
    vid = Video(vid)
    vid.set_size((700,700))
    while True:
        if not vid.draw(screen, (0, 0)):
            break
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                pygame.mixer.music.unpause()  # Reanudar la música
                return
    
    vid.close()
    pygame.mixer.music.unpause()  # Reanudar la música

        # Mostrar la pantalla con la imagen y la frase



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
        self.push_distance = 7  # Distancia del empuje en píxeles
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
        self.VIDAS = VIDAS
        self.dead = False
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
            self.check_collision()  # Verifica la colisión con los enemigos
            self.apply_damage()
            
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
                            punch_sound.play()
                            punch_sound.set_volume(0.30)
                        
                        boss_collision = pygame.sprite.spritecollide(self, boss_group, False)
                        for boss_sprite in boss_collision:
                            boss_sprite.reduce_health(20)
                            punch_sound.play()
                            punch_sound.set_volume(0.30)

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
            timer.stop()
            pygame.mixer.music.load('audio/Shrek - Melodía (Fairytale).mp3')
            pygame.mixer.music.play(-1)  # Suena
            
            self.image = self.dead_image
            if self.rect.y > 10:
                    self.rect.y -= 3
                    self.rect.x += 5
            else:
                self.dead = True
                death_sound.play()
                death_sound.set_volume(0.40)
                self.kill()

        #pygame.draw.rect(screen, "red", self.rect, 2)
        
    def check_collision(self):
        self.collided_enemies = pygame.sprite.spritecollide(self, world.enemies, False)
        self.collided_bosses = pygame.sprite.spritecollide(self, boss_group, False)

    def apply_damage(self):
        for enemy in self.collided_enemies:
            enemy.reduce_health(20)
            if enemy.health <= 0:
                enemy.kill()  # Elimina el enemigo si su vida llega a cero

        for boss_sprite in self.collided_bosses:
            boss_sprite.reduce_health(20)
            if boss_sprite.health <= 0:
                boss_sprite.kill()  # Elimina el jefe final si su vida llega a cero
class Gate:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.nivel = 0
        self.level_added = False  # Variable para controlar si el nivel ya ha sido sumado
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    #Si el jugador pasa el final, y toca la compuerta.
    def check_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.level_added:
            pygame.mixer.music.stop()
            all_sprites.remove(player)
            self.nivel += 1
            self.level_added = True
            pasar_al_siguiente_nivel()
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bola_fuego.png")
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()  # Elimina el proyectil si sale de la pantalla
class BossFinal(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player  # Assign the player object
        self.images_right = []
        self.images_left = []
        self.images_hit_right = []
        self.images_hit_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1
        self.speed = 2
        self.vel_y = 0
        self.follow_timer = 0
        self.attack_timer = 0  # temporizador para los ataques
        self.attack_delay = 150  # Intervalo de tiempo entre ataques y quite de vida
        self.health = 200  # Valor inicial de la vida
        self.mouth_offset_x = 120  # Offset en la coordenada X de la boca del dragón
        self.mouth_offset_y = 60  # Offset en la coordenada Y de la boca del dragón
        self.fireball_timer = 0
        self.fireball_delay = 100  # Intervalo de tiempo entre lanzamientos de bolas de fuego
        self.projectiles = pygame.sprite.Group()  # Grupo para almacenar los proyectiles
        self.max_health = 100  # Valor máximo de la vida del enemigo
        self.health = self.max_health  # Valor inicial de la vida del enemigo
        
        for num in range(0, 11):
            img_right = pygame.image.load(f'img/parado_drake/{num}.png')
            img_right = pygame.transform.scale(img_right, (150, 120))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        
        for num in range(0, 5):
            img_hit_right = pygame.image.load(f'img/ataque_dragon/{num}.png')
            img_hit_right = pygame.transform.scale(img_hit_right, (40, 70))
            img_hit_left = pygame.transform.flip(img_hit_right, True, False)
            self.images_hit_right.append(img_hit_right)
            self.images_hit_left.append(img_hit_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Inicializar el rectángulo de la boca
        self.mouth_rect = pygame.Rect(0, 0, 20, 20)

        # Bandera para controlar la animación de golpe
        self.is_hitting = False
        self.hit_counter = 0
        self.hit_duration = 5  # Duración de la animación de golpe en fotogramas
    def draw_health_bar(self):
        bar_width = 90  # Ancho de la barra de vida
        bar_height = 10  # Alto de la barra de vida
        bar_x = screen_width - bar_width - 50  # Coordenada X de la barra de vida (ajustada a la izquierda)
        bar_y = 60  # Coordenada Y de la barra de vida

        # Calcular la longitud de la barra de vida en función del valor actual de self.health
        health_width = (self.health / self.max_health) * bar_width

        # Dibujar el fondo de la barra de vida
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Dibujar la barra de vida actual
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

    def update(self):
        self.draw_health_bar()
        if pygame.sprite.collide_rect(self, self.player):
            if self.player.rect.left < self.rect.right:
                self.player.rect.x -= 0.5
            


        # Resto del código de actualización
        self.counter += 1
        if self.counter >= 8:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0

        self.attack_timer += 1

        # Check if the player is on the same y-axis level as the boss's mouth
        if self.rect.y <= self.player.rect.y <= self.rect.y + self.mouth_offset_y:
            # Disparar proyectiles y activar la animación de golpe
            if self.attack_timer >= self.attack_delay:
                self.attack_timer = 0
                if self.direction == 1:
                    projectile = Bullet(self.rect.x + 180, self.rect.y + 40, self.direction)
                else:
                    projectile = Bullet(self.rect.x - 40, self.rect.y + 40, self.direction)

                all_sprites.add(projectile)
                self.projectiles.add(projectile)
                # Activar la animación de golpe
                self.is_hitting = True
                self.hit_counter = self.hit_duration
        
        if self.is_hitting:
            if self.direction == 1:
                if self.index < len(self.images_hit_right):
                    self.image = self.images_hit_right[self.index]
                else:
                    self.image = self.images_hit_right[-1]
            else:
                if self.index < len(self.images_hit_left):
                    self.image = self.images_hit_left[self.index]
                else:
                    self.image = self.images_hit_left[-1]

            self.index += 1

            if self.index >= len(self.images_hit_right) or self.index >= len(self.images_hit_left):
                self.index = 0
                self.is_hitting = False
                self.hit_counter = 0
        else:
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]
            # Comprobar colisión entre la bola de fuego y el jugador
            if pygame.sprite.spritecollide(self.player, self.projectiles, True):
                # Acción a realizar cuando la bola de fuego golpea al jugador
                lose_life()
            # Dibujar la imagen del dragón en la pantalla
        screen.blit(self.image, self.rect)
        
    # Dentro de la clase BossFinal
    def reduce_health(self, amount):
        self.health -= amount
        
        if self.health <= 0:
            self.kill()  # Eliminar el jefe final cuando su vida llega a 0 o menos
            
        # Actualizar la posición del rectángulo de la boca
        self.mouth_rect.x = self.rect.x + self.mouth_offset_x
        self.mouth_rect.y = self.rect.y + self.mouth_offset_y
    

#manejador de niveles, si el nivel es uno ta ta ta ta.

##############################NIVEL 1#########################################
nivel_actual = 1
nivel1 = Level1()
mostrar_imagen("img/shrek_y_fiona.jpg","Salva a Fiona, ha sido secuestrada por el principe!")
intro("audio/video_recuerdos.mp4")
music = nivel2.music_bg
world = nivel1.world
timer = Timer(60000)
timer.start()
gate = Gate("img/fotos/exit.png", 655, 40, 40, 60)
player = Player(30, screen_height - 40 - 70)
#boss = BossFinal(200, screen_height - 385, player)
enemy = Enemy(200, screen_height - 385, 250, 100)
enemy2 = Enemy(100, screen_height - 500, 250, 100)
enemy.player = player  # Asigna el objeto player al enemigo
boss = BossFinal(-500, 80, player)
boss_group = pygame.sprite.Group()
boss_group.add(boss)
world.enemies.add(enemy, enemy2)  # Agrega el enemigo al grupo de enemigos en world
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, enemy2, world.enemies)#, boss agregar
#####################################################################################

def pasar_al_siguiente_nivel():
    global nivel_actual, music, world, gate, player, enemy, enemy2, all_sprites
    nivel_actual += 1

    if nivel_actual == 2:
        # Configuración para el nivel 2
        nivel2 = Level2()
        mostrar_imagen("img/shrek_y_fiona.jpg","Te queda poco para salvarla, no te rindas")
        intro("audio/nivel_2_video.mp4")
        music = nivel2.music_bg
        world = nivel2.world
        timer = Timer(60000)  # Temporizador de 60 segundos
        timer.start()
        gate = Gate("img/fotos/exit.png", 655, 40, 40, 60)
        player = Player(600, screen_height - 80)
        player.direction = -1
        enemy = Enemy(200, screen_height - 385, 250, 100)
        enemy2 = Enemy(100, screen_height - 500, 250, 100)
        enemy3 = Enemy(400, screen_height - 300, 550, 400)
        enemy4 = Enemy(400, screen_height - 500, 550, 400)
        enemy.player = player
        boss = BossFinal(-500, 80, player)
        boss_group = pygame.sprite.Group()
        boss_group.add(boss)
        world.enemies.add(enemy, enemy2, enemy3, enemy4)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player, enemy, enemy2, enemy3, enemy4, world.enemies)
        
    elif nivel_actual == 3:
        # Configuración para el nivel 3
        nivel3 = Level3()
        world = nivel3.world
        mostrar_imagen("img/ogro.jpg", "")
        pygame.mixer.music.load("audio/MUSICA PARA SUSPENSO-ACCION - MUSIC FOR SUSPENSE-ACTION (1).mp3")
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1)  # Reproducir en bucle
        timer = Timer(60000)  # Temporizador de 60 segundos
        timer.start()
        gate = Gate("img/fotos/exit.png", 0, 90, 40, 60)
        player = Player(600, 600)
        boss = BossFinal(550, 80, player)
        boss.direction = -1
        player.direction = -1
        boss_group = pygame.sprite.Group()
        boss_group.add(boss)
        enemy = Enemy(490, screen_height - 300, 550, 290)
        enemy4 = Enemy(290, screen_height - 400, 550, 290)
        enemy.player = player
        world.enemies.add(enemy, enemy4)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player, world.enemies, enemy, enemy4, boss_group)
    elif nivel_actual == 4:
        intro("audio/video_final.mp4")
        mostrar_imagen("img/6877113.jpg","¡Lo haz hecho, Shrek y Fiona te lo agradeceran siempre!")



run = True

while run:

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
    blit_level_background(nivel_actual)
    
    for i in range(VIDAS):
        screen.blit(vida_img, (pos_vidas[0] + i * (vida_img.get_width() + 5), pos_vidas[1]))
    world.platforms.draw(screen)
    world.coins.draw(screen)
    world.life.draw(screen)
    gate.check_collision(player)
    gate.draw(screen)  # Dibujar la compuerta en la ventana
    # Actualizar y dibujar el contador de monedas
    screen.blit(coin_image, (590, 10))
    coin_text = world.coin_font.render("X"+ " " +str(world.coin_counter), True, (255, 255, 255))
    screen.blit(coin_text, (coin_image.get_width() + 600, 20))
    

    all_sprites.update()
    all_sprites.draw(screen)
    
    if not timer.update():
        # El temporizador está en curso
        minutes = timer.get_elapsed_time() // 60000
        seconds = (timer.get_elapsed_time() % 60000) // 1000
        time_string = "{:02d}:{:02d}".format(minutes, seconds)
        text = font.render(time_string, True, 'White')
        screen.blit(text, (350, 20))
    else:
        # El temporizador ha terminado
        # Realiza las acciones correspondientes
        player.kill()
        screen.blit(game_over_image, (0, 0))
        # Reinicia el temporizador para que comience de nuevo
        timer.reset()
    if player.dead:
        screen.blit(game_over_image, (0, 0))
    pygame.display.update()
pygame.quit()
