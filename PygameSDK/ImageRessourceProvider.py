import pygame
from pygame import Rect

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
