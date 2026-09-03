from TaquinGrid import *

class TaquinSolver:
    def get_next_move(self, grid):
        return None
        
    def get_all_moves(self, grid):
        return []

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
        return self.get_move_sequence_with_history(grid, [])
        
    def get_move_sequence_with_history(self, grid, previous_grids):
        if grid.solved():
            return []
        for move_code in range(4):
            move = grid.get_direction_move_info(move_code)
            if move != None:
                new_grid = TaquinGrid(grid.grid_size, grid.current_array.copy())
                new_grid.complete_move(move_code)
                if new_grid.current_array not in previous_grids:
                    new_history = previous_grids + [grid.current_array]
                    next_sequence = self.get_move_sequence_with_history(new_grid, new_history)
                    if next_sequence != None:
                        return [move] + next_sequence
        return None
