from TaquinGridViewModel import *
from PygameSDK.View import *
from PygameSDK.Buttons import *
from PygameSDK.ImageView import *
from PygameSDK.Screen import *
from PygameSDK.MouseHandler import *
from PygameSDK.KeyboardHandler import *

class TaquinGridScreen(Screen):
    def __init__(self, v_m, size, img):
        super().__init__(v_m, size, [('arial', 50), ('arial', 20)])
        self.interface_width = 100
        self.image_view_width = self.size[0] - self.interface_width
        self.screen_height = self.size[1]
        self.image = img
    
    def unload_ressources(self):
        self.image.unload_image_ressource()
        
    def generate_views(self):
        super().generate_views()
        self.generate_interface()
        self.generate_images()
        self.generate_mouse_actions()
        self.generate_shortcuts()
        
    def update_views(self):
        self.update_interface()
        self.update_images()
        
    def generate_interface(self):
        interface_start_x = self.image_view_width
        
        self.first_button = Button(Rect(interface_start_x, 0, self.interface_width, self.screen_height/5), Color.white, Color.black, ('', Color.black, self.fonts[1], False), '')
        self.second_button = Button(Rect(interface_start_x, self.screen_height/5, self.interface_width, self.screen_height/5), Color.white, Color.black, ('', Color.black, self.fonts[1], False), '')
        
        self.time_button = Button(Rect(interface_start_x, 2*self.screen_height/5, self.interface_width, self.screen_height/5), Color.white, Color.black, ('', Color.black, self.fonts[1], False), 'toggle_time_display')
        self.score_button = Button(Rect(interface_start_x, 3*self.screen_height/5, self.interface_width, self.screen_height/5 - 1), Color.white, Color.black, ('', Color.black, self.fonts[1], False), 'toggle_score_display')
        
        color_buttons = []
        for index, color_code in enumerate(self.view_model.colors):
            color_button = Button(Rect(interface_start_x, 4*self.screen_height/5 + index * self.screen_height/25, self.interface_width, self.screen_height/25), Color(color_code).get_color_value(), None, None, 'select_background_color_' + color_code)
            color_buttons.append(color_button)
            
        interface_border = View(Rect(interface_start_x, 4*self.screen_height/5, self.interface_width, self.screen_height - 1), None, Color.black)
        
        self.update_interface()
        
        self.views = self.views + [self.first_button, self.second_button, self.time_button, self.score_button] + color_buttons + [interface_border]
        
    def update_interface(self):
        self.first_button.set_text(self.view_model.first_button_text())
        self.first_button.set_handler(self.view_model.first_button_handler())
        
        self.second_button.set_text(self.view_model.second_button_text())
        self.second_button.set_handler(self.view_model.second_button_handler())
        
        self.time_button.set_text(self.view_model.time_button_text())
        self.score_button.set_text(self.view_model.score_button_text())
        
    def generate_images(self):
        self.images_background = View(Rect(0, 0, self.image_view_width, self.screen_height), Color.white, None)
        
        self.hint_image = ImageView(Rect(0, 0, self.image_view_width, self.screen_height), None, None, None, (None, None, self.image.image_ressource, None))
        
        (self.image_tile_width, self.image_tile_height) = self.view_model.get_tile_dimension((self.image_view_width, self.screen_height))
        
        self.image_view_list = []
        for index, coordinates in enumerate(self.view_model.get_tiles_zones_coordinates()):
            tile_image_zone = (self.image_tile_width * coordinates[0], self.image_tile_height * coordinates[1], self.image_tile_width, self.image_tile_height)
            image_view = ImageButton(Rect(0, 0, self.image_tile_width, self.image_tile_height), None, None, ('', Color.red, self.fonts[0], False), (None, None, self.image.image_ressource, tile_image_zone), 'click_tile_index_' + str(index))
            self.image_view_list.append(image_view)
        self.views = self.views + [self.images_background, self.hint_image] + self.image_view_list
        
        self.update_images()
                
    def update_images(self):
        self.images_background.set_bkg_color(self.view_model.background_color.get_color_value())
        
        hide_grid = self.view_model.show_hint or self.view_model.grid_solved()
        self.hint_image.set_visibility(hide_grid)
        
        coordinates_list = self.view_model.get_tiles_positions_coordinates()
        for index, image_view in enumerate(self.image_view_list):
            coordinates = coordinates_list[index]
            movement = self.view_model.get_movement(index)
            tile_position_x = (coordinates[0] + movement[0]) * self.image_tile_width
            tile_position_y = (coordinates[1] + movement[1]) * self.image_tile_height
            if movement != (0,0):
                start_x = (coordinates[0] - 1) * self.image_tile_width if movement[0] < 0 else coordinates[0]
                start_y = (coordinates[1] - 1) * self.image_tile_height if movement[1] < 0 else coordinates[1]
                width = self.image_tile_width if movement[0] == 0 else 2 * self.image_tile_width
                height = self.image_tile_height if movement[1] == 0 else 2 * self.image_tile_height
                self.animation_zone = Rect(start_x, start_y, width, height)
            image_view.set_coordinates(Rect(tile_position_x, tile_position_y, self.image_tile_width, self.image_tile_height))
            image_view.set_text(self.view_model.get_displayed_text(index))
            image_view.set_visibility(not hide_grid)
    
    def generate_mouse_actions(self):
        self.mouse_actions.append(MouseHandler('mouse_button_released', 'stop_idle_actions'))
    
    def generate_shortcuts(self):
        self.shortcuts.append(KeyboardHandler('up', 'move_grid_0'))
        self.shortcuts.append(KeyboardHandler('down', 'move_grid_1'))
        self.shortcuts.append(KeyboardHandler('left', 'move_grid_2'))
        self.shortcuts.append(KeyboardHandler('right', 'move_grid_3'))
        
        self.shortcuts.append(KeyboardHandler('r', 'rotate_grid_0'))
        self.shortcuts.append(KeyboardHandler('t', 'rotate_grid_1'))
        
        self.shortcuts.append(KeyboardHandler('s', 'solve_algo'))
        self.shortcuts.append(KeyboardHandler('b', 'solve_bruteforce'))
