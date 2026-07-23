import pygame
from pygame import Rect
from PygameSDK.Label import *

class ImageView:
    def __init__(self, coord, bkg, border, text_info, image_info):
        super().__init__(coord, bkg, border, text_info)
        (self.image_path, self.keep_image_ratio, self.image_surface, self.image_zone) = image_info
        
    def display(self, screen):
        pygame.draw.rect(screen, self.background_color, self.coordinates)
        self.display_image(screen)
        if self.border_color != None:
            self.display_border(screen)
        if self.text != None:
            self.show_text(screen)
            
    def display_image(self, screen):
        if self.image_path != None:
            surface = pygame.image.load(file_name)
            if self.keep_image_ratio:
                adapted_surface = pygame.transform.scale(surface, self.get_image_adjusted_size(surface.get_size()))
            else:
                adapted_surface = pygame.transform.scale(surface, self.coordinates.size)
            screen.blit(image, image_coordinates)
        elif self.image_surface != None:
            screen.blit(self.image_surface, self.coordinates, self.image_zone)
            
    def get_image_adjusted_size(image_size):
        (image_width, image_height) = image_size
        (view_width, view_height) = self.coordinates.size
        image_zone_width = min(image_width, view_width)
        image_zone_height = int(image_zone_width * image_height / image_width)
        if image_zone_height > view_height:
                image_zone_height = min(view_height, image_height)
                image_zone_width = int(image_zone_height * image_width / image_height)
        return (image_zone_width, image_zone_height)
        
