
import os
import pygame
from taquinConstants import *

# récupérer les images, à garder en static, maybe mettre un fichier de config, maybe faire un tableau d'id plutôt que d'images
def generate_all_images(screen_size, image_list_size):
        (screen_width, screen_height) = screen_size
        (image_list_width, image_list_height) = image_list_size
        file_exist = True
        file_count = 1
        file_list = []
        while file_exist:
                file_name = 'images/image' + str(file_count) + '.jpg'
                if os.path.isfile(file_name):
                        temp_image = pygame.image.load(file_name)
                        temp_image = pygame.transform.scale(temp_image, (int(screen_width/image_list_width), int(screen_height/image_list_height)))
                        file_list.append(temp_image)
                        file_count = file_count + 1
                else:
                        file_exist = False
        return file_list

# static, tool pour connaitre la taille d'une image dans le menu principal (utile pour le click handler)
def get_small_image_size(screen_size, image_list_size):
        (screen_width, screen_height) = screen_size
        (image_list_width, image_list_height) = image_list_size
        return (int(screen_width/image_list_width), int(screen_height/image_list_height))

# static, génère les infos pour la gestion des inputs du click pendant la sélection de l'image
def generate_click_handler_data_for_main_vm(screen_size):
        (screen_width, screen_height) = screen_size
        interface_start = screen_width
        interface_center = screen_width + (INTERFACE_BIG_WIDTH / 2)
        interface_end = screen_width + INTERFACE_BIG_WIDTH
        input_data = []
        input_data.append((0, interface_start, 0, screen_height, 'select_image'))
        input_data.append((interface_start, interface_center, 0, screen_height / 3, 'decrement_width'))
        input_data.append((interface_center, interface_end, 0, screen_height / 3, 'increment_width'))
        input_data.append((interface_start, interface_center, screen_height / 3, screen_height * 2 / 3, 'decrement_height'))
        input_data.append((interface_center, interface_end, screen_height / 3, screen_height * 2 / 3, 'increment_height'))
        input_data.append((interface_start, interface_end, screen_height * 2 / 3, screen_height, 'start_game'))
        return input_data


class ImagesViewModel:
        def __init__(self, screen_size, image_list_size):
                self.image_list = generate_all_images(screen_size, image_list_size)
                self.image_list_size = image_list_size
                self.image_square_size = get_small_image_size(screen_size, image_list_size)
                self.click_handler_data = generate_click_handler_data_for_main_vm(screen_size)
                self.first_list_index = 0
                self.is_game_preparing = False
                self.game_running = False
                self.grid_width = 3
                self.grid_height = 3
                self.selected_image_index = 0

        def scroll_up(self):
                self.first_list_index = self.first_list_index - self.image_list_size[0] if self.first_list_index - self.image_list_size[0] >= 0 else 0

        def scroll_down(self):
                image_list_length = self.image_list_size[0] * self.image_list_size[1]
                self.first_list_index = self.first_list_index + self.image_list_size[0] if self.first_list_index + image_list_length < len(self.image_list) else self.first_list_index

        def select_index(self, position):
                if position + self.first_list_index < len(self.image_list):
                        self.selected_image_index = position + self.first_list_index
        
        def get_selected_image_index(self):
                return self.selected_image_index
        
        def get_selected_image_position(self):
                image_list_length = self.image_list_size[0] * self.image_list_size[1]
                if self.selected_image_index >= self.first_list_index and self.selected_image_index < self.first_list_index + image_list_length:
                        return self.selected_image_index - self.first_list_index
                return -1

        def get_image_at_position(self, position):
                if (position + self.first_list_index) >= len(self.image_list):
                        return None
                return self.image_list[position + self.first_list_index]

        def get_images_displayed_list(self):
                (image_list_width, image_list_height) = self.image_list_size
                image_list_length = image_list_width * image_list_height
                result = []
                
                for position in range(image_list_length):
                        if (position + self.first_list_index) >= len(self.image_list):
                                continue
                        result.append(self.get_image_at_position(position))
                return result

        def get_image_list_size(self):
                return self.image_list_size

        def prepare_for_start(self):
                self.is_game_preparing = True

        def start_game(self):
                # TODO : set screen size (adapt it to image shape)
                self.game_running = True
                self.is_game_preparing = False

        def quit_game(self):
                # TODO : set screen size (return to normal shape)
                self.game_running = False

        def should_start_game(self):
                return self.is_game_preparing

        def is_game_running(self):
                return self.game_running

        def decrement_grid_width(self):
                self.grid_width = self.grid_width - 1 if self.grid_width > 2 else self.grid_width

        def increment_grid_width(self):
                self.grid_width = self.grid_width + 1 if self.grid_width < 20 else self.grid_width

        def decrement_grid_height(self):
                self.grid_height = self.grid_height - 1 if self.grid_height > 2 else self.grid_height

        def increment_grid_height(self):
                self.grid_height = self.grid_height + 1 if self.grid_height < 20 else self.grid_height

        def get_grid_size(self):
                return (self.grid_width, self.grid_height)

        def get_code_for_click(self, pos):
                for handler in self.click_handler_data:
                        (x_start, x_end, y_start, y_end, code) = handler
                        if pos[0] > x_start and pos[0] < x_end and pos[1] > y_start and pos[1] < y_end:
                                return code
                return 'none'

        def handle_click(self, pos):
                handler_code = self.get_code_for_click(pos)
                if handler_code == 'select_image':
                        (image_width, image_height) = self.image_square_size
                        index_x = int(pos[0] // image_width)
                        index_y = int(pos[1] // image_height)
                        self.select_index(index_x + self.image_list_size[0] * index_y)
                elif handler_code == 'decrement_width':
                        self.decrement_grid_width()
                elif handler_code == 'increment_width':
                        self.increment_grid_width()
                elif handler_code == 'decrement_height':
                        self.decrement_grid_height()
                elif handler_code == 'increment_height':
                        self.increment_grid_height()
                elif handler_code == 'start_game':
                        self.prepare_for_start()
                
                
