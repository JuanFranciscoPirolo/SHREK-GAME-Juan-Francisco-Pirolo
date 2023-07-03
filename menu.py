import pygame
import pygame.mixer
from pygame.locals import *

pygame.init()

# Música
coin_sound = pygame.mixer.Sound("audio/coin.wav")
pygame.mixer.music.load('audio/X2Download.app - Dirty Deeds Done Dirt Cheap (128 kbps).mp3')  # Load the background music
pygame.mixer.music.set_volume(0.5)  # Establecer el volumen inicial
pygame.mixer.music.play(-1)  # Start playing the background music

clock = pygame.time.Clock()
fps = 60

# Configuración de pantalla
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Imágenes cargadas
coin_image = pygame.image.load("img/coin.png")
coin_image = pygame.transform.scale(coin_image, (60, 60))
vida_img = pygame.image.load('img/life.png')
vida_img = pygame.transform.scale(vida_img, (40, 35))
bg_img = pygame.image.load('img/fotos/shrekfondo.png')
VIDAS = 5
pos_vidas = (10, 10)  # Coordenadas (x, y) de la esquina superior izquierda donde se mostrarán las vidas

pygame.display.set_caption("Salva a Fiona")


class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        self.additional_images_visible = False

        self.button_font = pygame.font.Font(None, 30)
        self.show_additional_section = False  # Estado de visualización del apartado adicional

        self.additional_section_bg_img = pygame.image.load('img/fotos/shrekfondo.png')  # Carga de la imagen de fondo para el apartado adicional
        # Imágenes de los botones
        self.settings_button_img = pygame.image.load("botones/green_home.png")
        self.settings_button_img = pygame.transform.scale(self.settings_button_img, (50, 50))

        self.sound_effects_button_img = pygame.image.load("botones/green_star.png")
        self.sound_effects_button_img = pygame.transform.scale(self.sound_effects_button_img, (50, 50))

        self.music_on_button_img = pygame.image.load("botones/not_sound_green.png")
        self.music_on_button_img = pygame.transform.scale(self.music_on_button_img, (50, 50))

        self.music_off_button_img = pygame.image.load("botones/green_sound.png")
        self.music_off_button_img = pygame.transform.scale(self.music_off_button_img, (50, 50))

        self.slider_bg_img = pygame.image.load("img/barrita.png")
        self.slider_bg_img = pygame.transform.scale(self.slider_bg_img, (200, 20))

        self.slider_button_img = pygame.image.load("botones/circulo.png")
        self.slider_button_img = pygame.transform.scale(self.slider_button_img, (30, 30))

        button_offset_x = 65  # Valor para mover los botones hacia la derecha
        button_offset_y = -20 # Valor para mover los botones hacia abajo

        self.settings_button_rect = pygame.Rect(self.screen_width // 2 - self.button_width // 2 + button_offset_x,
                                                self.screen_height // 2 - self.button_height - self.button_margin + button_offset_y,
                                                self.button_width, self.button_height)
        self.sound_effects_button_rect = pygame.Rect(self.screen_width // 2 - self.button_width // 2 + button_offset_x,
                                                    self.screen_height // 2 + button_offset_y,
                                                    self.button_width, self.button_height)
        self.music_button_rect = pygame.Rect(self.screen_width // 2 - self.button_width // 2 + button_offset_x,
                                            self.screen_height // 2 + self.button_height + self.button_margin + button_offset_y,
                                            self.button_width, self.button_height)

        self.slider_bg_rect = pygame.Rect(self.screen_width // 2 - self.slider_bg_img.get_width() // 2,
                                          self.music_button_rect.bottom + self.button_margin,
                                          self.slider_bg_img.get_width(), self.slider_bg_img.get_height())

        self.slider_button_rect = pygame.Rect(self.slider_bg_rect.left,
                                              self.slider_bg_rect.centery - self.slider_button_img.get_height() // 2,
                                              self.slider_button_img.get_width(), self.slider_button_img.get_height()) 



        self.music_on = True  # Estado del botón de música (activado o desactivado)
        self.sound_effects_on = True  # Estado del botón de efectos de sonido (activado o desactivado)
        self.settings_menu_open = False  # Estado del menú de configuración (abierto o cerrado)

        self.button_state = "On"  # Estado inicial del botón

        self.is_dragging_slider = False  # Variable para rastrear si se está arrastrando el control deslizante


    def draw(self):
        self.screen.fill((255, 255, 255))  # Fondo blanco

        if self.settings_menu_open:
            # Crear y configurar el rectángulo del menú
            menu_width = 400
            menu_height = 300
            menu_x = (self.screen_width - menu_width) // 2
            menu_y = (self.screen_height - menu_height) // 2
            settings_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

            # Dibujar el rectángulo del menú
            pygame.draw.rect(self.screen, (0, 0, 0), settings_menu_rect)

            # Cargar la imagen de fondo del menú
            menu_background_img = pygame.image.load("img/fotos/HD-wallpaper-black-wood-graphics-texture-wood.jpg")
            menu_background_img = pygame.transform.scale(menu_background_img, (menu_width, menu_height))

            # Dibujar la imagen de fondo del menú
            self.screen.blit(menu_background_img, settings_menu_rect)

            # Dibujar botones y control deslizante solo si el menú está abierto
            self.draw_button(self.settings_button_img, self.settings_button_rect)
            self.draw_button(self.sound_effects_button_img, self.sound_effects_button_rect)
            self.draw_button(self.get_music_button_img(), self.music_button_rect)
            self.draw_slider()
                # Dibujar el apartado adicional si está activado
        if self.show_additional_section:
            self.screen.blit(self.additional_section_bg_img, (0, 0))  # Dibuja la imagen de fondo en la posición deseada

    def draw_button(self, button_img, button_rect):
        # Dibujar el botón
        self.screen.blit(button_img, button_rect)

    def get_button_text(self):
            return "On" if self.button_state == "Off" else "Off"

    def get_music_button_img(self):
        return self.music_on_button_img if self.button_state == "Off" else self.music_off_button_img

    def draw_slider(self):
        # Dibujar el fondo del control deslizante
        self.screen.blit(self.slider_bg_img, self.slider_bg_rect)

        # Calcular la posición x del botón del control deslizante en función del volumen actual
        slider_button_x = self.slider_bg_rect.left + (
                self.slider_bg_rect.width - self.slider_button_rect.width) * pygame.mixer.music.get_volume()

        # Actualizar la posición x del botón del control deslizante
        self.slider_button_rect.x = slider_button_x

        # Dibujar el botón del control deslizante
        self.screen.blit(self.slider_button_img, self.slider_button_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Alternar el estado del menú al presionar la tecla "Esc"
                self.settings_menu_open = not self.settings_menu_open
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Alternar el estado del botón de música al hacer clic
                if self.music_button_rect.collidepoint(event.pos):
                    if self.button_state == "Off":
                        self.button_state = "On"
                        pygame.mixer.music.unpause()  # Reanudar la reproducción de música
                    else:
                        self.button_state = "Off"
                        pygame.mixer.music.pause()  # Pausar la reproducción de música
                # Comprobar si se hizo clic en el control deslizante
                elif self.slider_button_rect.collidepoint(event.pos):
                    self.is_dragging_slider = True
                # Comprobar si se hizo clic en el botón de inicio
                elif self.settings_button_rect.collidepoint(event.pos):
                    # Aquí puedes agregar la lógica para el botón de inicio
                    print("Se presionó el botón de inicio")
                    self.show_additional_section = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Dejar de arrastrar el control deslizante cuando se suelta el botón del mouse
                self.is_dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                # Actualizar la posición del control deslizante mientras se arrastra
                if self.is_dragging_slider:
                    # Calcular el volumen basado en la posición x del control deslizante
                    volume = (event.pos[0] - self.slider_bg_rect.left) / (
                            self.slider_bg_rect.width - self.slider_button_rect.width)
                    # Asegurarse de que el volumen esté en el rango de 0 a 1
                    volume = max(0, min(volume, 1))
                    # Establecer el volumen de la música
                    pygame.mixer.music.set_volume(volume)



loading_screen = LoadingScreen(screen)
run = True

while run:
    loading_screen.draw()
    clock.tick(fps)

    # Manejo de eventos
    events = pygame.event.get()
    loading_screen.handle_events(events)

    for event in events:
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()
