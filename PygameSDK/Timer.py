import pygame

class Timer:
    def __init__(self):
        self.final_ticks = 0
        self.start_ticks = 0
        self.is_running = False
        
    def start_timer(self):
        if not self.is_running:
            self.start_ticks = pygame.time.get_ticks()
            self.is_running = True
        
    def stop_timer(self):
        if self.is_running:
            self.final_ticks = pygame.time.get_ticks() - self.start_ticks
            self.is_running = False
        
    def reset_timer(self):
        self.final_ticks = 0
        self.start_ticks = 0
        self.is_running = False
        
    def get_seconds(self):
        return ((pygame.time.get_ticks() - self.start_ticks) if self.is_running else self.final_ticks) // 1000
