from TaquinGridViewModel import *
from PygameSDK.Label import *
from PygameSDK.Button import *
from PygameSDK.ImageView import *
from PygameSDK.View import *
from PygameSDK.MouseHandler import *

class TaquinGridView(View):
    def __init__(self, v_m, size, img):
        super().__init__(v_m, size, [('arial', 50), ('arial', 20)])
        self.interface_width = 100
        self.image_view_width = self.size[0] - self.interface_width
        self.screen_height = self.size[1]
        self.image = img
        
    def generate_elements(self):
        super().generate_elements()
        self.generate_interface()
        self.generate_images()
        self.generate_mouse_actions()
        
    def generate_interface(self):
        interface_start_x = self.image_view_width
        
        self.buttons.append(Button(Rect(interface_start_x, 0, self.interface_width, self.screen_height/5), Color.white, Color.black, (self.view_model.first_button_text(), Color.black, self.fonts[1]), self.view_model.first_button_handler()))
        self.buttons.append(Button(Rect(interface_start_x, self.screen_height/5, self.interface_width, self.screen_height/5), Color.white, Color.black, (self.view_model.second_button_text(), Color.black, self.fonts[1]), self.view_model.second_button_handler()))
        
        self.buttons.append(Button(Rect(interface_start_x, 2*self.screen_height/5, self.interface_width, self.screen_height/5), Color.white, Color.black, (self.view_model.time_button_text(), Color.black, self.fonts[1]), 'toggle_time_display'))
        self.buttons.append(Button(Rect(interface_start_x, 3*self.screen_height/5, self.interface_width, self.screen_height/5), Color.white, Color.black, (self.view_model.score_button_text(), Color.black, self.fonts[1]), 'toggle_score_display'))
        
        for index, color_code in enumerate(self.view_model.colors):
            self.buttons.append(Button(Rect(interface_start_x, 4*self.screen_height/5 + index * self.screen_height/25, self.interface_width, self.screen_height/25), Color(color_code).get_color_value(), None, None, 'select_background_color_' + color_code))
        self.labels.append(Label(Rect(interface_start_x, 4*self.screen_height/5, self.interface_width, self.screen_height - 1), None, Color.black, None, None))
        
    def generate_images(self):
        if self.view_model.show_hint or self.view_model.grid_solved():
            self.labels.append(ImageView(Rect(0, 0, self.image_view_width, self.screen_height), None, None, None, (None, None, self.image.image_ressource, None)))
        else:
            self.labels.append(Label(Rect(0, 0, self.image_view_width, self.screen_height), self.view_model.background_color.get_color_value(), None, None, None))
            (game_width, game_height) = self.view_model.game_dimensions
            image_tile_width = self.image_view_width / game_width
            image_tile_height = self.screen_height / game_height
            for tile_infos in self.view_model.get_all_tiles_infos():
                (tile_position_x, tile_position_y) = (tile_infos[1][0] * image_tile_width, tile_infos[1][1] * image_tile_height)
                tile_image_zone = (tile_infos[2][0] * image_tile_width, tile_infos[2][1] * image_tile_height, image_tile_width, image_tile_height)
                text_info = (tile_infos[3], Color.red, self.fonts[0]) if tile_infos[3] != None else None
                self.buttons.append(ImageButton(Rect(tile_position_x, tile_position_y, image_tile_width, image_tile_height), None, None, text_info, (None, None, self.image.image_ressource, tile_image_zone), 'click_tile_index_' + str(tile_infos[0])))
    
    def generate_mouse_actions(self):
        self.mouse_actions.append(MouseHandler('mouse_button_released', 'stop_idle_actions'))
    
    def generate_shortcuts(self):
        print('TBD')
        # to add : direction move, rotate move, solve
