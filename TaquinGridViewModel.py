from PygameSDK.ViewModel import *
from PygameSDK.Color import *
from PygameSDK.Timer import *
from TaquinGrid import *

class TaquinGridViewModel(ViewModel):
    def __init__(self, game_size):
        super().__init__()
        self.current_grid = TaquinGrid(game_size)
        self.current_move = None
        
        self.colors = ['w', 'n', 'r', 'b', 'v']
        self.background_color = Color('w')
        
        self.move_count = 0
        self.timer = Timer()
        
        self.show_hint = False
        self.show_figures = False
        self.show_time = False
        self.show_score = False
    
    # superclass methods
    def handle_code(self, code):
        if 'click_tile_index_' in code:
            tile_index = int(code.split('click_tile_index_', 1)[1])
            self.move_tile(tile_index)
        if 'move_grid_' in code:
            move_code = int(code.split('move_grid_', 1)[1])
            self.move_grid(move_code)
        if 'rotate_grid_' in code:
            rotate_code = int(code.split('rotate_grid_', 1)[1])
            self.rotate_grid(rotate_code)
        if code == 'restart_game':
            self.shuffle_grid()
        if code == 'start_hint_display':
            self.start_showing_hint()
        if code == 'start_figures_display':
            self.start_showing_figures()
        if code == 'stop_idle_actions':
            self.stop_showing_hint()
            self.stop_showing_figures()
        if code == 'toggle_time_display':
            self.toggle_show_time()
        if code == 'toggle_score_display':
            self.toggle_show_score()
        if 'select_background_color_' in code:
            color_value = code.split('select_background_color_', 1)[1]
            self.change_background_color(color_value)
        if 'solve_algo' in code:
            self.solved_with_algo()
        if 'solve_bruteforce' in code:
            self.solved_with_bruteforce()
        if code == 'end_game':
            self.return_to_list_view()
        
    def did_complete_animation(self):
        if self.current_move == None:
            return
        self.current_grid.complete_move(self.current_move[1])
        self.current_move = None
        if self.grid_solved():
            self.timer.stop_timer()
    
    # action handlers
    def move_tile(self, tile_index):
        move_pair = self.current_grid.get_tile_move_info(tile_index)
        if move_pair != None:
            self.move_count += 1
            self.timer.start_timer()
            self.current_move = move_pair
    
    def move_grid(self, move_code):
        move_pair = self.current_grid.get_direction_move_info(move_code)
        if move_pair != None:
            self.move_count += 1
            self.timer.start_timer()
            self.current_move = move_pair
    
    def rotate_grid(self, rotate_code):
        rotate_chrono = (rotate_code == 0)
        move_pair = self.current_grid.get_rotation_move_info(rotate_chrono)
        if move_pair != None:
            self.move_count += 1
            self.timer.start_timer()
            self.current_move = move_pair
    
    def shuffle_grid(self):
        self.current_grid.shuffle()
        self.move_count = 0
        self.timer.reset_timer()
    
    def start_showing_hint(self):
        if not self.show_hint:
            self.show_hint = True
    
    def stop_showing_hint(self):
        if self.show_hint:
            self.show_hint = False
    
    def start_showing_figures(self):
        if not self.show_figures:
            self.show_figures = True
    
    def stop_showing_figures(self):
        if self.show_figures:
            self.show_figures = False
    
    def toggle_show_time(self):
        self.show_time = not self.show_time
    
    def toggle_show_score(self):
        self.show_score = not self.show_score
    
    def change_background_color(self, code):
        if code != self.background_color.color_code:
            self.background_color = Color(code)
    
    def return_to_list_view(self):
        self.should_return = True
    
    def solved_with_algo(self):
        print('not ready yet')
    
    def solved_with_bruteforce(self):
        print('not ready yet')

    # data providers for UI
    def get_tile_dimension(self, screen_size):
        return (screen_size[0] / self.current_grid.grid_size[0], screen_size[1] / self.current_grid.grid_size[1])
    
    def grid_solved(self):
        return self.current_grid.solved()
        
    def get_current_time(self):
        return self.timer.get_seconds() # no auto update, needs improvement
    
    def first_button_text(self):
        return 'Menu' if self.grid_solved() else 'Hint'
        
    def first_button_handler(self):
        return 'end_game' if self.grid_solved() else 'start_hint_display'
        
    def second_button_text(self):
        return 'Restart' if self.grid_solved() else 'Figures'
        
    def second_button_handler(self):
        return 'restart_game' if self.grid_solved() else 'start_figures_display'
        
    def time_button_text(self):
        return str(self.get_current_time()) if self.show_time else 'Time'
        
    def score_button_text(self):
        return str(self.move_count) if self.show_score else 'Score'
        
    def get_tiles_zones_coordinates(self):
        return self.current_grid.get_sorted_tiles_coordinates()
        
    def get_tiles_positions_coordinates(self):
        return self.current_grid.get_tiles_coordinates_in_grid()
        
    def get_displayed_text(self, index):
        return str(index + 1) if self.show_figures else None
        
    def get_movement(self, index):
        if self.current_move != None:
            (moving_index, move_code) = self.current_move
            if moving_index == index:
                if move_code == 0:
                    return (0, -1)
                if move_code == 1:
                    return (0, 1)
                if move_code == 2:
                    return (-1, 0)
                if move_code == 3:
                    return (1, 0)
        return None
                
