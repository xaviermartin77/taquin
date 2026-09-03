import math
import pygame
from PygameSDK.Color import *
from PygameSDK.Buttons import *

class Screen:
    def __init__(self, v_m, size, f_i = [('arial', 30)], bkg_code = 'w'):
        self.view_model = v_m
        
        self.size = size
        
        self.window = None
        self.background_color = Color(bkg_code)
        
        self.should_exit = False
        self.previous_screen = None
        
        self.views = []
        self.views_to_hide = []
        
        self.font_infos = f_i
        self.fonts = []
        
    def setup_screen(self):
        self.window = pygame.display.set_mode(self.size)
        for font_info in self.font_infos:
            self.fonts.append(pygame.font.SysFont(font_info[0], font_info[1], False, False))
        self.view_model.next_screen = None
        
        self.generate_views()
        self.window.fill(self.background_color.get_color_value())
        for view in self.views:
            view.should_update = False
            view.display(self.window)
        pygame.display.flip()
    
    def should_navigate(self):
        return self.view_model.next_screen != None
    
    def get_next_screen(self):
        return self.view_model.next_screen
    
    def should_return(self):
        return self.view_model.should_return
    
    def unload_ressources(self):
        print('unloading ressources')
        
    def generate_views(self):
        self.shortcuts = []
        self.mouse_actions = []
        self.views = []
        # Generate UI views here
        
    def update_views(self, update_state):
        return ([], [], [])
    
    def check_inputs(self):
        self.update_animation()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.should_exit = True
            if self.is_animating():
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
        return [view for view in self.views if (isinstance(view, Button) or isinstance(view, ImageButton))]
                        
    def update_if_needed(self):
        update_rect_list = []
        if not self.is_animating():
            self.update_views()
        else:
            update_rect_list.append(self.animation_zone())
        
        for old_view in self.views_to_hide:
            update_rect_list.append(view.coordinates)
        self.views_to_hide = []
            
        for view in self.views:
            if view.should_update:
                view.should_update = False
                update_rect_list.append(view.coordinates)
        
        if len(update_rect_list) > 0 :
            for view in self.views:
                view.display(self.window)
            pygame.display.update(update_rect_list)
        
    def update_views(self):
        print('updating views')
        # update ui views with view_model updates
        
    def remove_view(self, view):
        self.views_to_hide.append(view)
        self.views.remove(view)
        
    def animating_view(self):
        animating_views = [view for view in self.views if view.is_animating()]
        return animating_views[0] if len(animating_views) > 0 else None
        
    def is_animating(self):
        return self.animating_view() != None
        
    def animation_zone(self):
        if not self.is_animating():
            return None
        return self.animating_view().animation_zone
        
    def update_animation(self):
        if not self.is_animating():
            return
        animation_completed = self.animating_view().update_animation()
        if animation_completed:
            self.view_model.did_complete_animation()
