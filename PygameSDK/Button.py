import pygame
from pygame import Rect
from PygameSDK.Label import *
from PygameSDK.ImageView import *

class Button(Label):
    def __init__(self, coord, bkg, border, text_info, code):
        super().__init__(coord, bkg, border, text_info)
        self.handler_code = code
        
    def is_pushed(self, pos):
        return pos[0] > self.coordinates.left and pos[0] < self.coordinates.right and pos[1] > self.coordinates.top and pos[1] < self.coordinates.bottom

class ImageButton(ImageView):
    def __init__(self, coord, bkg, border, text_info, image_info, code):
        super().__init__(coord, bkg, border, text_info, image_info)
        self.handler_code = code
        
    def is_pushed(self, pos):
        return pos[0] > self.coordinates.left and pos[0] < self.coordinates.right and pos[1] > self.coordinates.top and pos[1] < self.coordinates.bottom
        
class TriangleButton(Button):
    def __init__(self, coord, bkg, border, code, orcode):
        super().__init__(coord, bkg, border, None, code)
        self.orientation = orcode
            
    def is_pushed(self, pos):
        if not super().is_pushed(pos):
            return False
        x_converted = (pos[0] - self.coordinates.left)/self.coordinates.width
        y_converted = (pos[1] - self.coordinates.top)/self.coordinates.height
        if self.orientation == 0:
            return x_converted + y_converted < 1
        if self.orientation == 1:
            return x_converted + y_converted > 1
        if self.orientation == 2:
            return x_converted < y_converted
        if self.orientation == 3:
            return x_converted > y_converted
            
    def display(self, screen):
        if self.orientation == 0:
            points = [self.coordinates.topleft, self.coordinates.topright, self.coordinates.bottomleft]
        if self.orientation == 1:
            points = [self.coordinates.topright, self.coordinates.bottomleft, self.coordinates.bottomright]
        if self.orientation == 2:
            points = [self.coordinates.topleft, self.coordinates.bottomleft, self.coordinates.bottomright]
        if self.orientation == 3:
            points = [self.coordinates.topleft, self.coordinates.topright, self.coordinates.bottomright]
        if self.background_color != None:
            pygame.draw.polygon(screen, self.background_color, points)
        if self.border_color != None:
            pygame.draw.line(screen, self.border_color, points[0], points[1])
            pygame.draw.line(screen, self.border_color, points[1], points[2])
            pygame.draw.line(screen, self.border_color, points[2], points[0])
