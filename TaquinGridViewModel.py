from PygameSDK.ViewModel import *
from PygameSDK.Color import *
from TaquinGrid import *

class TaquinGridViewModel(ViewModel):
    def __init__(self, game_size):
        super().__init__()
        self.game_dimensions = game_size
        self.current_grid = TaquinGrid(game_size)
        
        self.colors = ['w', 'n', 'r', 'b', 'v']
        self.background_color = Color('w')
        self.animation_frame_count = 30
        
        self.move_count = 0
        
        self.show_hint = False
        self.show_figures = False
        self.show_time = False
        self.show_score = False
        
    def update_animation(self):
        (index, move_code, animation_progress) = self.current_animation
        if animation_progress < self.animation_frame_count:
            self.current_animation = (index, move_code, animation_progress + 1)
        else:
           self.current_animation = None
           self.current_grid.complete_move(move_code)
        self.should_update = True
    
    # superclass methods
    def handle_code(self, code):
        if 'click_tile_index_' in code:
            tile_index = int(code.split('click_tile_index_', 1)[1])
            self.move_tile(tile_index)
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
        if code == 'end_game':
            self.return_to_list_view()
    
    # action handlers
    def move_tile(self, tile_index):
        possible_move = self.current_grid.get_tile_move(tile_index)
        if possible_move != None:
            self.move_count += 1
            self.current_animation = possible_move
            self.should_update = True
    
    def shuffle_grid(self):
        self.current_grid.shuffle()
        self.move_count = 0
        self.should_update = True
    
    def start_showing_hint(self):
        if not self.show_hint:
            self.show_hint = True
            self.should_update = True
    
    def stop_showing_hint(self):
        if self.show_hint:
            self.show_hint = False
            self.should_update = True
    
    def start_showing_figures(self):
        if not self.show_figures:
            self.show_figures = True
            self.should_update = True
    
    def stop_showing_figures(self):
        if self.show_figures:
            self.show_figures = False
            self.should_update = True
    
    def toggle_show_time(self):
        self.show_time = not self.show_time
        self.should_update = True
    
    def toggle_show_score(self):
        self.show_score = not self.show_score
        self.should_update = True
    
    def change_background_color(self, code):
        if code != self.background_color.color_code:
            self.background_color = Color(code)
            self.should_update = True
    
    def return_to_list_view(self):
        print('return to previous view')
        print('needs to be set in SDK (weak ref')

    # data providers for UI
    def grid_solved(self):
        return self.current_grid.solved()
        
    def get_current_time(self):
        return 0 # use pygame.time.get_ticks() with start_time when first move starts and final_time when grid is solved
    
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
    
    def get_all_tiles_infos(self):
        grid_tile_infos = self.current_grid.get_tiles_infos()
        result = []
        for tile_info in grid_tile_infos:
            (index, element, index_coord, element_coord) = tile_info
            value_text = str(element + 1) if self.show_figures else None
            move_info = None
            if self.current_animation != None:
                (moving_index, move_code, animation_progress) = self.current_animation
                if moving_index == index:
                    if move_code == 0:
                        move_info = (0, -1 * animation_progress/self.animation_frame_count)
                    if move_code == 1:
                        move_info = (0, animation_progress/self.animation_frame_count)
                    if move_code == 2:
                        move_info = (-1 *animation_progress/self.animation_frame_count, 0)
                    if move_code == 3:
                        move_info = (animation_progress/self.animation_frame_count, 0)
            result.append((index, (index_coord, move_info), element_coord, value_text))
        return result
                
