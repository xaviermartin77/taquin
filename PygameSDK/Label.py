import math
import pygame
from pygame import Rect

class Label:
    def __init__(self, bkg, border, textclr, txt, ft, rect, m_text_lines = False):
        self.background_color = bkg
        self.border_color = border
        self.text_color = textclr
        self.text = txt
        self.coordinates = rect
        self.multiple_text_lines = m_text_lines
        self.font = ft
        
    def display(self, screen):
        pygame.draw.rect(screen, self.background_color, self.coordinates)
        if self.border_color != None:
            self.display_border(screen)
        if self.text != None and self.font != None:
            self.show_text(screen)
            
    def display_border(self, screen):
        pygame.draw.line(screen, self.border_color, self.coordinates.topleft, self.coordinates.topright)
        pygame.draw.line(screen, self.border_color, self.coordinates.bottomleft, self.coordinates.bottomright)
        pygame.draw.line(screen, self.border_color, self.coordinates.topleft, self.coordinates.bottomleft)
        pygame.draw.line(screen, self.border_color, self.coordinates.topright, self.coordinates.bottomright)
        
    def show_text(self, screen):
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
                screen.blit(text_surface, text_rect)
        else:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.coordinates.center
            screen.blit(text_surface, text_rect)
