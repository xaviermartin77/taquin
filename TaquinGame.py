from TaquinImagesScreen import *
from TaquinImagesViewModel import *
from PygameSDK.Game import *
from TaquinEntity.TaquinGrid import *
from TaquinSolver.AlgoSolver import *
from TaquinSolver.BruteForceSolver import *
import itertools


view_model = TaquinImagesViewModel()
screen_size = (1500, 1000)
screen = TaquinImagesScreen(view_model, screen_size)
game = Game()
game.start_game(screen)
'''
# TODO : get all permutations for 3x2 grid, try to solve for each case, compare bruteforce solution with algo solution

bruteforce_solver = BruteForceSolver()
algo_solver = AlgoSolver()
array_list = list(itertools.permutations([0,1,2,3,4,5,6,7]))

hard_count = 0
imperfect_count = 0
two_count = 0
four_count = 0
six_count = 0
for array in array_list:
    grid = TaquinGrid((4,2), list(array))
    if not grid.is_solvable() or grid.solved():
        continue
    #test_algo = algo_solver.get_all_moves(grid)
    #print(test_algo)
    #diff = len(algo_solver.get_all_moves(grid)) - len(bruteforce_solver.get_all_moves(grid))
    count = len(algo_solver.get_all_moves(grid))
    if count > 45 :
        print(count)
        print(array)
        hard_count += 1
        print(len(bruteforce_solver.get_all_moves(grid)))
#print('total sub optimal : ' + str(imperfect_count))
print('total maybec sub optimal : ' + str(hard_count))
'''
