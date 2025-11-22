import random

# static, teste si le tableau est solvable, en utilisant la taille de la grid
def is_array_solvable(array, grid_size):
        (grid_width, grid_height) = grid_size
        grid_length = grid_width * grid_height
        test_array = list(range(grid_length))
        count = 0
        for i in range(grid_length):
                test_array[i] = array[i]
                if test_array[i] == grid_length-1:
                        (x,y) = (i % grid_width, i // grid_width)
                        count = count + grid_width + grid_height - x - y
        for i in range(grid_length):
                if test_array[i] != i:
                        for j in range(i,grid_length):
                                if test_array[j] == i:
                                        test_array[j] = test_array[i]
                                        test_array[i] = i
                                        count = count + 1
        return (count%2 == 0)

# static, génère un array random mais solvable
def get_random_array(grid_size):
        (grid_width, grid_height) = grid_size
        grid_length = grid_width * grid_height
        array = list(range(grid_length))
        solvable = False
        while not solvable:
                random.shuffle(array)
                solvable = is_array_solvable(array, grid_size)
        return array
                                  
