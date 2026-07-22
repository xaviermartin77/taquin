import math
import pygame
from PygameSDK.Color import *

class View:
    def __init__(self, v_m, size, f_i = ('arial', 30)):
        self.view_model = v_m
        
        self.size = size
        
        self.screen = None
        
        self.should_exit = False
        
        self.buttons = []
        self.labels = []
        
        self.font_info = f_i
        
    def setup_screen(self):
        self.screen = pygame.display.set_mode(self.size)
        
        self.generate_elements()
        self.display_view()
        
    def root_to_view(self):
        return None
        
    def generate_elements(self):
        self.shortcuts = []
        self.buttons = []
        self.labels = []
        self.font = pygame.font.SysFont(self.font_info[0], self.font_info[1], False, False)
        # Generate UI elements here
    
    def check_inputs(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.should_exit = True
            if event.type==pygame.KEYDOWN:
                for shortcut in self.shortcuts:
                    if shortcut.is_pressed(event.key):
                        self.view_model.handle_code(shortcut.handler_code)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_pushed(pos):
                        self.view_model.handle_code(button.handler_code)
                        
    def update_if_needed(self):
        if self.view_model.should_update:
            self.generate_elements()
            self.display_view()
            self.view_model.updated()
            
    def display_view(self):
        self.screen.fill(Color.white)
        self.display_elements()
        pygame.display.update()
    
    def display_elements(self):
        for label in self.labels:
            label.display(self.screen)
        for button in self.buttons:
            button.display(self.screen)
