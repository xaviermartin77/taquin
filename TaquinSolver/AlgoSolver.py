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
            return self.get_next_move_final_square(copy_grid)
        elif copy_grid.is_last_two_lines():
            return self.get_next_move_last_two_lines(copy_grid)
        elif copy_grid.is_last_two_elements_of_line():
            return self.get_next_move_last_two_elements_of_line(copy_grid)
        else:
            return self.get_next_move_common_case(copy_grid)
    
    def get_all_moves(self, grid):
        move_sequence = []
        copy_grid = SolvableGrid(grid.grid_size, grid.current_array.copy())
        while not copy_grid.solved():
            next_move = self.get_next_move(copy_grid)
            if next_move == None:
                print('An error occured while solving')
                break
            move_sequence.append(next_move)
            copy_grid.complete_move(next_move[1])
        return move_sequence
    
    def get_next_move_final_square(self, grid):
        (square_array, limits) = grid.get_last_square_array_and_limits()
        rotate_chrono = None
        if square_array[0] == 0:
            rotate_chrono = square_array[1] == 1
        elif square_array[3] == 0:
            rotate_chrono = square_array[1] != 3
        else:
            rotate_chrono = square_array[2] == 0
        move = grid.get_rotation_move_info(rotate_chrono, limits)
        if move == None:
            print('An error occured while solving')
        return move
    
    def get_next_move_last_two_lines(self, grid):
        two_lines_array = grid.get_last_two_lines_array()
        move_direction = self.get_move_direction_for_two_lines_array(two_lines_array)
        return grid.get_direction_move_info(move_direction)
        
    def get_move_direction_for_two_lines_array(self, array):
        adapted_grid = SolvableGrid((len(array)/2, 2), array)
        (first_column_index, last_column_index) = (0, len(array)/2 - 1)
        (top_x, top_y) = adapted_grid.get_tile_coordinates(0)
        (bottom_x, bottom_y) = adapted_grid.get_tile_coordinates(1)
        (blank_x, blank_y) = adapted_grid.get_tile_coordinates(-1)
        target_line = 0 if bottom_x < top_x else 1 if top_x < bottom_x else None
        left_tile_y = bottom_y if bottom_x < top_x else top_y if top_x < bottom_x else None
        right_tile_y = bottom_y if bottom_x > top_x else top_y if top_x > bottom_x else None
        vertical_move = 0 if blank_y == 0 else 1
        if blank_x < min(top_x, bottom_x):
            if blank_x == min(top_x, bottom_x) - 1:
                if top_x == bottom_x:
                    move_direction = 2 # move left (no choice)
                elif left_tile_y == target_line:
                    move_direction = 2 if blank_y == target_line else vertical_move
                else:
                    move_direction = 2 if blank_y != target_line else vertical_move
            else:
                move_direction = 2 # move left
        elif blank_x == min(top_x, bottom_x):
            if max(top_x, bottom_x) == blank_x + 1:
                if right_tile_y == target_line:
                    if blank_x == first_column_index:
                        move_direction = 2 if right_tile_y == blank_y else vertical_move
                    else:
                        move_direction = 3 if left_tile_y == target_line else vertical_move
                else:
                    if blank_x == first_column_index:
                        move_direction = 2 if right_tile_y != blank_y else vertical_move
                    else:
                        move_direction = 3
            else:
                move_direction = 2 if blank_y != target_line else vertical_move
        elif blank_x > min(top_x, bottom_x) and blank_x < max(top_x, bottom_x):
            if left_tile_y != target_line and blank_x == min(top_x, bottom_x) + 1:
                move_direction = 3 if blank_y != left_tile_y else vertical_move
            elif blank_x == max(top_x, bottom_x) - 1:
                if right_tile_y == target_line:
                    move_direction = 2 if blank_y == target_line else vertical_move
                else:
                    move_direction = 2 if blank_y != target_line else vertical_move
            else:
                move_direction = 2
        elif blank_x == max(top_x, bottom_x):
            if min(top_x, bottom_x) == blank_x - 1:
                if left_tile_y == target_line:
                    move_direction = 3 if right_tile_y == target_line else vertical_move
                else:
                    if blank_x == last_column_index:
                        move_direction = 3 if left_tile_y != blank_y else vertical_move
                    else:
                        move_direction = 2
            else:
                move_direction = 3 if blank_y != target_line else vertical_move
        else:
            if blank_x == max(top_x, bottom_x) + 1:
                if top_x == bottom_x:
                    move_direction = 3 # move right (no choice)
                elif min(top_x, bottom_x) == max(top_x, bottom_x) - 1 and left_tile_y != target_line:
                    move_direction = 3 if blank_y == right_tile_y else vertical_move
                else:
                    move_direction = 3 if blank_y != right_tile_y else vertical_move
            else:
                move_direction = 3 # move right
        return move_direction
    
    def get_next_move_last_two_elements_of_line(self, grid):
        if grid.is_two_columns_solvable():
            mirror_two_lines_array = grid.get_two_lines_array_from_last_two_columns()
            mirror_move_direction = self.get_move_direction_for_two_lines_array(mirror_two_lines_array)
            correct_move_direction = self.get_mirror_move_direction(mirror_move_direction)
            return grid.get_direction_move_info(correct_move_direction)
        return None # manage translate three tiles (two targets and blank tile) on two last columns here
        
    def get_mirror_move_direction(self, move_direction):
        if move_direction == 0: # up
            return 3 # right
        if move_direction == 1: # down
            return 2 # left
        if move_direction == 2: # left
            return 0 # up
        if move_direction == 3: # right
            return 1 # down
    
    def get_next_move_common_case(self, grid):
        ((target_x, target_y), (tile_x, tile_y), (blank_x, blank_y), (last_line_index, last_column_index)) = grid.get_common_array_info()
        if (blank_x - tile_x) >= 2:
            move_direction = 0 if (blank_x, blank_y) == (target_x, target_y) else 3
        elif (tile_x - blank_x) >= 2:
            move_direction = 2
        elif (blank_y - tile_y) >= 2:
            move_direction = 1
        elif (tile_y - blank_y) >= 2:
            move_direction = 0
        elif tile_x < target_x:
            if blank_x == tile_x:
                move_direction = 2
            elif blank_x < tile_x:
                move_direction = 2 if blank_y != tile_y else 1 if tile_y == last_line_index else 0
            else:
                move_direction = 3 if blank_y == tile_y else 1 if blank_y > tile_y else 0
        elif tile_x > target_x:
            if blank_x == tile_x:
                move_direction = 3
            elif blank_x > tile_x:
                move_direction = 3 if blank_y != tile_y else 1 if tile_y == last_line_index else 0
            else:
                move_direction = 2 if blank_y == tile_y else 1 if blank_y > tile_y else 0
        else: # target_x == tile_x => tile_y < target_y
            if blank_x == tile_x:
                move_direction = 0 if blank_y < tile_y else 3 if tile_x == last_column_index else 2
            elif blank_x > tile_x:
                move_direction = 3 if blank_y < tile_y else 1
            else:
                if tile_y == target_y + 1:
                    move_direction = 2 if blank_y > tile_y else 0
                else:
                    move_direction = 2 if blank_y < tile_y else 1
        return grid.get_direction_move_info(move_direction)


class SolvableGrid(TaquinGrid):
    def get_first_unsolved_tile_coordinates(self):
        filter_result = next(filter(lambda item: item[0] != item[1], enumerate(self.current_array)), None)
        if filter_result == None: # grid already solved, should not happen
            return self.grid_size
        return self.get_coordinates(filter_result[0])
    
    def get_last_two_lines_first_unsolved_rank(self):
        filter_result = next(filter(lambda item: item[0] != item[1] and self.get_grid_length() - 1 - item[0] < self.grid_size[0], enumerate(self.current_array)), None)
        last_line_first_unsolved_tile_x = self.grid_size[0] if filter_result == None else self.get_coordinates(filter_result[0])[0]
        first_unsolved_x = self.get_first_unsolved_tile_coordinates()[0]
        return min(first_unsolved_x, last_line_first_unsolved_tile_x)
        
    def get_last_two_elements_of_unsolved_line(self):
        if not self.is_last_two_elements_of_line():
            return (grid_width * grid_height - 2, grid_width * grid_height - 1)
        filter_result = next(filter(lambda item: item[0] != item[1], enumerate(self.current_array)), None)
        if filter_result == None: # grid already solved, should not happen
            return (grid_width * grid_height - 2, grid_width * grid_height - 1)
        first_unsolved_index = filter_result[0]
        if self.get_coordinates(first_unsolved_index)[0] == self.grid_size[0] - 1:
            return (first_unsolved_index - 1, first_unsolved_index)
        else:
            return (first_unsolved_index, first_unsolved_index + 1)
    
    def is_final_square(self):
        (grid_width, grid_height) = self.grid_size
        if grid_height - self.get_first_unsolved_tile_coordinates()[1] >= 3:
            return False
        last_two_lines_first_unsolved_rank = self.get_last_two_lines_first_unsolved_rank()
        return grid_width - last_two_lines_first_unsolved_rank < 3
    
    def is_last_two_lines(self):
        return self.grid_size[1] - self.get_first_unsolved_tile_coordinates()[1] < 3
    
    def is_last_two_elements_of_line(self):
        return self.grid_size[0] - self.get_first_unsolved_tile_coordinates()[0] < 3
        
    def is_two_columns_solvable(self):
        (first_index, second_index) = self.get_last_two_elements_of_unsolved_line()
        first_index_tile_x = self.get_tile_coordinates(first_index)[0]
        second_index_tile_x = self.get_tile_coordinates(second_index)[0]
        blank_x = self.get_blank_tile_coordinates()[0]
        return self.grid_size[0] - first_index_tile_x < 3 and self.grid_size[0] - second_index_tile_x < 3  and self.grid_size[0] - blank_x < 3
    
    def get_last_square_array_and_limits(self):
        (grid_width, grid_height) = self.grid_size
        first_index = grid_width * (grid_height - 1) - 2
        last_index = grid_width * grid_height - 1
        square_array = []
        for index, value in enumerate([self.current_array[first_index], self.current_array[first_index + 1], self.current_array[last_index - 1], self.current_array[last_index]]):
            if value == first_index:
                square_array.append(0)
            if value == first_index + 1:
                square_array.append(1)
            if value == last_index - 1:
                square_array.append(2)
            if value == last_index:
                square_array.append(3)
        return (square_array, (first_index, last_index))
    
    def get_last_two_lines_array(self):
        (grid_width, grid_height) = self.grid_size
        last_two_lines_first_unsolved_rank = self.get_last_two_lines_first_unsolved_rank()
        
        first_index = grid_width * (grid_height - 1) - (grid_width - last_two_lines_first_unsolved_rank)
        second_index = grid_width * grid_height - (grid_width - last_two_lines_first_unsolved_rank)
        last_index = grid_width * grid_height - 1
        
        square_array = []
        for column_index in range(grid_height - 2, grid_height):
            for line_index in range(last_two_lines_first_unsolved_rank, grid_width):
                value = self.current_array[line_index + grid_width * column_index]
                if value == first_index:
                    square_array.append(0)
                elif value == second_index:
                    square_array.append(1)
                elif value == last_index:
                    square_array.append(-1)
                else:
                    square_array.append(None)
        return square_array
        
    def get_two_lines_array_from_last_two_columns(self):
        (grid_width, grid_height) = self.grid_size
        (first_index, second_index) = self.get_last_two_elements_of_unsolved_line()
        last_index = grid_width * grid_height - 1
        start_column_index = self.get_first_unsolved_tile_coordinates()[1]
        
        square_array = []
        for line_index in range(grid_width - 1, grid_width - 3, -1):
            for column_index in range(start_column_index, grid_height):
                value = self.current_array[line_index + grid_width * column_index]
                if value == first_index:
                    square_array.append(1)
                elif value == second_index:
                    square_array.append(0)
                elif value == last_index:
                    square_array.append(-1)
                else:
                    square_array.append(None)
        return square_array
        
    def get_common_array_info(self):
        (grid_width, grid_height) = self.grid_size
        first_unsolved_coord = self.get_first_unsolved_tile_coordinates()
        tile_coord = self.get_tile_coordinates(first_unsolved_coord[0] + grid_width * first_unsolved_coord[1])
        blank_coord = self.get_blank_tile_coordinates()
        grid_limits = (grid_width - 1, grid_height - 1)
        return (first_unsolved_coord, tile_coord, blank_coord, grid_limits)
