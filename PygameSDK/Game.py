import pygame

class Game:
    def __init__(self):
        self.view = None
        
    def start_game(self, view):
        loop = True
        
        pygame.init()
        self.update_screen(view)
        
        while loop:
            self.view.check_inputs()
            if self.view.should_exit:
                loop = False
            self.view.update_if_needed()
            new_view = self.view.root_to_view()
            if new_view != None:
                update_screen(new_view)
        pygame.quit()
        
    def update_screen(self, view):
        self.view = view
        
        self.view.setup_screen()
        
