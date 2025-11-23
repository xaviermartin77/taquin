import math 
from taquinConstants import *
from taquinUtils import *


'''
# solver, à voir plus tard

def solveDoubleHorizontal(currentArray, target_column, grid_width, grid_height):
        up_target_index = (grid_height - 2) * grid_width + target_column
        down_target_index = (grid_height - 1) * grid_width + target_column
        
        blank_index = -1
        up_index = -1
        down_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == up_target_index:
                        up_index = i
                if currentArray[i] == down_target_index:
                        down_index = i
                if blank_index != -1 and up_index != -1 and down_index != -1:
                        break
        if blank_index == -1 or up_index == -1 or down_index == -1 :
                return (-1,-1)

        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        up_x, up_y = getPositionFromIndex(up_index, grid_width)
        down_x, down_y = getPositionFromIndex(down_index, grid_width)
        target_x = target_column
        target_up_y = grid_height - 2
        target_down_y = grid_height - 1
        
        if (blank_x < target_x + 3) and (up_x < target_x + 3) and (down_x < target_x + 3):
                if up_x == target_x and down_x == target_x:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                if (up_x == target_x) or (down_x == target_x):
                        if blank_x == target_x:
                                if up_x == target_x + 1 or  down_x == target_x + 1:
                                        if (up_x == target_x and up_y > blank_y) or (down_x == target_x and down_y < blank_y):
                                                orientation = 2 if blank_y == grid_height - 1 else 3
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                                else:
                                        if (up_x == target_x and up_y < blank_y) or (down_x == target_x and down_y > blank_y):
                                                orientation = 2 if blank_y == grid_height - 1 else 3
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if (up_y == target_up_y and up_x == target_x) or (down_y == target_down_y and down_x == target_x):
                                if blank_x == target_x + 1 and ((up_x == target_x and blank_y != up_y and (up_y != down_y or down_x != up_x + 1)) or (down_x == target_x and blank_y != down_y and (up_y != down_y or up_x != down_x + 1))):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = up_target_index + 1
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                        else:
                                if blank_x == target_x + 1 and ((up_y == target_up_y and up_x == target_x + 1) or (down_y == target_down_y and down_x == target_x + 1)):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = up_target_index + 1
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                else:
                        if blank_x == target_x and up_x == down_x:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if blank_x < target_x + 2 and ((up_x == target_x + 2 and down_x < target_x + 2) or (up_x < target_x + 2 and down_x == target_x + 2)):
                                orientation = True if up_x < target_x + 2 else False
                                firstIndex = up_target_index
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, orientation)
                        else:
                                #TODO : find good rotate orientation
                                firstIndex = up_target_index + 1
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)

        
        if (blank_x < up_x and blank_x > down_x) or (blank_x > up_x and blank_x < down_x) or (blank_x < up_x and blank_x < down_x):
                if ((blank_x == up_x - 1 and blank_y != up_y) or (blank_x == down_x - 1 and blank_y != down_y)) and up_x != down_x:
                        orientation = 2 if blank_y == grid_height - 1 else 3
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
        
        if blank_x > up_x and blank_x > down_x:
                if ((blank_y == up_y and blank_x == up_x + 1) or (blank_y == down_y and blank_x == down_x + 1)) and up_x != down_x:
                        orientation = 2 if blank_y == grid_height - 1 else 3
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                else:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                
        if blank_x == up_x or blank_x == down_x:
                if blank_x < up_x or blank_x < down_x:
                        if (blank_x == up_x and up_y == target_up_y) or (blank_x == down_x and down_y == target_down_y):
                                orientation = 2 if blank_y == grid_height - 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                if (up_x == blank_x + 1) or (down_x == blank_x + 1):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                else:
                        if up_y != down_y:
                                orientation = 2 if blank_y == grid_height - 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                
                                
        
        return(-1,-1)

def solveDoubleVertical(currentArray, target_line, grid_width, grid_height):
        left_target_index = (target_line + 1) * grid_width - 2
        right_target_index = (target_line + 1) * grid_width - 1

        blank_index = -1
        left_index = -1
        right_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == left_target_index:
                        left_index = i
                if currentArray[i] == right_target_index:
                        right_index = i
                if blank_index != -1 and left_index != -1 and right_index != -1:
                        break
        if blank_index == -1 or left_index == -1 or right_index == -1 :
                return (-1,-1)

        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        left_x, left_y = getPositionFromIndex(left_index, grid_width)
        right_x, right_y = getPositionFromIndex(right_index, grid_width)
        target_y = target_line
        target_left_x = grid_width - 2
        target_right_x = grid_width - 1

        # cas à gérer : left ou right ou blank pas encore dans les colonnes
        if blank_x < target_left_x or left_x < target_left_x or right_x < target_left_x:
                # left et right dans la bonne colonne mais pas blank
                if (left_x >= target_left_x and right_x >= target_left_x):
                        if blank_y == left_y or blank_y == right_y:
                                # TODO : handle special case 3 line missing, left and right blocking blank
                                if blank_y  == target_y + 1:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                if blank_y  == grid_height - 1:
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                if left_y == target_y + 1 or right_y == target_y + 1:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                # blank à droite de left et right
                if left_x < blank_x and right_x < blank_x:
                        # blank parmi les deux cases target, aller vers le bas
                        if blank_y == target_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        # aller vers la droite, sauf si les deux cases sur la même colonne juste à gauche, alors aller à la hauteur du plus haut, puis aller vers la droite
                        else:
                                print('cas particulier')
                                # return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                # blank à gauche de left et right
                if left_x > blank_x and right_x > blank_x:
                        # left ou right dans la colonne juste à droite, ne pas aller vers la gauche, aller vers le haut ou le bas selon les cas
                        if (blank_y == left_y and left_x == blank_x + 1) or (blank_y == right_y and right_x == blank_x + 1):
                                print('cas particulier')
                        # aller vers la gauche
                        else:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                # blank entre left et right, se mettre au niveau de la plus à gauche puis aller vers la droite
                if (left_x < blank_x and right_x > blank_x) or (left_x > blank_x and right_x < blank_x):
                        print('cas particulier')
                        #return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                # blank sur la colonne de left ou de right
                # à gérer : autre case à gauche -> aller vers la gauche (aller chercher l'autre cas, prioritaire)
                # à gérer : autre case à droite -> bouger la case verticalement vers l'autre (ou le plus haut possible si case tout en haut)
                # à gérer : autre case sur la même colonne -> si case la plus basse en dessous, monter, si blank en dessous des deux cases adjacentes, aller vers la gauche, sinon aller vers la droite (pour se décaler et continuer la montée)
                        
                # cas blank à gauche des deux : aller vers la droite sauf si un des deux sur le chemin (cf les deux déjà dans la colonne ?)
                # cas blank à droite des deux : aller vers la gauche, sauf si sur la ligne en cours de solve
                # cas entre les deux : aller vers la droite (attention cas particuliers ?)
                # cas meme colonne que celui de droite
                # cas meme colonne que celui de gauche
                # stratégie : mettre les 2 sur la meme ligne en gérant la partie gauche d'abord, gérer les cas particuliers 'tout à gauche' et 'sur la meme colonne'

                # si plus d'une colonne d'écart : décaler le plus à gauche vers la droite (à développer)
                # si meme colonne : passer par le haut ou le bas pour décaller celui du haut vers la droite (attention : cas particulier 3 lignes à solve)
                # si une colonne d'écart : monter le plus en bas (passer par la droite ou la gauche)
                # si une colonne d'écart, les 2 sur la meme ligne : décaller l'ensemble vers la droite

        # deux dernières colonnes uniquement, blank ou left ou right pas encore dans un bloc de 6
        if (blank_y < target_y + 3) and (left_y < target_y + 3) and (right_y < target_y + 3):
                if left_y == target_y and right_y == target_y:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                if (left_y == target_y) or (right_y == target_y):
                        if blank_y == target_y:
                                if right_y == target_y + 1 or  left_y == target_y + 1:
                                        if (left_y == target_y and left_x > blank_x) or (right_y == target_y and right_x < blank_x):
                                                orientation = 0 if blank_x == grid_width - 1 else 1
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                else:
                                        if (left_y == target_y and left_x < blank_x) or (right_y == target_y and right_x > blank_x):
                                                orientation = 0 if blank_x == grid_width - 1 else 1
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        if (left_x == target_left_x and left_y == target_y) or (right_x == target_right_x and right_y == target_y):
                                if blank_y == target_y + 1 and ((left_y == target_y and blank_x != left_x and (right_x != left_x or right_y != left_y + 1)) or (right_y == target_y and blank_x != right_x and (right_x != left_x or left_y != right_y + 1))):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = left_target_index + grid_width
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                        else:
                                if blank_y == target_y + 1 and ((left_x == target_left_x and left_y == target_y + 1) or (right_x == target_right_x and right_y == target_y + 1)):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = left_target_index + grid_width
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                else:
                        if blank_y == target_y and left_y == right_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        if blank_y < target_y + 2 and ((left_y == target_y + 2 and right_y < target_y + 2) or (left_y < target_y + 2 and right_y == target_y + 2)):
                                orientation = True if right_y < target_y + 2 else False
                                firstIndex = left_target_index
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, orientation)
                        else:
                                #TODO : find good rotate orientation
                                firstIndex = left_target_index + grid_width
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
        # bloc de 6 (les 3 paragraphes)       
        if (blank_y < left_y and blank_y > right_y) or (blank_y > left_y and blank_y < right_y) or (blank_y < left_y and blank_y < right_y):
                if ((blank_y == left_y - 1 and blank_x != left_x) or (blank_y == right_y - 1 and blank_x != right_x)) and left_y != right_y:
                        orientation = 0 if blank_x == grid_width - 1 else 1
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
        
        if blank_y > left_y and blank_y > right_y:
                if ((blank_x == right_x and blank_y == right_y + 1) or (blank_x == left_x and blank_y == left_y + 1)) and left_y != right_y:
                        orientation = 0 if blank_x == grid_width - 1 else 1
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                else:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                
        if blank_y == left_y or blank_y == right_y:
                if blank_y < left_y or blank_y < right_y:
                        if (blank_y == left_y and left_x == target_left_x) or (blank_y == left_y and left_x == target_left_x):
                                orientation = 0 if blank_x == grid_width - 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                if (left_y == blank_y + 1) or (right_y == blank_y + 1):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                else:
                        if left_x != right_x:
                                orientation = 0 if blank_x == grid_width - 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                
                                
        
        return(-1,-1)

def solveGeneral(currentArray, target_index, grid_width, grid_height):
        blank_index = -1
        tile_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == target_index:
                        tile_index = i
                if blank_index != -1 and tile_index != -1:
                        break
        if blank_index == -1 or tile_index == -1:
                return (-1,-1)
        
        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        target_x, target_y = getPositionFromIndex(target_index, grid_width)
        tile_x, tile_y = getPositionFromIndex(tile_index, grid_width)
        
        if tile_x == target_x:
                if blank_y < tile_y:
                        if blank_x == tile_x:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        else:
                                orientation = 0 if blank_x > tile_x else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_y == tile_y:
                        orientation = 3 if (blank_x < tile_x and tile_y == target_y + 1) else 2
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_y > tile_y:
                        if blank_x == tile_x:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if blank_x > tile_x:
                                return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                        if blank_x < tile_x:
                                orientation = 3 if tile_y > target_y + 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
        else:
                if (blank_x < tile_x and target_x <= blank_x) or (blank_x > tile_x and target_x >= blank_x):
                        if blank_y == tile_y:
                                orientation = 1 if blank_x < tile_x else 0
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                orientation = 2 if blank_y > tile_y else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_x == tile_x:
                        if blank_y < tile_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        else:
                                orientation = 1 if target_x > tile_x else 0
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if (blank_x > tile_x and target_x <= blank_x) or (blank_x < tile_x and target_x >= blank_x):
                        if blank_y == tile_y:
                                orientation = 2 if tile_y > target_y + 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                orientation = 0 if blank_x > tile_x else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
        return(-1,-1)



'''

# static, créé un id pour un array donné (utilisé pour le solver brute force)
def get_key_from_array(array):
        strings = [str(integer) for integer in array]
        string = '|'.join(strings)
        return string

# static, génère une array à partir d'un id (utilisé pour le solver brute force)
def get_array_from_key(key):
        strings = key.split('|')
        array = []
        for string in strings:
                array.append(int(string))
        return array

# static, methode de test pour obtenir toutes les permutations d'un tableau de taille n
def get_all_permutations(grid_size):
        (grid_width, grid_height) = grid_size
        n = grid_width * grid_height
        array = list(range(n))
        arrays = [list(range(n))]
        count = []
        for i in range(n):
                count.append(0)
        index = 0
        while index < n:
                if count[index] < index:
                        if index%2 == 0:
                                temp_value = array[0]
                                array[0] = array[index]
                                array[index] = temp_value
                        else:
                                temp_value = array[count[index]]
                                array[count[index]] = array[index]
                                array[index] = temp_value
                        if is_array_solvable(array, grid_size):
                                new_array = []
                                for element in array:
                                        new_array.append(element)
                                arrays.append(new_array)
                        count[index] = count[index] + 1
                        index = 0
                else:
                        count[index] = 0
                        index = index + 1
        return arrays

class Solver:
        def __init__(self, grid_size):
                self.grid_size = grid_size
                self.shortest_ways = {}

        def get_move_count_algo(self, current_array):
                count = 0
                solved = all(current_array[i] <= current_array[i+1] for i in range(len(current_array)-1))
                while not solved:
                        (direction, rotation) = self.get_next_move_algo(current_array)
                        if direction == -1 and rotation == None:
                                #print('no solution found')
                                return -1
                        current_array = self.update_array_with_direction_if_possible(current_array, direction, rotation)
                        count = count + 1
                        solved = all(current_array[i] <= current_array[i+1] for i in range(len(current_array)-1))
                return count

        def get_next_move_algo(self, current_array):
                (grid_width, grid_height) = self.grid_size
                solved_column_count = 0
                solved_line_count = 0
                for index, value in enumerate(current_array): # finding the first index that is not solved
                        if value == index:
                                solved_column_count = solved_column_count + 1
                                if solved_column_count == grid_width:
                                        solved_column_count = 0
                                        solved_line_count = solved_line_count + 1
                        else:
                                break
                if solved_line_count == grid_height:
                        return (-1, None)
                if grid_height - solved_line_count < 3: # only two lines to solve
                        solved_column_count = 0
                        for j in range(grid_width):
                                top_tile_index = grid_width*(grid_height-2) + j
                                bottom_tile_index = grid_width*(grid_height-1) + j
                                if current_array[top_tile_index] == top_tile_index and current_array[bottom_tile_index] == bottom_tile_index:
                                        solved_column_count = solved_column_count + 1
                                else:
                                        break
                        if grid_width - solved_column_count < 3: # only four tiles to solve
                                return self.get_next_move_final_square(current_array)
                        else:
                                #print('get_next_move_last_two_lines')
                                return self.get_next_move_last_two_lines(current_array, solved_column_count)
                else:
                        if grid_width - solved_column_count < 3: # only two elements to handle before solving the line
                                #print('get_next_move_last_two_elements_in_line')
                                return self.get_next_move_last_two_elements_in_line(current_array)
                        else:
                                #print('get_next_move_common_case')
                                return self.get_next_move_common_case(current_array)
                return -1

        def get_next_move_final_square(self, current_array):
                (grid_width, grid_height) = self.grid_size
                first_index = grid_width * (grid_height - 1) - 2
                last_index = grid_width * grid_height - 1
                square_array = [current_array[first_index], current_array[first_index + 1], current_array[last_index - 1], current_array[last_index]]
                rotation = self.get_next_rotation_square(square_array, 0, first_index, 3, last_index)
                return (-1, (rotation, first_index, last_index))
                '''
                if square_array[0] ==  first_index:
                        if square_array[1] == last_index:
                                return (-1, (False, first_index, last_index))
                        else:
                                return (-1, (True, first_index, last_index))
                if square_array[1] ==  first_index:
                        return (-1, (False, first_index, last_index))
                if square_array[2] ==  first_index:
                        return (-1, (True, first_index, last_index))
                if square_array[3] ==  first_index:
                        if square_array[1] == last_index:
                                return (-1, (False, first_index, last_index))
                        else:
                                return (-1, (True, first_index, last_index))
                return (-1, None)
                '''

        def get_next_rotation_square(self, array, target_position, target_index, blank_position, blank_index):
                if array[target_position] == target_index:
                        temp_position = target_position
                        while array[temp_position] != blank_index and temp_position != blank_position:
                                temp_position = self.get_next_square_chrono(temp_position)
                        if array[temp_position] == blank_index:
                                return False
                        else:
                                return True
                second_position = self.get_next_square_chrono(target_position)
                if array[second_position] == target_index:
                        return False
                opposite_position = self.get_next_square_chrono(second_position)
                if array[opposite_position] == target_index:
                        next_position = self.get_next_square_chrono(opposite_position)        
                        if array[next_position] == blank_index:
                                return True
                        else:
                                return False
                last_position = self.get_next_square_chrono(opposite_position)
                if array[last_position] == target_index:
                        return True

        def get_next_square_chrono(self, index):
                if index == 0:
                        return 1
                if index == 1:
                        return 3
                if index == 3:
                        return 2
                if index == 2:
                        return 0

        # prérequis : avoir un patron de la solution attendue
        # piste 1 : copier / coller en simplifiant l'algo du square_array
        # piste 2 : généraliser l'algo square, le rendre compatible avec n'importe quelle solution attendue
        def get_next_move_last_two_lines(self, array, target_column):
                (grid_width, grid_height) = self.grid_size
                up_target_index = (grid_height - 2) * grid_width + target_column
                down_target_index = (grid_height - 1) * grid_width + target_column
        
                blank_index = -1
                up_index = -1
                down_index = -1
                for i in range(len(array)):
                        if array[i] == len(array)-1:
                                blank_index = i
                        if array[i] == up_target_index:
                                up_index = i
                        if array[i] == down_target_index:
                                down_index = i
                        if blank_index != -1 and up_index != -1 and down_index != -1:
                                break
                if blank_index == -1 or up_index == -1 or down_index == -1 :
                        return (-1, None)

                (blank_x, blank_y) = (blank_index % grid_width, blank_index // grid_width)
                (up_x, up_y) = (up_index % grid_width, up_index // grid_width)
                (down_x, down_y) = (down_index % grid_width, down_index // grid_width)
                target_up_y = grid_height - 2
                target_down_y = grid_height - 1
        
                if (blank_x < target_column + 3) and (up_x < target_column + 3) and (down_x < target_column + 3):
                        if up_x == target_column and down_x == target_column: # les deux cases cibles sont sur la colonne cible (forcément inversées, sinon ça serait solvé)
                                return (1, None)
                        if (up_x == target_column) or (down_x == target_column): # une des deux cases cibles est sur la colonne cible
                                if blank_x == target_column: # la case blanche est sur la colonne cible
                                        if up_x == target_column + 1 or  down_x == target_column + 1: # l'autre case cible est sur la colonne juste après
                                                if (up_x == target_column and up_y > blank_y) or (down_x == target_column and down_y < blank_y): # la case sur la colonne cible est bien placée
                                                        orientation = 2 if blank_y == grid_height - 1 else 3
                                                        return (orientation, None)
                                                else: # la case sur la colonne cible n'est pas bien placée
                                                        return (0, None)
                                        else: # l'autre case cible est sur la colonne dernière colonne
                                                if (up_x == target_column and up_y < blank_y) or (down_x == target_column and down_y > blank_y): # la case sur la colonne cible n'est pas bien placée
                                                        orientation = 2 if blank_y == grid_height - 1 else 3
                                                        return (orientation, None)
                                                else:
                                                        return (0, None) # la case sur la colonne cible est bien placée
                                if (up_y == target_up_y and up_x == target_column) or (down_y == target_down_y and down_x == target_column): # la case blanche n'est pas sur la colonne vide, une case est bien placée
                                        # la case blanche est sur la colonne suivante et n'est pas sur la même ligne, l'autre case n'est pas juste à côté
                                        if blank_x == target_column + 1 and \
                                           ((up_x == target_column and blank_y != up_y and (up_y != down_y or down_x != up_x + 1))\
                                           or (down_x == target_column and blank_y != down_y and (up_y != down_y or up_x != down_x + 1))):
                                                return (1, None)
                                        else: # la case blanche est sur la dernière colonne ou la case blanche est sur la même ligne ou l'autre case est juste à côté
                                                #TODO : find good rotate orientation
                                                first_index = up_target_index + 1
                                                last_index = first_index + grid_width + 1
                                                return (-1, (True, first_index, last_index))
                                else: # la case blanche n'est pas sur la colonne cible, la case sur la colonne cible n'est pas bien placée
                                        if blank_x == target_column + 1 and ((up_y == target_up_y and up_x == target_column + 1) or (down_y == target_down_y and down_x == target_column + 1)):
                                                return (1, None) # la case blanche est sur la colonne suivante et la case pas sur la bonne colonne est sur la bonne ligne
                                        else: # la case blanche est sur la dernière colonne ou la case pas sur la bonne colonne n'est pas sur la bonne ligne
                                                #TODO : find good rotate orientation
                                                first_index = up_target_index + 1
                                                last_index = first_index + grid_width + 1
                                                return (-1, (True, first_index, last_index))
                        else:
                                if blank_x == target_column and up_x == down_x: # aucune case n'est sur la bonne colonne et la case blanche est sur la colonne cible et les deux cases sont sur la même colonne
                                        return (0, None)
                                if blank_x < target_column + 2 and ((up_x == target_column + 2 and down_x < target_column + 2) or (up_x < target_column + 2 and down_x == target_column + 2)):
                                        orientation = True if up_x < target_column + 2 else False # la case blanche n'est pas sur la dernière colonne, une seule case est sur la dernière colonne
                                        first_index = up_target_index
                                        last_index = first_index + grid_width + 1
                                        return (-1, (orientation, first_index, last_index))
                                else:
                                        #TODO : find good rotate orientation
                                        first_index = up_target_index + 1
                                        last_index = first_index + grid_width + 1
                                        return (-1, (True, first_index, last_index))
                print('not ready yet')
                return (-1, None)

        def get_next_move_last_two_elements_in_line(self, array):
                print('not ready yet') # TODO : handle 2 cases -> elements need to be be put on the last two columns, or already at the right place
                return (-1, None)

        def get_next_move_common_case(self, array):
                print('not ready yet')
                return (-1, None)
                

        def get_next_move_brute_force(self, current_array):
                if get_key_from_array(current_array) not in self.shortest_ways:
                        self.shortest_ways = self.get_full_brute_force_solution(current_array)
                if get_key_from_array(current_array) in self.shortest_ways:
                        solution = self.shortest_ways[get_key_from_array(current_array)]
                        return self.get_next_move_from_solution(solution)
                print('bug : solution non trouvée')
                return -1

        def get_move_count_brute_force(self, current_array):
                if all(current_array[i] <= current_array[i+1] for i in range(len(current_array)-1)):
                        return 0
                if get_key_from_array(current_array) not in self.shortest_ways:
                        self.shortest_ways = self.get_full_brute_force_solution(current_array)
                if get_key_from_array(current_array) in self.shortest_ways:
                        solution = self.shortest_ways[get_key_from_array(current_array)]
                        return len(solution)
                print('bug : solution non trouvée')
                return -1

        def get_full_brute_force_solution(self, current_array):
                (grid_width, grid_height) = self.grid_size
                grid_length = grid_width * grid_height
                solved_array = list(range(grid_length))

                
                shortest_ways = self.shortest_ways
                if get_key_from_array(solved_array) in self.shortest_ways: # solution array not empty
                        current_list = []
                        for key in shortest_ways.keys():
                                temp_array = get_array_from_key(key)
                                current_list.append(temp_array)
                else: # starting from scratch
                        shortest_ways[get_key_from_array(solved_array)] = []
                        current_list = [solved_array] 
                solution_found = False
                
                while len(shortest_ways) < math.factorial(grid_length)/2 and not solution_found:
                        next_list = []
                        for array in current_list:
                                if solution_found:
                                        break
                                for i in range(4):
                                        new_array = self.update_array_with_direction_if_possible(array, i)
                                        if new_array == None:
                                                continue
                                        if get_key_from_array(new_array) not in shortest_ways:
                                                shortest_way = []
                                                for move in shortest_ways[get_key_from_array(array)]:
                                                        shortest_way.append(move)
                                                shortest_way.append(i)
                                                shortest_ways[get_key_from_array(new_array)] = shortest_way
                                                if get_key_from_array(current_array) == get_key_from_array(new_array):
                                                        solution_found = True
                                                        break
                                                next_list.append(new_array)
                        current_list = []
                        for element in next_list:
                                current_list.append(element)
                if solution_found:
                        return shortest_ways
                else:
                        return {}
        
        
        def update_array_with_direction_if_possible(self, array, direction, rotation = None):
                white_tile_index = -1
                new_array = list(range(len(array)))
                for index in range(len(array)):
                        new_array[index] = array[index]
                        if array[index] == len(array) - 1:
                                white_tile_index = index
                if white_tile_index == -1:
                        return None
                (grid_width, grid_height) = self.grid_size
                (white_tile_x, white_tile_y) = (white_tile_index % grid_width, white_tile_index // grid_width)
                if rotation != None:
                        (rotate_chrono, start_index, end_index) = rotation
                        (start_tile_x, start_tile_y) = (start_index % grid_width, start_index // grid_width)
                        (end_tile_x, end_tile_y) = (end_index % grid_width, end_index // grid_width)
                        if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == start_tile_y:
                                if rotate_chrono and white_tile_x != start_tile_x:
                                        direction = 1
                                if (not rotate_chrono) and white_tile_x != end_tile_x:
                                        direction = 0
                        if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == end_tile_y:
                                if rotate_chrono and white_tile_x != end_tile_x:
                                        direction = 0
                                if (not rotate_chrono) and white_tile_x != start_tile_x:
                                        direction = 1
                        if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == start_tile_x:
                                if rotate_chrono and white_tile_y != end_tile_y:
                                        direction = 3
                                if (not rotate_chrono) and white_tile_y != start_tile_y:
                                        direction = 2
                        if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == end_tile_x:
                                if rotate_chrono and white_tile_y != start_tile_y:
                                        direction = 2
                                if (not rotate_chrono) and white_tile_y != end_tile_y:
                                        direction = 3
                can_move = False
                if white_tile_x < grid_width - 1 and direction == 0:
                        can_move = True
                        new_array[white_tile_index] = new_array[white_tile_index + 1]
                        new_array[white_tile_index + 1] = len(array) - 1
                if white_tile_x > 0 and direction == 1:
                        can_move = True
                        new_array[white_tile_index] = new_array[white_tile_index - 1]
                        new_array[white_tile_index - 1] = len(array) - 1
                if white_tile_y > 0 and direction == 2:
                        can_move = True
                        new_array[white_tile_index] = new_array[white_tile_index - grid_width]
                        new_array[white_tile_index - grid_width] = len(array) - 1
                if white_tile_y < grid_height - 1 and direction == 3:
                        can_move = True
                        new_array[white_tile_index] = new_array[white_tile_index + grid_width]
                        new_array[white_tile_index + grid_width] = len(array) - 1
                if can_move:
                        return new_array
                else:
                        return None

        def get_next_move_from_solution(self, solution):
                if len(solution) == 0:
                        return -1
                elif solution[-1] == 0:
                        return 1
                elif solution[-1] == 1:
                        return 0
                elif solution[-1] == 2:
                        return 3
                elif solution[-1] == 3:
                        return 2


'''

grid_size = (3,2)
solver = Solver(grid_size)
permutations = get_all_permutations(grid_size)

#print(len(permutations))
count1 = 0
count2 = 0
count3 = 0
max_diff = 0
for array in permutations:
        move_count = solver.get_move_count_brute_force(array)
        move_count_algo = solver.get_move_count_algo(array)
        if move_count_algo == -1:
                count1 = count1 + 1
        elif move_count_algo != move_count:
                diff = move_count_algo - move_count
                if diff > max_diff:
                        max_diff = diff
                        print(array)
                        print((move_count_algo, move_count))
                count2 = count2 + 1
        else:
                count3 = count3 + 1
print(max_diff)

'''
