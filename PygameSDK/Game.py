import pygame
import weakref

class Game:
    def __init__(self):
        self.view = None
        
    def start_game(self, view):
        loop = True
        
        pygame.init()
        self.display_screen(view)
        
        while loop:
            self.view.check_inputs()
            if self.view.should_exit:
                loop = False
                continue
            if self.view.should_navigate():
                self.navigate()
            elif self.view.should_return():
                self.return_to_previous_view()
            else:
                self.view.update_if_needed()
        pygame.quit()
        
    def navigate(self):
        new_view = self.view.get_next_view()
        new_view.previous_view = weakref.ref(self.view)()
        self.display_screen(new_view)
        
    def return_to_previous_view(self):
        self.view.unload_ressources()
        previous_view = self.view.previous_view
        self.display_screen(previous_view)
        
    def display_screen(self, view):
        self.view = view
        self.view.setup_view()
        
