import pygame

class MouseHandler():
    def __init__(self, name, code):
        self.event_name = name
        self.handler_code = code
        
    def is_triggered(self, event):
        if self.event_name == 'scroll_up' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            return True
        if self.event_name == 'scroll_down' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            return True
        if self.event_name == 'mouse_button_released' and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return True
        return False
