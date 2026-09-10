import pygame
from pygame import Rect
from PygameSDK.View import *

class Label(View):
    def __init__(self, coord, bkg, border, text_info):
        super().__init__(coord, bkg, border)
        if text_info != None:
            (self.text, self.text_color, self.font, self.multiple_text_lines) = text_info
        else:
            self.text = None
        
    def display(self, window):
        displaying = super().display(window)
        if self.is_visible and self.text != None:
            self.show_text(window)
            
    def set_text(self, txt):
        if self.text != txt:
            self.text = txt
            self.should_update = True
            
    def set_text_color(self, txt_clr):
        if self.text_color != txt_clr:
            self.text_color = txt_clr
            self.should_update = True
        
    def show_text(self, window):
        if self.multiple_text_lines:
            words = self.text.split()
            lines = []
            current_line = ''
            for word in words:
                new_line = current_line + ' ' + word
                text_surface = self.font.render(new_line, True, self.text_color)
                text_rect = text_surface.get_rect()
                if text_rect.width > self.coordinates.width:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = new_line
            lines.append(current_line)
            line_height = self.coordinates.height/len(lines)
            for index, line in enumerate(lines):
                text_surface = self.font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.coordinates.centerx, self.coordinates.top + line_height*index + line_height/2)
                window.blit(text_surface, text_rect)
        else:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.coordinates.center
            window.blit(text_surface, text_rect)
