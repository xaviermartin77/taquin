from PygameSDK.Label import *
from PygameSDK.Button import *
from PygameSDK.View import *
from PygameSDK.MouseHandler import *

class TaquinImagesView(View):
    def __init__(self, v_m, size):
        super().__init__(v_m, size)
        self.interface_width = 400
        self.grid_width = self.size[0] - self.interface_width
        self.screen_height = self.size[1]
        
    def generate_elements(self):
        super().generate_elements()
        self.generate_interface()
        self.generate_images()
        self.generate_mouse_actions()
        
    def generate_interface(self):
        interface_start_x = self.grid_width
        
        self.labels.append(Label(Rect(interface_start_x, 0, self.interface_width, self.screen_height/3), Color.white, Color.black, None))
        self.labels.append(Label(Rect(interface_start_x, 0, self.interface_width, self.screen_height/6), None, None, ('Width', Color.black, self.fonts[0])))
        if self.view_model.should_display_minus_button_for_width():
            self.buttons.append(Button(Rect(interface_start_x, self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('-', Color.black, self.fonts[0]), 'decrement_width'))
        self.labels.append(Label(Rect(interface_start_x, self.screen_height/6, self.interface_width, self.screen_height/6), None, None, (str(self.view_model.game_width), Color.black, self.fonts[0])))
        if self.view_model.should_display_plus_button_for_width():
            self.buttons.append(Button(Rect(interface_start_x + self.interface_width/2, self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('+', Color.black, self.fonts[0]), 'increment_width'))
        
        self.labels.append(Label(Rect(interface_start_x, self.screen_height/3, self.interface_width, self.screen_height/3), Color.white, Color.black, None))
        self.labels.append(Label(Rect(interface_start_x, self.screen_height/3, self.interface_width, self.screen_height/6), None, None, ('Height', Color.black, self.fonts[0])))
        if self.view_model.should_display_minus_button_for_height():
            self.buttons.append(Button(Rect(interface_start_x, 3*self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('-', Color.black, self.fonts[0]), 'decrement_height'))
        self.labels.append(Label(Rect(interface_start_x, 3*self.screen_height/6, self.interface_width, self.screen_height/6), None, None, (str(self.view_model.game_height), Color.black, self.fonts[0])))
        if self.view_model.should_display_plus_button_for_height():
            self.buttons.append(Button(Rect(interface_start_x + self.interface_width/2, 3*self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('+', Color.black, self.fonts[0]), 'increment_height'))
        
        self.buttons.append(Button(Rect(interface_start_x, 2*self.screen_height/3, self.interface_width, self.screen_height/3), Color.white, Color.black, ('Start', Color.black, self.fonts[0]), 'start_game'))
        
    def generate_images(self):
        (image_grid_width, image_grid_height) = self.view_model.images_grid_dimensions
        image_view_width = self.grid_width / image_grid_width
        image_view_height = self.screen_height / image_grid_height
        for index, image in enumerate(self.view_model.get_displayed_images()):
                (image_position_x, image_position_y) = ((index % image_grid_width) * image_view_width, (index // image_grid_width) * image_view_height)
                real_index = self.view_model.get_real_index(index)
                border_color = Color.red if (self.view_model.selected_image_index == real_index) else None
                self.buttons.append(ImageButton(Rect(image_position_x, image_position_y, image_view_width, image_view_height), Color.white, border_color, None, (image.file_path, True, None, None), 'select_index_' + str(real_index)))
    
    def generate_mouse_actions(self):
        self.mouse_actions.append(MouseHandler('scroll_up', 'scroll_images_up'))
        self.mouse_actions.append(MouseHandler('scroll_down', 'scroll_images_down'))
