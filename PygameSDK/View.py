import pygame
from pygame import Rect
from PygameSDK.Animation import *

class View:
    def __init__(self, coord, bkg, border):
        self.coordinates = coord
        self.background_color = bkg
        self.border_color = border
        self.is_visible = True
        self.should_update = False
        self.animation = None
        self.animation_zone = None
        
    def display(self, window):
        if not self.is_visible:
            return
        if self.background_color != None:
            pygame.draw.rect(window, self.background_color, self.coordinates)
        if self.border_color != None:
            self.display_border(window)
            
    def display_border(self, window):
        pygame.draw.line(window, self.border_color, self.coordinates.topleft, self.coordinates.topright)
        pygame.draw.line(window, self.border_color, self.coordinates.bottomleft, self.coordinates.bottomright)
        pygame.draw.line(window, self.border_color, self.coordinates.topleft, self.coordinates.bottomleft)
        pygame.draw.line(window, self.border_color, self.coordinates.topright, self.coordinates.bottomright)
            
    def set_visibility(self, show):
        if self.is_visible != show:
            self.is_visible = show
            self.should_update = True
            
    def set_coordinates(self, coord):
        if self.coordinates != coord:
            self.coordinates = coord
            self.should_update = True
            
    def set_border_color(self, border):
        if self.border_color != border:
            self.border_color = border
            self.should_update = True
            
    def set_bkg_color(self, bkg):
        if self.background_color != bkg:
            self.background_color = bkg
            self.should_update = True
            
    def start_animation(self, animation):
        self.animation_zone = animation.get_full_zone()
        self.animation = animation
            
    def update_animation(self):
        if self.animation == None:
            return True
        
        self.animation.increment_step()
        self.set_coordinates(self.animation.get_current_position())
            
        if self.animation.is_completed():
            self.animation = None
            self.animation_zone = None
            return True
        return False
            
    def is_animating(self):
        return self.animation != None
    
