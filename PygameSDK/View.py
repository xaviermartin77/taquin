import math
import pygame
from PygameSDK.Color import *
from PygameSDK.Button import *

class View:
    def __init__(self, v_m, size, f_i = [('arial', 30)], bkg_code = 'w'):
        self.view_model = v_m
        
        self.size = size
        
        self.screen = None
        self.background_color = Color(bkg_code)
        
        self.should_exit = False
        self.previous_view = None
        
        self.elements = []
        self.elements_to_hide = []
        
        self.font_infos = f_i
        self.fonts = []
        
        self.animation_zone = None
        
    def setup_view(self):
        self.screen = pygame.display.set_mode(self.size)
        for font_info in self.font_infos:
            self.fonts.append(pygame.font.SysFont(font_info[0], font_info[1], False, False))
        self.view_model.next_view = None
        
        self.generate_elements()
        self.screen.fill(self.background_color.get_color_value())
        for element in self.elements:
            element.should_update = False
            element.display(self.screen)
        pygame.display.flip()
    
    def should_navigate(self):
        return self.view_model.next_view != None
    
    def get_next_view(self):
        return self.view_model.next_view
    
    def should_return(self):
        return self.view_model.should_return
    
    def unload_ressources(self):
        print('unloading ressources')
        
    def generate_elements(self):
        self.shortcuts = []
        self.mouse_actions = []
        self.elements = []
        # Generate UI elements here
        
    def update_elements(self, update_state):
        return ([], [], [])
    
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
                for button in self.get_button_list():
                    if button.is_pushed(pos):
                        self.view_model.handle_code(button.handler_code)
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button != 1) or (event.type == pygame.MOUSEBUTTONUP):
                for mouse_action in self.mouse_actions:
                    if mouse_action.is_triggered(event):
                        self.view_model.handle_code(mouse_action.handler_code)
    
    def get_button_list(self):
        return [element for element in self.elements if (isinstance(element, Button) or isinstance(element, ImageButton))]
                        
    def update_if_needed(self):
        self.update_elements()
        update_rect_list = []
        if self.animation_zone != None:
            update_rect_list.append(self.animation_zone.copy())
            self.animation_zone = None
        
        for old_element in self.elements_to_hide:
            update_rect_list.append(element.coordinates)
        self.elements_to_hide = []
            
        for element in self.elements:
            if element.should_update:
                element.should_update = False
                update_rect_list.append(element.coordinates)
        
        if len(update_rect_list) > 0 :
            for element in self.elements:
                element.display(self.screen)
            pygame.display.update(update_rect_list)
        
    def update_elements(self):
        print('updating elements')
        # update ui elements with view_model updates
        
    def remove_element(self, element):
        self.elements_to_hide.append(element)
        self.elements.remove(element)
