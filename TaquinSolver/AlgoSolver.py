from TaquinEntity.TaquinGrid import *
from TaquinSolver.TaquinSolver import *

class AlgoSolver(TaquinSolver):
    def __init__(self):
        self.memorized_list = []
    
    def get_next_move(self, grid):
        copy_grid = SolvableGrid(grid.grid_size, grid.current_array.copy())
        if copy_grid.solved(): # grid already solved
            return None
        if copy_grid.is_final_square():
            self.solve_final_square(copy_grid)
        elif copy_grid.is_last_two_lines():
            self.solve_last_two_lines(copy_grid)
        elif copy_grid.is_last_two_elements_of_line():
            self.solve_last_two_elements_of_line(copy_grid)
        else:
            self.solve_common_case(copy_grid)
    
    def get_all_moves(self, grid):
        move_sequence = []
        copy_grid = SolvableGrid(grid.grid_size, grid.current_array.copy())
        while not copy_grid.solved():
            next_move = self.get_next_move(copy_grid)
            if next_move == None:
                print('An error occured while solving')
                break
            move_sequence.append(next_move)
            copy_grid.complete_move(move[1])
        return move_sequence
    
    def solve_final_square(self, grid):
        print('final square')
        return None
    
    def solve_last_two_lines(self, grid):
        print('last two lines')
        return None
    
    def solve_last_two_elements_of_line(self, grid):
        print('last two elements of line')
        return None
    
    def solve_common_case(self, grid):
        print('common case')
        return None

class SolvableGrid(TaquinGrid):
    def get_first_unsolved_tile_coordinates(self):
        filter_result = next(filter(lambda item: item[0] != item[1], enumerate(self.current_array)), None)
        if filter_result == None: # grid already solved, should not happen
            return self.grid_size
        return self.get_coordinates(filter_result[0])
    
    def get_last_line_first_unsolved_tile_x(self):
        filter_result = next(filter(lambda item: item[0] != item[1] and self.get_grid_length() - 1 - item[0] < self.grid_size[0], enumerate(self.current_array)), None)
        if filter_result == None: # last line fully solved
            return self.grid_size[0]
        return self.get_coordinates(filter_result[0])[0]
    
    def is_final_square(self):
        (grid_width, grid_height) = self.grid_size
        (first_unsolved_x, first_unsolved_y) = self.get_first_unsolved_tile_coordinates()
        if grid_height - first_unsolved_y >= 3:
            return False
        last_line_first_unsolved_tile_x = self.get_last_line_first_unsolved_tile_x()
        first_unsolved_rank = first_unsolved_x if first_unsolved_x < last_line_first_unsolved_tile_x else last_line_first_unsolved_tile_x
        return (grid_width - first_unsolved_rank < 3) and (grid_height - first_unsolved_y < 3)
    
    def is_last_two_lines(self):
        return self.grid_size[1] - self.get_first_unsolved_tile_coordinates()[1] < 3
    
    def is_last_two_elements_of_line(self):
        return self.grid_size[0] - self.get_first_unsolved_tile_coordinates()[0] < 3
