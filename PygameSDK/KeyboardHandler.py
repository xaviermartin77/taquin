import pygame

class KeyboardHandler():
    def __init__(self, name, code):
        self.key_name = name
        self.handler_code = code
        
    def is_pressed(self, key):
        return self.key_name == pygame.key.name(key)

