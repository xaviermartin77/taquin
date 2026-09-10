import math
from TaquinEntity.TaquinGrid import *
from TaquinSolver.TaquinSolver import *

class BruteForceSolver(TaquinSolver):
    def __init__(self):
        self.memorized_list = []
    
    def get_next_move(self, grid):
        if len(self.memorized_list) == 0:
            self.memorized_list = self.get_all_moves(grid)
        if len(self.memorized_list) == 0:
            return None
        next_move = (self.memorized_list[0][0], self.memorized_list[0][1])
        self.memorized_list.pop(0)
        return next_move
        
    def get_all_moves(self, grid):
        if grid.solved():
            return []
        former_positions = { 0 : [([], grid)] }
        former_arrays = [grid.current_array]
        current_step = 1
        while len(former_arrays) < (math.factorial(len(grid.current_array)) / 2):
            print('step : ' + str(current_step))
            print('arrays : ' + str(len(former_arrays)))
            if len(former_positions[current_step - 1]) == 0:
                break
            new_list = []
            for pair in former_positions[current_step - 1]:
                former_sequence = pair[0]
                former_grid = pair[1]
                for move_code in range(4):
                    move = former_grid.get_direction_move_info(move_code)
                    if move != None:
                        new_grid = TaquinGrid(grid.grid_size, former_grid.current_array.copy())
                        new_grid.complete_move(move_code)
                        if new_grid.solved():
                            return former_sequence + [move]
                        array_already_found = False
                        for array in former_arrays:
                            if array == new_grid.current_array:
                                array_already_found = True
                                break
                        if array_already_found:
                            continue
                        former_arrays.append(new_grid.current_array)
                        new_sequence = former_sequence.copy() + [move]
                        new_list.append((new_sequence, new_grid))
            former_positions[current_step] = new_list
            current_step = current_step + 1
        print('Error while solving')
        return []
