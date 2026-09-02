import pygame
from pygame import Rect
from PygameSDK.Label import *

class ImageRessourceProvider:
    def get_image_surface(self, image_path, rect_size, keep_ratio, adjustement = None):
        surface = pygame.image.load(image_path)
        if keep_ratio:
            adapted_surface = pygame.transform.scale(surface, self.get_image_adjusted_size(surface.get_size(), rect_size, adjustement))
        else:
            adapted_surface = pygame.transform.scale(surface, rect_size)
        return (adapted_surface, adapted_surface.get_size())
            
    def get_image_adjusted_size(self, image_size, rect_size, adjustement):
        (image_width, image_height) = image_size
        (view_width, view_height) = rect_size
        image_zone_width = min(image_width, view_width)
        image_zone_height = int(image_zone_width * image_height / image_width)
        if image_zone_height > view_height:
            image_zone_height = min(view_height, image_height)
            image_zone_width = int(image_zone_height * image_width / image_height)
        if adjustement != None:
            image_zone_width = image_zone_width - image_zone_width%adjustement[0]
            image_zone_height = image_zone_height - image_zone_height%adjustement[1]
        return (image_zone_width, image_zone_height)
        

class ImageView(Label):
    def __init__(self, coord, bkg, border, text_info, image_info):
        super().__init__(coord, bkg, border, text_info)
        (self.image_path, self.keep_image_ratio, self.image_surface, self.image_zone) = image_info
        self.image_provider = ImageRessourceProvider()
        
    def display(self, screen):
        if not self.is_visible:
            return
        if self.background_color != None:
            pygame.draw.rect(screen, self.background_color, self.coordinates)
        self.display_image(screen)
        if self.border_color != None:
            self.display_border(screen)
        if self.text != None:
            self.show_text(screen)
            
    def display_image(self, screen):
        if self.image_path != None:
            image_surface = self.image_provider.get_image_surface(self.image_path, self.coordinates.size, self.keep_image_ratio)[0]
            screen.blit(image_surface, self.coordinates)
        elif self.image_surface != None:
            screen.blit(self.image_surface, self.coordinates, self.image_zone)
            
    def set_image_path(self, path):
        if self.image_path != path:
            self.image_path = path
            self.should_update = True
        
