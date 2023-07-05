nivel_actual = 1
nivel1 = Level1()
mostrar_imagen("img/shrek_y_fiona.jpg","Salva a Fiona, ha sido secuestrada por el principe!")
intro("audio/video_recuerdos.mp4")
music = nivel2.music_bg
timer.start()
world = nivel1.world
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