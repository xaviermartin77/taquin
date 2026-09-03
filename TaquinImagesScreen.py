from PygameSDK.View import *
from PygameSDK.Label import *
from PygameSDK.Buttons import *
from PygameSDK.Screen import *
from PygameSDK.MouseHandler import *

class TaquinImagesScreen(Screen):
    def __init__(self, v_m, size):
        super().__init__(v_m, size)
        self.interface_width = 400
        self.grid_width = self.size[0] - self.interface_width
        self.screen_height = self.size[1]
        
    def generate_views(self):
        super().generate_views()
        self.generate_interface()
        self.generate_images()
        self.generate_mouse_actions()
        
    def update_views(self):
        self.update_interface()
        self.update_images()
        
    def generate_interface(self):
        interface_start_x = self.grid_width
        
        width_background = View(Rect(interface_start_x, 0, self.interface_width, self.screen_height/3), Color.white, Color.black)
        width_title = Label(Rect(interface_start_x, 0, self.interface_width, self.screen_height/6), None, None, ('Width', Color.black, self.fonts[0], False))
        self.minus_button_for_width = Button(Rect(interface_start_x, self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('-', Color.black, self.fonts[0], False), 'decrement_width')
        self.width_label = Label(Rect(interface_start_x, self.screen_height/6, self.interface_width, self.screen_height/6), None, None, ('', Color.black, self.fonts[0], False))
        self.plus_button_for_width = Button(Rect(interface_start_x + self.interface_width/2, self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('+', Color.black, self.fonts[0], False), 'increment_width')
        
        height_background = View(Rect(interface_start_x, self.screen_height/3, self.interface_width, self.screen_height/3), Color.white, Color.black)
        height_title = Label(Rect(interface_start_x, self.screen_height/3, self.interface_width, self.screen_height/6), None, None, ('Height', Color.black, self.fonts[0], False))
        self.minus_button_for_height = Button(Rect(interface_start_x, 3*self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('-', Color.black, self.fonts[0], False), 'decrement_height')
        self.height_label = Label(Rect(interface_start_x, 3*self.screen_height/6, self.interface_width, self.screen_height/6), None, None, ('', Color.black, self.fonts[0], False))
        self.plus_button_for_height = Button(Rect(interface_start_x + self.interface_width/2, 3*self.screen_height/6, self.interface_width/2, self.screen_height/6), None, None, ('+', Color.black, self.fonts[0], False), 'increment_height')
        
        start_button = Button(Rect(interface_start_x, 2*self.screen_height/3, self.interface_width, self.screen_height/3), Color.white, Color.black, ('Start', Color.black, self.fonts[0], False), 'start_game')
        
        self.update_interface()
        
        self.views = self.views + [width_background, width_title, self.minus_button_for_width, self.width_label, self.plus_button_for_width, height_background, height_title, self.minus_button_for_height, self.height_label, self.plus_button_for_height, start_button]
    
    def update_interface(self):
        self.minus_button_for_width.set_visibility(self.view_model.should_display_minus_button_for_width())
        self.plus_button_for_width.set_visibility(self.view_model.should_display_plus_button_for_width())
        self.width_label.set_text(str(self.view_model.game_width))
        
        self.minus_button_for_height.set_visibility(self.view_model.should_display_minus_button_for_height())
        self.plus_button_for_height.set_visibility(self.view_model.should_display_plus_button_for_height())
        self.height_label.set_text(str(self.view_model.game_height))
        
    def generate_images(self): # creating all image views, hiding them if no image is available
        self.image_view_list = []
        for index in range(self.view_model.get_grid_size()):
            image_view = self.create_image_button(index)
            self.image_view_list.append(image_view)
        self.views = self.views + self.image_view_list
        
        self.update_images()
            
    def create_image_button(self, index):
        (image_grid_width, image_grid_height) = self.view_model.images_grid_dimensions
        image_view_width = self.grid_width / image_grid_width
        image_view_height = self.screen_height / image_grid_height
        (image_position_x, image_position_y) = ((index % image_grid_width) * image_view_width, (index // image_grid_width) * image_view_height)
        return ImageButton(Rect(image_position_x, image_position_y, image_view_width - 1, image_view_height - 1), Color.white, None, None, (None, False, None, None), 'select_index_' + str(index))
        
    def update_images(self):
        image_list = self.view_model.get_displayed_images()
        for index, image_view in enumerate(self.image_view_list):
            if index < len(image_list):
                image_view.set_visibility(True)
                image = image_list[index]
                image_view.set_image_path(image.file_path)
                if index == self.view_model.get_relative_selected_index():
                    image_view.set_border_color(Color.red)
                else:
                    image_view.set_border_color(Color.black)
            else:
                image_view.set_visibility(False)
                image_view.set_image_path(None)
        
    
    def generate_mouse_actions(self):
        self.mouse_actions.append(MouseHandler('scroll_up', 'scroll_images_up'))
        self.mouse_actions.append(MouseHandler('scroll_down', 'scroll_images_down'))
