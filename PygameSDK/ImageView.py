import pygame
from pygame import Rect
from PygameSDK.Label import *
from PygameSDK.ImageRessourceProvider import *

class ImageView(Label):
    def __init__(self, coord, bkg, border, text_info, image_info):
        super().__init__(coord, bkg, border, text_info)
        (self.image_path, self.keep_image_ratio, self.image_surface, self.image_zone) = image_info
        self.image_provider = ImageRessourceProvider()
        
    def display(self, window):
        if not self.is_visible:
            return
        if self.background_color != None:
            pygame.draw.rect(window, self.background_color, self.coordinates)
        self.display_image(window)
        if self.border_color != None:
            self.display_border(window)
        if self.text != None:
            self.show_text(window)
            
    def display_image(self, window):
        if self.image_path != None:
            image_surface = self.image_provider.get_image_surface(self.image_path, self.coordinates.size, self.keep_image_ratio)[0]
            window.blit(image_surface, self.coordinates)
        elif self.image_surface != None:
            window.blit(self.image_surface, self.coordinates, self.image_zone)
            
    def set_image_path(self, path):
        if self.image_path != path:
            self.image_path = path
            self.should_update = True
        
