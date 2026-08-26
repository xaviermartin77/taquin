import math
import pygame
from PygameSDK.Color import *

class View:
    def __init__(self, v_m, size, f_i = [('arial', 30)], bkg_code = 'w'):
        self.view_model = v_m
        
        self.size = size
        
        self.screen = None
        self.background_color = Color(bkg_code)
        
        self.should_exit = False
        self.previous_view = None
        
        self.buttons = []
        self.labels = []
        
        self.font_infos = f_i
        self.fonts = []
        
    def setup_view(self):
        self.screen = pygame.display.set_mode(self.size)
        for font_info in self.font_infos:
            self.fonts.append(pygame.font.SysFont(font_info[0], font_info[1], False, False))
        self.view_model.next_view = None
        self.view_model.should_update = True
    
    def should_navigate(self):
        return self.view_model.next_view != None
    
    def get_next_view(self):
        return self.view_model.next_view
    
    def should_return(self):
        return self.view_model.should_return
        
    def generate_elements(self):
        self.shortcuts = []
        self.mouse_actions = []
        self.buttons = []
        self.labels = []
        # Generate UI elements here
    
    def check_inputs(self):
        if self.view_model.is_animating():
            self.view_model.update_animation()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.should_exit = True
            if self.view_model.is_animating():
                continue
            if event.type == pygame.KEYDOWN:
                for shortcut in self.shortcuts:
                    if shortcut.is_pressed(event.key):
                        self.view_model.handle_code(shortcut.handler_code)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_pushed(pos):
                        self.view_model.handle_code(button.handler_code)
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button != 1) or (event.type == pygame.MOUSEBUTTONUP):
                for mouse_action in self.mouse_actions:
                    if mouse_action.is_triggered(event):
                        self.view_model.handle_code(mouse_action.handler_code)
                        
    def update_if_needed(self):
        if self.view_model.should_update:
            self.generate_elements()
            self.display_view()
            self.view_model.updated()
            
    def display_view(self):
        self.screen.fill(self.background_color.get_color_value())
        self.display_elements()
        pygame.display.flip() #TODO : use pygame.display.update() with rectangles to update when SDK is ready
    
    def display_elements(self):
        for label in self.labels:
            label.display(self.screen)
        for button in self.buttons:
            button.display(self.screen)
