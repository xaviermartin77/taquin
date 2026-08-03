import random

class TaquinGrid:
    def __init__(self, size, array = None):
        self.grid_size = size
        self.current_array = array
        if self.current_array == None:
            self.shuffle()
    
    def get_coordinates(self, index):
        return (index % self.grid_size[0], index // self.grid_size[0])
    
    def get_tiles_infos(self, include_text):
        result = []
        for index, element in enumerate(self.current_array):
            if element == (self.grid_size[0] * self.grid_size[1] - 1):
                continue
            value_text = str(element) if include_text else None
            result.append((index, self.get_coordinates(index), self.get_coordinates(element), value_text))
        return result
    
    def shuffle(self):
        self.current_array = list(range(self.grid_size[0] * self.grid_size[1]))
        random.shuffle(self.current_array)
        while not self.is_solvable():
            random.shuffle(self.current_array)
    
    def is_solvable(self):
        (grid_width, grid_height) = self.grid_size
        grid_length = len(self.current_array)
        
        # calculating the number of moves needed to put the blank tile on the right spot
        index_of_blank = self.current_array.index(grid_length-1)
        (x_blank, y_blank) = (index_of_blank % grid_width, index_of_blank // grid_width)
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
        
    def get_blank_tile_coordinates(self):
        return self.get_coordinates(self.current_array.index(len(self.current_array) - 1))
        
    def move_tile_if_possible(self, index):
        blank_tile_coord = self.get_blank_tile_coordinates()
        tile_coord = self.get_coordinates(index)
        if blank_tile_coord[0] == tile_coord[0]:
            if blank_tile_coord[1] == tile_coord[1] - 1:
                self.move_tile(0) # up
                return True
            if blank_tile_coord[1] == tile_coord[1] + 1:
                self.move_tile(1) # down
                return True
        if blank_tile_coord[1] == tile_coord[1]:
            if blank_tile_coord[0] == tile_coord[0] - 1:
                self.move_tile(2) # left
                return True
            if blank_tile_coord[0] == tile_coord[0] + 1:
                self.move_tile(3) # right
                return True
        return False
        
    def move_tile(self, move_code):
        blank_index = self.current_array.index(len(self.current_array) - 1)
        grid_width = self.grid_size[0]
        if move_code == 0 and (blank_index + grid_width) < len(self.current_array):
            self.current_array[blank_index], self.current_array[blank_index + grid_width] = self.current_array[blank_index + grid_width], self.current_array[blank_index]
        if move_code == 1 and (blank_index - grid_width) >= 0:
            self.current_array[blank_index], self.current_array[blank_index - grid_width] = self.current_array[blank_index - grid_width], self.current_array[blank_index]
        if move_code == 2 and blank_index%grid_width != (grid_width - 1):
            self.current_array[blank_index], self.current_array[blank_index + 1] = self.current_array[blank_index + 1], self.current_array[blank_index]
        if move_code == 3 and (blank_index%grid_width) != 0:
            self.current_array[blank_index], self.current_array[blank_index - 1] = self.current_array[blank_index - 1], self.current_array[blank_index]
