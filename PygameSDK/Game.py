import pygame

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
            new_view = self.view.navigate_to_view()
            if new_view != None:
                self.display_screen(new_view)
            else:
                self.view.update_if_needed()
        pygame.quit()
        
    def display_screen(self, view):
        self.view = view
        
        self.view.setup_view()
        
