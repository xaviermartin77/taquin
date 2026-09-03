import pygame
from pygame import Rect

class Animation:
    def __init__(self, code, start_info, anim_info, frames = 30):
        self.animation_code = code
        self.start_state_info = start_info
        self.animation_info = anim_info
        self.animation_frame_count = frames
        self.animation_progress = 0
        
    def get_full_zone(self):
        if self.animation_code == 'moving':
            (x_translation, y_translation) = self.animation_info
            (x, y, w, h) = self.start_state_info
            start_x = x + x_translation if x_translation < 0 else x
            start_y = y + y_translation if y_translation < 0 else y
            width = w + (-1 * x_translation) if x_translation < 0 else w + x_translation
            height = h + (-1 * y_translation) if y_translation < 0 else h + y_translation
            return Rect(start_x, start_y, width, height)
        return Rect(0, 0, 0, 0)
        
    def increment_step(self):
        self.animation_progress += 1
        
    def get_current_position(self):
        if self.animation_code == 'moving':
            (x_total_translation, y_total_translation) = self.animation_info
            (x, y, w, h) = self.start_state_info
            x_current_position = x + (x_total_translation * self.animation_progress / self.animation_frame_count)
            y_current_position = y + (y_total_translation * self.animation_progress / self.animation_frame_count)
            return Rect(x_current_position, y_current_position, w, h)
        return Rect(0, 0, 0, 0)
        
    def is_completed(self):
        return self.animation_progress == self.animation_frame_count
    
