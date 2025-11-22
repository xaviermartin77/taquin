import pygame
from taquinUtils import *
from taquinConstants import *
from taquinSolver import *


#static, génère les infos pour la gestion des inputs du click pendant le jeu
def generate_click_handler_data_for_game_vm(screen_size):
        (screen_width, screen_height) = screen_size
        interface_start = screen_width
        interface_end = screen_width + INTERFACE_WIDTH
        input_data = []
        input_data.append((0, interface_start, 0, screen_height, 'select_tile'))
        input_data.append((interface_start, interface_end, 0, screen_height / 5, 'first_button'))
        input_data.append((interface_start, interface_end, screen_height / 5, screen_height * 2 / 5, 'second_button'))
        input_data.append((interface_start, interface_end, screen_height * 2 / 5, screen_height * 3 / 5, 'show_score'))
        input_data.append((interface_start, interface_end, screen_height * 3 / 5, screen_height * 4 / 5, 'show_time'))
        input_data.append((interface_start, interface_end, screen_height * 4 / 5, screen_height * 21 / 25, 'background_white'))
        input_data.append((interface_start, interface_end, screen_height * 21 / 25, screen_height * 22 / 25, 'background_black'))
        input_data.append((interface_start, interface_end, screen_height * 22 / 25, screen_height * 23 / 25, 'background_red'))
        input_data.append((interface_start, interface_end, screen_height * 23 / 25, screen_height * 24 / 25, 'background_blue'))
        input_data.append((interface_start, interface_end, screen_height * 24 / 25, screen_height, 'background_green'))
        return input_data

#static, génère les infos pour la gestion des inputs du clavier pendant le jeu
def generate_shortcut_handler_data_for_game_vm():
        input_data = []
        input_data.append((pygame.K_r, 'rotate_chrono'))
        input_data.append((pygame.K_t, 'rotate_trigo'))
        input_data.append((pygame.K_LEFT, 'move_left'))
        input_data.append((pygame.K_RIGHT, 'move_right'))
        input_data.append((pygame.K_DOWN, 'move_down'))
        input_data.append((pygame.K_UP, 'move_up'))
        input_data.append((pygame.K_s, 'solve_algo'))
        input_data.append((pygame.K_b, 'solve_brute'))
        input_data.append((pygame.K_BACKSPACE, 'quit'))
        return input_data

# static, récupère l'image à partir de son index
def generate_full_screen_image(image_index, grid_size):
        image = pygame.image.load('images/image' + str(image_index+1) + '.jpg')
        image = pygame.transform.scale(image, get_full_screen_image_size(image.get_width(), image.get_height(), grid_size))
        return image

# static, calcule la taille de l'image par rapport à l'écran
def get_full_screen_image_size(imageWidth, imageHeight, grid_size):
        (grid_width, grid_height) = grid_size
        screen_width = min(MAX_WIDTH - INTERFACE_WIDTH, imageWidth)
        screen_height = screen_width * imageHeight / imageWidth
        if screen_height > MAX_HEIGHT:
                screen_height = min(MAX_HEIGHT, imageHeight)
                screen_width = screen_height * imageWidth / imageHeight
        adjusted_screen_width = int(screen_width) - int(screen_width)%grid_width
        adjusted_screen_height = int(screen_height) - int(screen_height)%grid_height
        return int(adjusted_screen_width), int(adjusted_screen_height)

class GameViewModel:
        def __init__(self, image_index, grid_size):
                selected_image = generate_full_screen_image(image_index, grid_size)
                self.full_screen_image = selected_image
                self.grid_size = grid_size
                self.firstListIndex = 0
                self.tile_size = (selected_image.get_width()/grid_size[0], selected_image.get_height()/grid_size[1])
                self.click_handler_data = generate_click_handler_data_for_game_vm((selected_image.get_width(), selected_image.get_height()))
                self.shortcut_handler_data = generate_shortcut_handler_data_for_game_vm()
                self.is_game_leaving = False
                
                self.background_color = white
                
                self.start_ticks = 0
                self.final_time = 0
                self.seconds = 0
                self.move_count = 0
                
                self.is_showing_hint = False
                self.is_showing_figures = False
                self.is_showing_score = True
                self.is_showing_time = True

                self.current_array = get_random_array(grid_size) #[1, 4, 2, 3, 5, 0]
                self.current_movement = (0, 0, 0) # progress, tile, target
                self.solver = Solver(grid_size)

        def get_game_screen_size(self):
                return (self.full_screen_image.get_width() + INTERFACE_WIDTH, self.full_screen_image.get_height())

        def get_game_screen_square(self):
                return (0, 0, self.full_screen_image.get_width(), self.full_screen_image.get_height())

        def get_full_screen_image(self):
                return self.full_screen_image

        def shuffle(self):
                self.start_ticks = 0
                self.final_time = 0
                self.seconds = 0
                self.move_count = 0        
                self.current_array = get_random_array(self.grid_size)
                self.current_movement = (0, 0, 0)

        def start_showing_hint(self):
                self.is_showing_hint = True

        def stop_showing_hint(self):
                self.is_showing_hint = False

        def should_show_hint(self):
                return self.is_showing_hint

        def start_showing_figures(self):
                self.is_showing_figures = True

        def stop_showing_figures(self):
                self.is_showing_figures = False

        def should_show_figures(self):
                return self.is_showing_figures

        def switch_showing_score(self):
                self.is_showing_score = not self.is_showing_score

        def should_show_score(self):
                return self.is_showing_score

        def switch_showing_time(self):
                self.is_showing_time = not self.is_showing_time

        def should_show_time(self):
                return self.is_showing_time

        def select_background_color(self, color):
                self.background_color = color

        def get_background_color(self):
                return self.background_color

        def increment_move_count(self):
                self.move_count = self.move_count + 1

        def get_move_count(self):
                return self.move_count

        def check_if_grid_is_solved(self):
                if self.is_game_solved() and self.final_time == 0 and self.start_ticks>0:
                        self.final_time = pygame.time.get_ticks() - self.start_ticks

        def get_time_to_display(self):
                return (self.final_time if self.is_game_solved() else (pygame.time.get_ticks() - self.start_ticks if self.start_ticks > 0 else 0)) // 1000

        def is_game_solved(self):
                return all(self.current_array[i] <= self.current_array[i+1] for i in range(len(self.current_array)-1))

        def is_tile_moving(self):
                return self.current_movement[0] != 0

        def is_white_tile(self, tile_index):
                return self.current_array[tile_index] == len(self.current_array) - 1

        def get_white_tile_index(self):
                for index in range(len(self.current_array)):
                        if self.is_white_tile(index):
                                return index
                return -1
        
        def move_with_direction_if_possible(self, direction):
                white_tile_index = self.get_white_tile_index()
                (white_tile_x, white_tile_y) = self.get_coordinates_from_index(white_tile_index)
                (grid_width, grid_height) = self.grid_size
                
                if white_tile_x < grid_width - 1 and direction == 0:
                        # move left
                        self.start_moving(white_tile_index + 1, white_tile_index)
                if white_tile_x > 0 and direction == 1:
                        # move right
                        self.start_moving(white_tile_index - 1, white_tile_index)
                if white_tile_y > 0 and direction == 2:
                        # move down
                        self.start_moving(white_tile_index - grid_width, white_tile_index)
                if white_tile_y < grid_height - 1 and direction == 3:
                        # move up
                        return self.start_moving(white_tile_index + grid_width, white_tile_index)

        def rotate_if_possible(self, rotate_chrono, start_index = 0, end_index = -1):
                if end_index == -1:
                        end_index = len(self.current_array) - 1
                white_tile_index = self.get_white_tile_index()
                (white_tile_x, white_tile_y) = self.get_coordinates_from_index(white_tile_index)
                (start_tile_x, start_tile_y) = self.get_coordinates_from_index(start_index)
                (end_tile_x, end_tile_y) = self.get_coordinates_from_index(end_index)
                
                if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == start_tile_y:
                        if rotate_chrono and white_tile_x != start_tile_x:
                                self.move_with_direction_if_possible(1)
                        if (not rotate_chrono) and white_tile_x != end_tile_x:
                                self.move_with_direction_if_possible(0)
                if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == end_tile_y:
                        if rotate_chrono and white_tile_x != end_tile_x:
                                self.move_with_direction_if_possible(0)
                        if (not rotate_chrono) and white_tile_x != start_tile_x:
                                self.move_with_direction_if_possible(1)
                if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == start_tile_x:
                        if rotate_chrono and white_tile_y != end_tile_y:
                                self.move_with_direction_if_possible(3)
                        if (not rotate_chrono) and white_tile_y != start_tile_y:
                                self.move_with_direction_if_possible(2)
                if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == end_tile_x:
                        if rotate_chrono and white_tile_y != start_tile_y:
                                self.move_with_direction_if_possible(2)
                        if (not rotate_chrono) and white_tile_y != end_tile_y:
                                self.move_with_direction_if_possible(3)

        def move_tile_if_possible(self, position):
                tile_index = self.get_tile_index_from_position(position)
                if tile_index != -1:
                        target_tile_index = self.get_target_index_from_tile(tile_index)
                        if target_tile_index != -1:
                                self.start_moving(tile_index, target_tile_index)
                        

        def get_tile_index_from_position(self, position):
                (x, y) = position
                (tile_width, tile_height) = self.tile_size
                (grid_width, grid_height) = self.grid_size
                for i in range(grid_width):
                        for j in range(grid_height):
                                if x >= tile_width*i and x < tile_width*(i+1) and y >= tile_height*j and y < tile_height*(j+1):
                                        return j*grid_width + i
                return -1
                        

        def get_coordinates_from_index(self, index):
                grid_width = self.grid_size[0]
                return index % grid_width, index // grid_width

        def get_target_index_from_tile(self, tile_index):
                (grid_width, grid_height) = self.grid_size
                if self.is_white_tile(tile_index):
                        return -1
                (i, j) = self.get_coordinates_from_index(tile_index)
                if i > 0 and self.is_white_tile(tile_index - 1):
                        return tile_index - 1
                if i < grid_width - 1 and self.is_white_tile(tile_index + 1):
                        return tile_index + 1
                if j > 0 and self.is_white_tile(tile_index - grid_width):
                        return tile_index - grid_width
                if j < grid_height - 1 and self.is_white_tile(tile_index + grid_width):
                        return tile_index + grid_width
                return -1

        def get_current_move_step_size(self):
                if not self.is_tile_moving():
                        return 0
                (progress, tile_index, target_tile_index) = self.current_movement
                grid_width = self.grid_size[0]
                (tile_width, tile_height) = self.tile_size
                if tile_index == target_tile_index - 1:
                        return tile_width/10
                if tile_index == target_tile_index + 1:
                        return -tile_width/10
                if tile_index == target_tile_index - grid_width:
                        return tile_height/10
                if tile_index == target_tile_index + grid_width:
                        return -tile_height/10

        def get_current_move_state_for_tile(self, tile_index_to_check):
                if not self.is_tile_moving() :
                        return (0, 0)
                (progress, tile_index, target_tile_index) = self.current_movement
                if tile_index != tile_index_to_check:
                        return (0, 0)
                grid_width = self.grid_size[0]
                if tile_index == target_tile_index - 1 or tile_index == target_tile_index + 1:
                        return (progress, 0)
                if tile_index == target_tile_index - grid_width or tile_index == target_tile_index + grid_width:
                        return (0, progress)
                return (0, 0)

        def start_moving(self, tile_index, target_tile_index):
                if self.is_game_solved():
                        return
                if self.start_ticks == 0:
                        self.start_ticks = pygame.time.get_ticks()
                self.move_count = self.move_count + 1
                first_progress = 1 if tile_index < target_tile_index else -1
                self.current_movement = (first_progress, tile_index, target_tile_index)

        def increment_progress_if_needed(self):
                if not self.is_tile_moving():
                        return
                (progress, tile_index, target_tile_index) = self.current_movement
                new_progress = progress + self.get_current_move_step_size()
                (tile_width, tile_height) = self.tile_size
                grid_width = self.grid_size[0]
                movement_completed = \
                        (tile_index == target_tile_index - 1 and new_progress >= tile_width) \
                        or (tile_index == target_tile_index + 1 and new_progress <= -tile_width) \
                        or (tile_index == target_tile_index - grid_width and new_progress >= tile_height) \
                        or (tile_index == target_tile_index + grid_width and new_progress <= -tile_height)
                if movement_completed:
                        self.grid_size
                        self.current_array[target_tile_index] = self.current_array[tile_index]
                        self.current_array[tile_index] = len(self.current_array) - 1
                        self.current_movement = (0, 0, 0)
                else:
                        self.current_movement = (new_progress, tile_index, target_tile_index)

        def get_tile_info_grid(self):
                (tile_width, tile_height) = self.tile_size
                result = []
                for index, tile_value in enumerate(self.current_array):
                        if self.is_white_tile(index) and not self.is_game_solved():
                                continue
                        
                        (x_position_on_screen, y_position_on_screen) = self.get_coordinates_from_index(index)
                        (x_move_value, y_move_value) = self.get_current_move_state_for_tile(index)
                        tile_coordinates = (x_position_on_screen * tile_width + x_move_value, y_position_on_screen * tile_height + y_move_value)
                        
                        (x_position_on_image, y_position_on_image) = self.get_coordinates_from_index(tile_value)
                        tile_size_square_to_display = (x_position_on_image * tile_width, y_position_on_image * tile_height, tile_width, tile_height)
                        
                        text = (str(tile_value + 1)) if self.is_showing_figures else ''
                        text_center_coordinates = (x_position_on_screen * tile_width + x_move_value + tile_width/2, y_position_on_screen * tile_height + y_move_value + tile_height/2)

                        result.append((tile_coordinates, tile_size_square_to_display, text, text_center_coordinates))
                return result

        def get_code_for_click(self, pos):
                for handler in self.click_handler_data:
                        (x_start, x_end, y_start, y_end, code) = handler
                        if pos[0] > x_start and pos[0] < x_end and pos[1] > y_start and pos[1] < y_end:
                                return code
                return 'none'

        def handle_click(self, pos):
                handler_code = self.get_code_for_click(pos)
                if handler_code == 'select_tile':
                        self.move_tile_if_possible(pos)
                if handler_code == 'first_button':
                        if self.is_game_solved():
                                self.prepare_for_leaving()
                        else:
                                self.start_showing_hint()
                elif handler_code == 'second_button':
                        if self.is_game_solved():
                                self.shuffle()
                        else:
                                self.start_showing_figures()
                elif handler_code == 'show_score':
                        self.switch_showing_score()
                elif handler_code == 'show_time':
                        self.switch_showing_time()
                elif handler_code == 'background_white':
                        self.select_background_color(white)
                elif handler_code == 'background_black':
                        self.select_background_color(black)
                elif handler_code == 'background_red':
                        self.select_background_color(red)
                elif handler_code == 'background_blue':
                        self.select_background_color(blue)
                elif handler_code == 'background_green':
                        self.select_background_color(green)
        
        def prepare_for_leaving(self):
                self.is_game_leaving = True

        def should_leave_game(self):
                # TODO : dealloc / deactivate params if needed
                return self.is_game_leaving

        def get_code_for_key(self, key):
                for handler in self.shortcut_handler_data:
                        (key_id, code) = handler
                        if key == key_id:
                                return code
                return 'none'

        def handle_shortcut(self, key):
                handler_code = self.get_code_for_key(key)
                if handler_code == 'rotate_chrono':
                        self.rotate_if_possible(True)
                elif handler_code == 'rotate_trigo':
                        self.rotate_if_possible(False)
                elif handler_code == 'move_left':
                        self.move_with_direction_if_possible(0)
                elif handler_code == 'move_right':
                        self.move_with_direction_if_possible(1)
                elif handler_code == 'move_down':
                        self.move_with_direction_if_possible(2)
                elif handler_code == 'move_up':
                        self.move_with_direction_if_possible(3)
                elif handler_code == 'solve_algo':
                        self.solve_algo()
                elif handler_code == 'solve_brute':
                        self.solve_brute_force()
                elif handler_code == 'quit':
                        self.prepare_for_leaving()

        def solve_brute_force(self):
                next_move = self.solver.get_next_move_brute_force(self.current_array)
                if next_move != -1:
                        self.move_with_direction_if_possible(next_move)

        def solve_algo(self):
                (next_move, rotation) = self.solver.get_next_move_algo(self.current_array)
                if next_move != -1:
                        self.move_with_direction_if_possible(next_move)
                if rotation != None:
                        (rotate_chrono, start_index, end_index) = rotation
                        self.rotate_if_possible(rotate_chrono, start_index, end_index)

