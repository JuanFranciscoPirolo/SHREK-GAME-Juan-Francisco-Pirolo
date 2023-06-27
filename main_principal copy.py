import pygame
import pygame.mixer
from pygame.locals import *
from enemy import Enemy
from world import World
from jugador import Player
from level1 import Level1

pygame.init()
#musica
fire_sound = pygame.mixer.Sound("audio/Efecto de Sonido - Fuego (Incendio).mp3")
death_sound = pygame.mixer.Sound("audio/Sonido de muerte de Fortnite-Death Fortnite sound.mp3")
life_sound = pygame.mixer.Sound("audio/Sonido de experiencia en minecraft.mp3")
coin_sound = pygame.mixer.Sound("audio/coin.wav")
punch_sound = pygame.mixer.Sound("audio/Efecto de sonido- Golpe.mp3")
#pygame.mixer.music.load('audio/X2Download.app - Dirty Deeds Done Dirt Cheap (128 kbps).mp3')  # Load the background music
#pygame.mixer.music.play(-1)  # Start playing the background music
clock = pygame.time.Clock()
fps = 60
# Configuración de pantalla
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Imágenes cargadas
coin_image = pygame.image.load("img/coin.png")
coin_image = pygame.transform.scale(coin_image,(60,60))
vida_img = pygame.image.load('img/life.png')
vida_img = pygame.transform.scale(vida_img, (40, 35))
bg_img = pygame.image.load('img/fotos/shrekfondo.png')
VIDAS = 5
pos_vidas = (10, 10)  # Coordenadas (x, y) de la esquina superior izquierda donde se mostrarán las vidas

pygame.display.set_caption("Salva a Fiona")

#Perder una vida
def lose_life():
    global VIDAS

    if VIDAS > 0:
        VIDAS -= 1
    
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
        self.image = self.images_right[self.index]
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
            if self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
        
        self.counter += 1
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
    
        self.collided_enemies = []
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
        self.health = 100  # Valor inicial de la vida
        self.mouth_offset_x = 120  # Offset en la coordenada X de la boca del dragón
        self.mouth_offset_y = 60  # Offset en la coordenada Y de la boca del dragón
        self.fireball_timer = 0
        self.fireball_delay = 100  # Intervalo de tiempo entre lanzamientos de bolas de fuego
        self.projectiles = pygame.sprite.Group()  # Grupo para almacenar los proyectiles
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

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.direction = 1
        else:
            self.direction = -1

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

        # Actualizar la posición del rectángulo de la boca
        self.mouth_rect.x = self.rect.x + self.mouth_offset_x
        self.mouth_rect.y = self.rect.y + self.mouth_offset_y


world = World()
player = Player(30, screen_height - 40 - 70)
boss = BossFinal(200, screen_height - 385, player)
enemy = Enemy(200, screen_height - 385, 250, 100)
enemy2 = Enemy(100, screen_height - 500, 250, 100)
enemy.player = player  # Asigna el objeto player al enemigo
world.enemies.add(enemy, enemy2)  # Agrega el enemigo al grupo de enemigos en world

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, enemy2, boss)



all_sprites.add(world.enemies)  # Agrega el grupo de enemigos al grupo all_sprites
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
        coin_sound.set_volume(0.04)

    collisions = pygame.sprite.spritecollide(player, world.life, True)
    for life in collisions:
        if VIDAS < 5:
            VIDAS += 1
        life_sound.play()
        life_sound.set_volume(0.01)
    # Actualizar las plataformas
    world.platforms.update()
    
    # Dibujar en la pantalla
    screen.blit(bg_img, (-100, -60))
    for i in range(VIDAS):
        screen.blit(vida_img, (pos_vidas[0] + i * (vida_img.get_width() + 5), pos_vidas[1]))
    world.platforms.draw(screen)
    world.coins.draw(screen)
    world.life.draw(screen)
    # Actualizar y dibujar el contador de monedas
    screen.blit(coin_image, (590, 5))
    coin_text = world.coin_font.render("X"+ " " +str(world.coin_counter), True, (255, 255, 255))
    screen.blit(coin_text, (coin_image.get_width() + 600, 20))


    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
