from PygameSDK.ViewModel import *
from TaquinEntity.TaquinImageProvider import *
from TaquinGridScreen import *
from TaquinGridViewModel import *

class TaquinImagesViewModel(ViewModel):
    def __init__(self, grid_dim = (3, 4)):
        super().__init__()
        
        self.images_grid_dimensions = grid_dim
        self.image_provider = TaquinImageProvider()
        self.generate_image_list()
        
        self.first_list_index = 0
        self.game_width = 4
        self.game_height = 2
        self.selected_image_index = 0
    
    def generate_image_list(self):
        self.image_list = self.image_provider.generate_default_images()
        
    def get_grid_size(self):
        return self.images_grid_dimensions[0] * self.images_grid_dimensions[1]
    
    # superclass methods
    def handle_code(self, code):
        if code == 'decrement_width':
            self.decrement_game_width()
        if code == 'increment_width':
            self.increment_game_width()
        if code == 'decrement_height':
            self.decrement_game_height()
        if code == 'increment_height':
            self.increment_game_height()
        if code == 'scroll_images_up':
            self.scroll_images_up()
        if code == 'scroll_images_down':
            self.scroll_images_down()
        if 'select_index_' in code:
            selected_index = int(code.split('select_index_', 1)[1])
            self.select_image(selected_index)
        if code == 'start_game':
            self.switch_to_game_screen()
    
    # action handlers
    def decrement_game_width(self):
        self.game_width = self.game_width - 1

    def increment_game_width(self):
        self.game_width = self.game_width + 1

    def decrement_game_height(self):
        self.game_height = self.game_height - 1

    def increment_game_height(self):
        self.game_height = self.game_height + 1

    def scroll_images_up(self):
        if self.first_list_index - self.images_grid_dimensions[0] >= 0:
            self.first_list_index = self.first_list_index - self.images_grid_dimensions[0]

    def scroll_images_down(self):
        image_list_length = self.get_grid_size()
        if self.first_list_index + image_list_length < len(self.image_list):
            self.first_list_index = self.first_list_index + self.images_grid_dimensions[0]

    def select_image(self, selected_index):
        real_index = selected_index + self.first_list_index
        if real_index < len(self.image_list):
            self.selected_image_index = real_index
    
    def switch_to_game_screen(self):
        game_size = (self.game_width, self.game_height)
        view_model = TaquinGridViewModel(game_size)
        
        selected_image = self.image_list[self.selected_image_index]
        selected_image.load_image_ressource((1400, 1000), game_size)
        
        screen_size = (selected_image.image_size[0] + 100, selected_image.image_size[1])
        
        self.next_screen = TaquinGridScreen(view_model, screen_size, selected_image)

    # data providers for UI
    def should_display_minus_button_for_width(self):
        return self.game_width > 2
        
    def should_display_plus_button_for_width(self):
        return self.game_width < 20
        
    def should_display_minus_button_for_height(self):
        return self.game_height > 2
        
    def should_display_plus_button_for_height(self):
        return self.game_height < 20
    
    def get_displayed_images(self):
        last_index = self.first_list_index + self.get_grid_size()
        if last_index >= len(self.image_list):
            last_index = len(self.image_list)
        return self.image_list[self.first_list_index:last_index]
        
    def get_relative_selected_index(self):
        return self.selected_image_index - self.first_list_index
                
                
