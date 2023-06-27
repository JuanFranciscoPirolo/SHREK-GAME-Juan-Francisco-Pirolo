import pygame
from main_principal import lose_life
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
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
                all_sprites = pygame.sprite.Group()
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
