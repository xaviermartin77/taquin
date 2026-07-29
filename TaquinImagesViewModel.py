from PygameSDK.ViewModel import *
from TaquinImage import *

class TaquinImagesViewModel(ViewModel):
    def __init__(self, grid_dim = (3, 4)):
        super().__init__()
        
        self.images_grid_dimensions = grid_dim
        self.image_provider = TaquinImageProvider()
        self.generate_image_list()
        
        self.first_list_index = 0
        self.game_width = 3
        self.game_height = 3
        self.selected_image_index = 0
    
    def generate_image_list(self):
        self.image_list = self.image_provider.generate_default_images()
    
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
            self.root_to_game_view()
    
    # action handlers
    def decrement_game_width(self):
        self.game_width = self.game_width - 1
        self.should_update = True

    def increment_game_width(self):
        self.game_width = self.game_width + 1
        self.should_update = True

    def decrement_game_height(self):
        self.game_height = self.game_height - 1
        self.should_update = True

    def increment_game_height(self):
        self.game_height = self.game_height + 1
        self.should_update = True

    def scroll_images_up(self):
        if self.first_list_index - self.images_grid_dimensions[0] >= 0:
            self.first_list_index = self.first_list_index - self.images_grid_dimensions[0]
            self.should_update = True

    def scroll_images_down(self):
        image_list_length = self.images_grid_dimensions[0] * self.images_grid_dimensions[1]
        if self.first_list_index + image_list_length < len(self.image_list):
            self.first_list_index = self.first_list_index + self.images_grid_dimensions[0]
            self.should_update = True

    def select_image(self, selected_index):
        if selected_index < len(self.image_list):
            self.selected_image_index = selected_index
            self.should_update = True
    
    def root_to_game_view(self):
        print('starting game')
        print('chosen game width : ' + str(self.game_width))
        print('chosen game height : ' + str(self.game_height))
        selected_image = self.image_list[self.selected_image_index]
        print('image selected : ' + selected_image.file_path)
        print('switching to new view')

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
        grid_size = self.images_grid_dimensions[0] * self.images_grid_dimensions[1]
        last_index = self.first_list_index + grid_size
        if last_index >= len(self.image_list):
            last_index = len(self.image_list)
        return self.image_list[self.first_list_index:last_index]
        
    def get_real_index(self, index):
        return index + self.first_list_index
                
                
