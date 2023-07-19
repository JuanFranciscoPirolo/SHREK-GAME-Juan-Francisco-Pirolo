import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
    
    def start(self):
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
    
    def stop(self):
        self.is_running = False
    
    def update(self):
        if self.is_running:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            remaining_time = self.duration - elapsed_time

            if remaining_time <= 0:
                self.is_running = False
                return True
            else:
                self.elapsed_time = remaining_time
                return False
    
    def get_elapsed_time(self):
        return self.elapsed_time
    
    def reset(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False

    def resume(self):
        if not self.is_running:
            self.start_time = pygame.time.get_ticks() - (self.duration - self.elapsed_time)
            self.is_running = True
