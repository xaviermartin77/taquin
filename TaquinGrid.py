import random

class TaquinGrid:
    def __init__(self, size, array = None):
        self.grid_size = size
        self.current_array = array
        if self.current_array == None:
            self.shuffle()
    
    def get_coordinates(self, index):
        return (index % self.grid_size[0], index // self.grid_size[0])
        
    def get_grid_length(self):
        return self.grid_size[0] * self.grid_size[1]
        
    def get_blank_tile_value(self):
        return self.grid_size[0] * self.grid_size[1] - 1
        
    def get_blank_tile_index(self):
        return self.current_array.index(self.get_blank_tile_value())
        
    def get_blank_tile_coordinates(self):
        return self.get_coordinates(self.get_blank_tile_index())
    
    def get_tiles_infos(self):
        result = []
        for index, element in enumerate(self.current_array):
            if element == self.get_blank_tile_value():
                continue
            result.append((index, element, self.get_coordinates(index), self.get_coordinates(element)))
        return result
    
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
        for index, element in enumerate(self.current_array):
            if element != index:
                return False
        return True
        
    def get_tile_move(self, index):
        blank_tile_coord = self.get_blank_tile_coordinates()
        tile_coord = self.get_coordinates(index)
        move_code = None
        if blank_tile_coord[0] == tile_coord[0]:
            if blank_tile_coord[1] == tile_coord[1] - 1:
                move_code = 0 # up
            if blank_tile_coord[1] == tile_coord[1] + 1:
                move_code = 1 # down
        if blank_tile_coord[1] == tile_coord[1]:
            if blank_tile_coord[0] == tile_coord[0] - 1:
                move_code = 2 # left
            if blank_tile_coord[0] == tile_coord[0] + 1:
                move_code = 3 # right
        if move_code != None:
            return (index, move_code, 0)
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
