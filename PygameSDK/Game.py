import pygame
import weakref

class Game:
    def __init__(self):
        self.screen = None
        
    def start_game(self, screen):
        loop = True
        
        pygame.init()
        self.display_screen(screen)
        
        while loop:
            self.screen.check_inputs()
            if self.screen.should_exit:
                loop = False
                continue
            if self.screen.should_navigate():
                self.navigate()
            elif self.screen.should_return():
                self.return_to_previous_screen()
            else:
                self.screen.update_if_needed()
        pygame.quit()
        
    def navigate(self):
        new_screen = self.screen.get_next_screen()
        new_screen.previous_screen = weakref.ref(self.screen)()
        self.display_screen(new_screen)
        
    def return_to_previous_screen(self):
        self.screen.unload_ressources()
        previous_screen = self.screen.previous_screen
        self.display_screen(previous_screen)
        
    def display_screen(self, screen):
        self.screen = screen
        self.screen.setup_screen()
        
