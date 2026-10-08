import random

class TaquinGrid:
    def __init__(self, size, array = None):
        self.grid_size = size
        self.current_array = array
        if self.current_array == None:
            self.shuffle()
    
    def get_coordinates(self, index):
        return (index % self.grid_size[0], index // self.grid_size[0])
    
    def get_tile_coordinates(self, value):
        return self.get_coordinates(self.current_array.index(value))
        
    def get_grid_length(self):
        return self.grid_size[0] * self.grid_size[1]
        
    def get_blank_tile_value(self):
        return self.grid_size[0] * self.grid_size[1] - 1
        
    def get_blank_tile_index(self):
        return self.current_array.index(self.get_blank_tile_value())
        
    def get_blank_tile_coordinates(self):
        return self.get_coordinates(self.get_blank_tile_index())
        
    def get_sorted_tiles_coordinates(self):
        return list(map(self.get_coordinates, list(range(self.get_grid_length() - 1))))
        
    def get_tiles_coordinates_in_grid(self):
        return list(map(lambda value: self.get_coordinates(self.current_array.index(value)), list(range(self.get_grid_length() - 1))))
    
    def shuffle(self):
        self.current_array = list(range(self.get_grid_length()))
        random.shuffle(self.current_array)
        while not self.is_solvable():
            random.shuffle(self.current_array)
    
    def is_solvable(self):
        (grid_width, grid_height) = self.grid_size
        grid_length = self.get_grid_length()
        
        # calculating the number of moves needed to put the blank tile on the right spot
        (x_blank, y_blank) = self.get_blank_tile_coordinates()
        count = grid_width + grid_height - x_blank - y_blank
        
        # adding the number of switch needed to solve the grid
        test_array = self.current_array.copy()
        for i in range(grid_length):
            if test_array[i] != i:
                for j in range(i, grid_length):
                    if test_array[j] == i:
                        test_array[i], test_array[j] = test_array[j], test_array[i]
                        count += 1
        
        # grid is solvable only if this sum is odd
        return (count%2 == 0)
        
    def solved(self):
        for index, value in enumerate(self.current_array):
            if value != index:
                return False
        return True
        
    def get_tile_move_info(self, value):
        (blank_tile_x, blank_tile_y) = self.get_blank_tile_coordinates()
        (tile_x, tile_y) = self.get_tile_coordinates(value)
        if blank_tile_x == tile_x:
            if blank_tile_y == tile_y - 1:
                return (value, 0) # up
            if blank_tile_y == tile_y + 1:
                return (value, 1) # down
        if blank_tile_y == tile_y:
            if blank_tile_x == tile_x - 1:
                return (value, 2) # left
            if blank_tile_x == tile_x + 1:
                return (value, 3) # right
        return None
    
    def get_direction_move_info(self, move_code):
        (grid_width, grid_height) = self.grid_size
        (blank_tile_x, blank_tile_y) = self.get_blank_tile_coordinates()
        blank_tile_index = self.get_blank_tile_index()
        if move_code == 0 and blank_tile_y != grid_height - 1: # up
            return (self.current_array[blank_tile_index + grid_width], 0)
        if move_code == 1 and blank_tile_y != 0: # down
            return (self.current_array[blank_tile_index - grid_width], 1)
        if move_code == 2 and blank_tile_x != grid_width - 1: # left
            return (self.current_array[blank_tile_index + 1], 2)
        if move_code == 3 and blank_tile_x != 0: # right
            return (self.current_array[blank_tile_index - 1], 3)
        return None
    
    def get_rotation_move_info(self, rotate_chrono, limits = None):
        (start_index, end_index) = limits if limits != None else (0, self.get_grid_length() - 1)
        (start_x, start_y) = self.get_coordinates(start_index)
        (end_x, end_y) = self.get_coordinates(end_index)
        (blank_tile_x, blank_tile_y) = self.get_blank_tile_coordinates()
        
        move_up = self.get_direction_move_info(0)
        move_down = self.get_direction_move_info(1)
        move_left = self.get_direction_move_info(2)
        move_right = self.get_direction_move_info(3)
        
        if blank_tile_x == start_x and blank_tile_y >= start_y and blank_tile_y <= end_y:
            if rotate_chrono and blank_tile_y != end_y:
                return move_up
            if not rotate_chrono and blank_tile_y != start_y:
                return move_down
        if blank_tile_x == end_x and blank_tile_y >= start_y and blank_tile_y <= end_y:
            if rotate_chrono and blank_tile_y != start_y:
                return move_down
            if not rotate_chrono and blank_tile_y != end_y:
                return move_up
        if blank_tile_y == start_y and blank_tile_x >= start_x and blank_tile_x <= end_x:
            if rotate_chrono and blank_tile_x != start_x:
                return move_right
            if not rotate_chrono and blank_tile_x != end_x:
                return move_left
        if blank_tile_y == end_y and blank_tile_x >= start_x and blank_tile_x <= end_x:
            if rotate_chrono and blank_tile_x != end_x:
                return move_left
            if not rotate_chrono and blank_tile_x != start_x:
                return move_right
        return None
    
    def complete_move(self, move_code):
        blank_index = self.get_blank_tile_index()
        grid_width = self.grid_size[0]
        if move_code == 0 and (blank_index + grid_width) < len(self.current_array):
            self.current_array[blank_index], self.current_array[blank_index + grid_width] = self.current_array[blank_index + grid_width], self.current_array[blank_index]
        if move_code == 1 and (blank_index - grid_width) >= 0:
            self.current_array[blank_index], self.current_array[blank_index - grid_width] = self.current_array[blank_index - grid_width], self.current_array[blank_index]
        if move_code == 2 and blank_index%grid_width != (grid_width - 1):
            self.current_array[blank_index], self.current_array[blank_index + 1] = self.current_array[blank_index + 1], self.current_array[blank_index]
        if move_code == 3 and (blank_index%grid_width) != 0:
            self.current_array[blank_index], self.current_array[blank_index - 1] = self.current_array[blank_index - 1], self.current_array[blank_index]
