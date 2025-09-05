# Python program to read 
# image using PIL module 
  
# importing PIL 
import math 
from PIL import Image, ImageDraw
import pygame
from pygame.locals import *
import random
import os

MAX_WIDTH = 1900
MAX_HEIGHT = 960
INTERFACE_BIG_WIDTH = 400
INTERFACE_WIDTH = 100
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

# récupérer les images, à garder en static, maybe mettre un fichier de config, maybe faire un tableau d'id plutôt que d'images
def generate_all_images(screen_size, image_list_size):
        (screen_width, screen_height) = screen_size
        (image_list_width, image_list_height) = image_list_size
        file_exist = True
        file_count = 1
        file_list = []
        while file_exist:
                file_name = 'images/image' + str(file_count) + '.jpg'
                if os.path.isfile(file_name):
                        temp_image = pygame.image.load(file_name)
                        temp_image = pygame.transform.scale(temp_image, (int(screen_width/image_list_width), int(screen_height/image_list_height)))
                        file_list.append(temp_image)
                        file_count = file_count + 1
                else:
                        file_exist = False
        return file_list

# static, tool pour connaitre la taille d'une image dans le menu principal (utile pour le click handler)
def get_small_image_size(screen_size, image_list_size):
        (screen_width, screen_height) = screen_size
        (image_list_width, image_list_height) = image_list_size
        return (int(screen_width/image_list_width), int(screen_height/image_list_height))

# static, génère les infos pour la gestion des inputs du click pendant la sélection de l'image
def generate_click_handler_data_for_main_vm(screen_size):
        (screen_width, screen_height) = screen_size
        interface_start = screen_width
        interface_center = screen_width + (INTERFACE_BIG_WIDTH / 2)
        interface_end = screen_width + INTERFACE_BIG_WIDTH
        input_data = []
        input_data.append((0, interface_start, 0, screen_height, 'select_image'))
        input_data.append((interface_start, interface_center, 0, screen_height / 3, 'decrement_width'))
        input_data.append((interface_center, interface_end, 0, screen_height / 3, 'increment_width'))
        input_data.append((interface_start, interface_center, screen_height / 3, screen_height * 2 / 3, 'decrement_height'))
        input_data.append((interface_center, interface_end, screen_height / 3, screen_height * 2 / 3, 'increment_height'))
        input_data.append((interface_start, interface_end, screen_height * 2 / 3, screen_height, 'start_game'))
        return input_data

#static, génère les infos pour la gestion des inputs du click pendant le jeu
def generate_click_handler_data_for_game_vm(screen_size):
        (screen_width, screen_height) = screen_size
        interface_start = screen_width
        interface_end = screen_width + INTERFACE_WIDTH
        input_data = []
        input_data.append((0, interface_start, 0, screen_height, 'select_tile'))
        input_data.append((interface_start, interface_end, 0, screen_height / 5, 'first_button'))
        input_data.append((interface_start, interface_end, screen_height / 5, screen_height * 2 / 5, 'second_button'))
        input_data.append((interface_start, interface_end, screen_height * 2 / 5, screen_height * 3 / 5, 'show_score'))
        input_data.append((interface_start, interface_end, screen_height * 3 / 5, screen_height * 4 / 5, 'show_time'))
        input_data.append((interface_start, interface_end, screen_height * 4 / 5, screen_height * 21 / 25, 'background_white'))
        input_data.append((interface_start, interface_end, screen_height * 21 / 25, screen_height * 22 / 25, 'background_black'))
        input_data.append((interface_start, interface_end, screen_height * 22 / 25, screen_height * 23 / 25, 'background_red'))
        input_data.append((interface_start, interface_end, screen_height * 23 / 25, screen_height * 24 / 25, 'background_blue'))
        input_data.append((interface_start, interface_end, screen_height * 24 / 25, screen_height, 'background_green'))
        return input_data

#static, génère les infos pour la gestion des inputs du clavier pendant le jeu
def generate_shortcut_handler_data_for_game_vm():
        input_data = []
        input_data.append((pygame.K_r, 'rotate_chrono'))
        input_data.append((pygame.K_t, 'rotate_trigo'))
        input_data.append((pygame.K_LEFT, 'move_left'))
        input_data.append((pygame.K_RIGHT, 'move_right'))
        input_data.append((pygame.K_DOWN, 'move_down'))
        input_data.append((pygame.K_UP, 'move_up'))
        input_data.append((pygame.K_s, 'solve_algo'))
        input_data.append((pygame.K_b, 'solve_brute'))
        return input_data

# static, récupère l'image à partir de son index
def generate_full_screen_image(image_index, grid_size):
        image = pygame.image.load('images/image' + str(image_index+1) + '.jpg')
        image = pygame.transform.scale(image, get_full_screen_image_size(image.get_width(), image.get_height(), grid_size))
        return image

# static, calcule la taille de l'image par rapport à l'écran
def get_full_screen_image_size(imageWidth, imageHeight, grid_size):
        (grid_width, grid_height) = grid_size
        screen_width = min(MAX_WIDTH - INTERFACE_WIDTH, imageWidth)
        screen_height = screen_width * imageHeight / imageWidth
        if screen_height > MAX_HEIGHT:
                screen_height = min(MAX_HEIGHT, imageHeight)
                screen_width = screen_height * imageWidth / imageHeight
        adjusted_screen_width = int(screen_width) - int(screen_width)%grid_width
        adjusted_screen_height = int(screen_height) - int(screen_height)%grid_height
        return int(adjusted_screen_width), int(adjusted_screen_height)

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

# method UI, affiche l'image de la tuile sur l'écran (screen), attention au move (utilisé pour le mouvement des tuiles)
def display_tile_image(screen, image, tile_info):
        (tile_coordinates, tile_size_square_to_display, text_to_display, text_center_coordinates) = tile_info
        display_image(screen, image, tile_coordinates, tile_size_square_to_display)
        if (text_to_display != ''):
                display_text(screen, text_to_display, text_center_coordinates, True, red)

# method UI, affiche toutes les tuiles, sur méthode de displayTileImage (progress -> move)
def display_all_tiles(screen, image, tile_info_grid): 
        for tile_info in tile_info_grid:
                display_tile_image(screen, image, tile_info)

# method UI, affiche l'image sur l'écran
def display_image(screen, image, image_coordinates, image_zone):
        screen.blit(image, image_coordinates, image_zone)

# method UI, affiche un texte sur l'écran
def display_text(screen, text_to_display, text_center_coordinates, is_big_font, color):
        font = pygame.font.SysFont('arial', 50, False, False) if is_big_font else pygame.font.SysFont('arial', 20, False, False)
        textSurface = font.render(text_to_display, True, color)
        textRect = textSurface.get_rect()
        textRect.center = text_center_coordinates
        screen.blit(textSurface, textRect)
        
# method UI, affiche toutes les images à sélectionner, avec une taille custom (en x et en y)
def display_all_images_to_select(screen, image_list, image_list_size):
        (image_list_width, image_list_height) = image_list_size
        screen_width = screen.get_width() - INTERFACE_BIG_WIDTH
        screen_height = screen.get_height()
        image_width = screen_width/image_list_width
        image_height = screen_height/image_list_height
        for index, image in enumerate(image_list):
                (x,y) = (index % image_list_width, index // image_list_width)
                image_coordinates = (x*screen_width/image_list_width, y*screen_height/image_list_height)
                image_zone = (0, 0, screen_width/image_list_width, screen_height/image_list_height)
                display_image(screen, image, image_coordinates, image_zone)

# method UI, montre l'image complète (pour l'indice et quand le jeu est terminé)
def show_fullscreen_image(screen, image):
        screen.blit(image, (0,0))

# method UI, affiche l'interface pendant le jeu (indice, redémarrer, score, temps, couleur du fond)
# to add : back, solve, shortcuts
def display_game_interface(screen, showing_score, score, showing_time, time, solved):
        interface_start = screen.get_width() - INTERFACE_WIDTH
        interface_center = screen.get_width() - (INTERFACE_WIDTH / 2)
        interface_end = screen.get_width()

        first_text = 'Menu' if solved else 'Hint'
        display_text(screen, first_text, (interface_center, screen.get_height() / 10), False, black)

        pygame.draw.line(screen, black, (interface_start, screen.get_height()/5), (interface_end, screen.get_height()/5))

        second_text = 'Restart' if solved else 'Figures'
        display_text(screen, second_text, (interface_center, screen.get_height() * 3 / 10), False, black)

        pygame.draw.line(screen, black, (interface_start, 2*screen.get_height()/5), (interface_end, 2*screen.get_height()/5))

        score_text = 'Score'
        if showing_score:
                score_text = str(score)
        display_text(screen, score_text, (interface_center, screen.get_height() * 5 / 10), False, black)

        pygame.draw.line(screen, black, (interface_start, 3*screen.get_height()/5), (screen.get_width(), 3*screen.get_height()/5))

        time_text = 'Time'
        if showing_time:
                time_text = str(time)
        display_text(screen, time_text, (interface_center, screen.get_height() * 7 / 10), False, black)

        pygame.draw.line(screen, black, (interface_start, 4*screen.get_height()/5-1), (screen.get_width(), 4*screen.get_height()/5-1))
        
        screen.fill(white, (interface_start, screen.get_height() * 4 / 5, interface_end, screen.get_height() * 21 / 25))
        screen.fill(black, (interface_start, screen.get_height() * 21 / 25, interface_end, screen.get_height() * 22 /25))
        screen.fill(red, (interface_start, screen.get_height() * 22 / 25, interface_end, screen.get_height() * 23 /25))
        screen.fill(blue, (interface_start, screen.get_height() * 23 / 25, interface_end, screen.get_height() * 24 /25))
        screen.fill(green, (interface_start, screen.get_height() * 24 / 25, interface_end, screen.get_height()))

# method UI, encadre une zone avec des traits
def draw_square(screen, square_coordinates, color):
        (left, right, top, bottom) = square_coordinates
        pygame.draw.line(screen, red, (left, top), (right, top))
        pygame.draw.line(screen, red, (left, bottom), (right, bottom))
        pygame.draw.line(screen, red, (left, top), (left, bottom))
        pygame.draw.line(screen, red, (right, top), (right, bottom))


# method UI, affiche l'interface avant le jeu (image sélectionnée, nombre de tuiles longueur et largeut, démarrer)
# to add : hint, stats
def display_start_interface(screen, selected_image_index, grid_size, image_list_size):
        (grid_width, grid_height) = grid_size
        (image_list_width, image_list_height) = image_list_size

        if selected_image_index != -1:
                index_x = selected_image_index % image_list_width
                index_y = selected_image_index // image_list_width
                screen_width = screen.get_width() - INTERFACE_BIG_WIDTH
                screen_height = screen.get_height()
                image_width = screen_width/image_list_width
                image_height = screen_height/image_list_height
                selected_image_square = (index_x * image_width, (index_x + 1) * image_width, index_y * image_height, (index_y + 1) * image_height)
                draw_square(screen, selected_image_square, red)

        interface_start = screen.get_width() - INTERFACE_BIG_WIDTH
        interface_left = screen.get_width() - (INTERFACE_BIG_WIDTH * 3 / 4)
        interface_center = screen.get_width() - (INTERFACE_BIG_WIDTH / 2)
        interface_right = screen.get_width() - (INTERFACE_BIG_WIDTH / 4)
        interface_end = screen.get_width()
        
        display_text(screen, 'Width', (interface_center, screen.get_height()/6 - 40), True, black)
        display_text(screen, str(grid_width), (interface_center, screen.get_height()/6 + 40), True, black)
        minus_text_for_width = '-' if grid_width > 2 else ''
        display_text(screen, minus_text_for_width, (interface_left, screen.get_height()/6 + 40), True, black)
        plus_text_for_width = '+' if grid_width < 20 else ''
        display_text(screen, plus_text_for_width, (interface_right, screen.get_height()/6 + 40), True, black)
        
        pygame.draw.line(screen, black, (interface_start, screen.get_height()/3), (interface_end, screen.get_height()/3))
        
        display_text(screen, 'Height', (interface_center, 3*screen.get_height()/6 - 40), True, black)
        display_text(screen, str(grid_height), (interface_center, 3*screen.get_height()/6 + 40), True, black)
        minus_text_for_height = '-' if grid_height > 2 else ''
        display_text(screen, minus_text_for_height, (interface_left, 3*screen.get_height()/6 + 40), True, black)
        plus_text_for_height = '+' if grid_height < 20 else ''
        display_text(screen, plus_text_for_height, (interface_right, 3*screen.get_height()/6 + 40), True, black)

        pygame.draw.line(screen, black, (screen.get_width() - INTERFACE_BIG_WIDTH, 2*screen.get_height()/3), (screen.get_width(), 2*screen.get_height()/3))

        display_text(screen, 'Start', (interface_center, 5*screen.get_height()/6), True, black)


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
                
                

class ImagesViewModel:
        def __init__(self, screen_size, image_list_size):
                self.image_list = generate_all_images(screen_size, image_list_size)
                self.image_list_size = image_list_size
                self.image_square_size = get_small_image_size(screen_size, image_list_size)
                self.click_handler_data = generate_click_handler_data_for_main_vm(screen_size)
                self.first_list_index = 0
                self.is_game_preparing = False
                self.game_running = False
                self.grid_width = 3
                self.grid_height = 3
                self.selected_image_index = 0

        def scroll_up(self):
                self.first_list_index = self.first_list_index - self.image_list_size[0] if self.first_list_index - self.image_list_size[0] >= 0 else 0

        def scroll_down(self):
                image_list_length = self.image_list_size[0] * self.image_list_size[1]
                self.first_list_index = self.first_list_index + self.image_list_size[0] if self.first_list_index + image_list_length < len(self.image_list) else self.first_list_index

        def select_index(self, position):
                if position + self.first_list_index < len(self.image_list):
                        self.selected_image_index = position + self.first_list_index
        
        def get_selected_image_index(self):
                return self.selected_image_index
        
        def get_selected_image_position(self):
                image_list_length = self.image_list_size[0] * self.image_list_size[1]
                if self.selected_image_index >= self.first_list_index and self.selected_image_index < self.first_list_index + image_list_length:
                        return self.selected_image_index - self.first_list_index
                return -1

        def get_image_at_position(self, position):
                if (position + self.first_list_index) >= len(self.image_list):
                        return None
                return self.image_list[position + self.first_list_index]

        def get_images_displayed_list(self):
                (image_list_width, image_list_height) = self.image_list_size
                image_list_length = image_list_width * image_list_height
                result = []
                
                for position in range(image_list_length):
                        if (position + self.first_list_index) >= len(self.image_list):
                                continue
                        result.append(self.get_image_at_position(position))
                return result

        def get_image_list_size(self):
                return self.image_list_size

        def prepare_for_start(self):
                self.is_game_preparing = True

        def start_game(self):
                # TODO : set screen size (adapt it to image shape)
                self.game_running = True
                self.is_game_preparing = False

        def quit_game(self):
                # TODO : set screen size (return to normal shape)
                self.game_running = False

        def should_start_game(self):
                return self.is_game_preparing

        def is_game_running(self):
                return self.game_running

        def decrement_grid_width(self):
                self.grid_width = self.grid_width - 1 if self.grid_width > 2 else self.grid_width

        def increment_grid_width(self):
                self.grid_width = self.grid_width + 1 if self.grid_width < 20 else self.grid_width

        def decrement_grid_height(self):
                self.grid_height = self.grid_height - 1 if self.grid_height > 2 else self.grid_height

        def increment_grid_height(self):
                self.grid_height = self.grid_height + 1 if self.grid_height < 20 else self.grid_height

        def get_grid_size(self):
                return (self.grid_width, self.grid_height)

        def get_code_for_click(self, pos):
                for handler in self.click_handler_data:
                        (x_start, x_end, y_start, y_end, code) = handler
                        if pos[0] > x_start and pos[0] < x_end and pos[1] > y_start and pos[1] < y_end:
                                return code
                return 'none'

        def handle_click(self, pos):
                handler_code = self.get_code_for_click(pos)
                if handler_code == 'select_image':
                        (image_width, image_height) = self.image_square_size
                        index_x = int(pos[0] // image_width)
                        index_y = int(pos[1] // image_height)
                        self.select_index(index_x + self.image_list_size[0] * index_y)
                elif handler_code == 'decrement_width':
                        self.decrement_grid_width()
                elif handler_code == 'increment_width':
                        self.increment_grid_width()
                elif handler_code == 'decrement_height':
                        self.decrement_grid_height()
                elif handler_code == 'increment_height':
                        self.increment_grid_height()
                elif handler_code == 'start_game':
                        self.prepare_for_start()
                
                

class GameViewModel:
        def __init__(self, image_index, grid_size):
                selected_image = generate_full_screen_image(image_index, grid_size)
                self.full_screen_image = selected_image
                self.grid_size = grid_size
                self.firstListIndex = 0
                self.tile_size = (selected_image.get_width()/grid_size[0], selected_image.get_height()/grid_size[1])
                self.click_handler_data = generate_click_handler_data_for_game_vm((selected_image.get_width(), selected_image.get_height()))
                self.shortcut_handler_data = generate_shortcut_handler_data_for_game_vm()
                self.is_game_leaving = False
                
                self.background_color = white
                
                self.start_ticks = 0
                self.final_time = 0
                self.seconds = 0
                self.move_count = 0
                
                self.is_showing_hint = False
                self.is_showing_figures = False
                self.is_showing_score = True
                self.is_showing_time = True

                self.current_array = get_random_array(grid_size) #[1, 4, 2, 3, 5, 0]
                self.current_movement = (0, 0, 0) # progress, tile, target
                self.solver = Solver(grid_size)

        def get_game_screen_size(self):
                return (self.full_screen_image.get_width() + INTERFACE_WIDTH, self.full_screen_image.get_height())

        def get_game_screen_square(self):
                return (0, 0, self.full_screen_image.get_width(), self.full_screen_image.get_height())

        def get_full_screen_image(self):
                return self.full_screen_image

        def shuffle(self):
                self.start_ticks = 0
                self.final_time = 0
                self.seconds = 0
                self.move_count = 0        
                self.current_array = get_random_array(grid_size)
                self.current_movement = (0, 0, 0)

        def start_showing_hint(self):
                self.is_showing_hint = True

        def stop_showing_hint(self):
                self.is_showing_hint = False

        def should_show_hint(self):
                return self.is_showing_hint

        def start_showing_figures(self):
                self.is_showing_figures = True

        def stop_showing_figures(self):
                self.is_showing_figures = False

        def should_show_figures(self):
                return self.is_showing_figures

        def switch_showing_score(self):
                self.is_showing_score = not self.is_showing_score

        def should_show_score(self):
                return self.is_showing_score

        def switch_showing_time(self):
                self.is_showing_time = not self.is_showing_time

        def should_show_time(self):
                return self.is_showing_time

        def select_background_color(self, color):
                self.background_color = color

        def get_background_color(self):
                return self.background_color

        def increment_move_count(self):
                self.move_count = self.move_count + 1

        def get_move_count(self):
                return self.move_count

        def check_if_grid_is_solved(self):
                if self.is_game_solved() and self.final_time == 0 and self.start_ticks>0:
                        self.final_time = pygame.time.get_ticks() - self.start_ticks

        def get_time_to_display(self):
                return (self.final_time if self.is_game_solved() else (pygame.time.get_ticks() - self.start_ticks if self.start_ticks > 0 else 0)) // 1000

        def is_game_solved(self):
                return all(self.current_array[i] <= self.current_array[i+1] for i in range(len(self.current_array)-1))

        def is_tile_moving(self):
                return self.current_movement[0] != 0

        def is_white_tile(self, tile_index):
                return self.current_array[tile_index] == len(self.current_array) - 1

        def get_white_tile_index(self):
                for index in range(len(self.current_array)):
                        if self.is_white_tile(index):
                                return index
                return -1
        
        def move_with_direction_if_possible(self, direction):
                white_tile_index = self.get_white_tile_index()
                (white_tile_x, white_tile_y) = self.get_coordinates_from_index(white_tile_index)
                (grid_width, grid_height) = self.grid_size
                
                if white_tile_x < grid_width - 1 and direction == 0:
                        # move left
                        self.start_moving(white_tile_index + 1, white_tile_index)
                if white_tile_x > 0 and direction == 1:
                        # move right
                        self.start_moving(white_tile_index - 1, white_tile_index)
                if white_tile_y > 0 and direction == 2:
                        # move down
                        self.start_moving(white_tile_index - grid_width, white_tile_index)
                if white_tile_y < grid_height - 1 and direction == 3:
                        # move up
                        return self.start_moving(white_tile_index + grid_width, white_tile_index)

        def rotate_if_possible(self, rotate_chrono, start_index = 0, end_index = -1):
                if end_index == -1:
                        end_index = len(self.current_array) - 1
                white_tile_index = self.get_white_tile_index()
                (white_tile_x, white_tile_y) = self.get_coordinates_from_index(white_tile_index)
                (start_tile_x, start_tile_y) = self.get_coordinates_from_index(start_index)
                (end_tile_x, end_tile_y) = self.get_coordinates_from_index(end_index)
                
                if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == start_tile_y:
                        if rotate_chrono and white_tile_x != start_tile_x:
                                self.move_with_direction_if_possible(1)
                        if (not rotate_chrono) and white_tile_x != end_tile_x:
                                self.move_with_direction_if_possible(0)
                if white_tile_x >= start_tile_x and white_tile_x <= end_tile_x and white_tile_y == end_tile_y:
                        if rotate_chrono and white_tile_x != end_tile_x:
                                self.move_with_direction_if_possible(0)
                        if (not rotate_chrono) and white_tile_x != start_tile_x:
                                self.move_with_direction_if_possible(1)
                if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == start_tile_x:
                        if rotate_chrono and white_tile_y != end_tile_y:
                                self.move_with_direction_if_possible(3)
                        if (not rotate_chrono) and white_tile_y != start_tile_y:
                                self.move_with_direction_if_possible(2)
                if white_tile_y >= start_tile_y and white_tile_y <= end_tile_y and white_tile_x == end_tile_x:
                        if rotate_chrono and white_tile_y != start_tile_y:
                                self.move_with_direction_if_possible(2)
                        if (not rotate_chrono) and white_tile_y != end_tile_y:
                                self.move_with_direction_if_possible(3)

        def move_tile_if_possible(self, position):
                tile_index = self.get_tile_index_from_position(position)
                if tile_index != -1:
                        target_tile_index = self.get_target_index_from_tile(tile_index)
                        if target_tile_index != -1:
                                self.start_moving(tile_index, target_tile_index)
                        

        def get_tile_index_from_position(self, position):
                (x, y) = position
                (tile_width, tile_height) = self.tile_size
                (grid_width, grid_height) = self.grid_size
                for i in range(grid_width):
                        for j in range(grid_height):
                                if x >= tile_width*i and x < tile_width*(i+1) and y >= tile_height*j and y < tile_height*(j+1):
                                        return j*grid_width + i
                return -1
                        

        def get_coordinates_from_index(self, index):
                grid_width = self.grid_size[0]
                return index % grid_width, index // grid_width

        def get_target_index_from_tile(self, tile_index):
                (grid_width, grid_height) = self.grid_size
                if self.is_white_tile(tile_index):
                        return -1
                (i, j) = self.get_coordinates_from_index(tile_index)
                if i > 0 and self.is_white_tile(tile_index - 1):
                        return tile_index - 1
                if i < grid_width - 1 and self.is_white_tile(tile_index + 1):
                        return tile_index + 1
                if j > 0 and self.is_white_tile(tile_index - grid_width):
                        return tile_index - grid_width
                if j < grid_height - 1 and self.is_white_tile(tile_index + grid_width):
                        return tile_index + grid_width
                return -1

        def get_current_move_step_size(self):
                if not self.is_tile_moving():
                        return 0
                (progress, tile_index, target_tile_index) = self.current_movement
                grid_width = self.grid_size[0]
                (tile_width, tile_height) = self.tile_size
                if tile_index == target_tile_index - 1:
                        return tile_width/10
                if tile_index == target_tile_index + 1:
                        return -tile_width/10
                if tile_index == target_tile_index - grid_width:
                        return tile_height/10
                if tile_index == target_tile_index + grid_width:
                        return -tile_height/10

        def get_current_move_state_for_tile(self, tile_index_to_check):
                if not self.is_tile_moving() :
                        return (0, 0)
                (progress, tile_index, target_tile_index) = self.current_movement
                if tile_index != tile_index_to_check:
                        return (0, 0)
                grid_width = self.grid_size[0]
                if tile_index == target_tile_index - 1 or tile_index == target_tile_index + 1:
                        return (progress, 0)
                if tile_index == target_tile_index - grid_width or tile_index == target_tile_index + grid_width:
                        return (0, progress)
                return (0, 0)

        def start_moving(self, tile_index, target_tile_index):
                if self.is_game_solved():
                        return
                if self.start_ticks == 0:
                        self.start_ticks = pygame.time.get_ticks()
                self.move_count = self.move_count + 1
                first_progress = 1 if tile_index < target_tile_index else -1
                self.current_movement = (first_progress, tile_index, target_tile_index)

        def increment_progress_if_needed(self):
                if not self.is_tile_moving():
                        return
                (progress, tile_index, target_tile_index) = self.current_movement
                new_progress = progress + self.get_current_move_step_size()
                (tile_width, tile_height) = self.tile_size
                grid_width = self.grid_size[0]
                movement_completed = \
                        (tile_index == target_tile_index - 1 and new_progress >= tile_width) \
                        or (tile_index == target_tile_index + 1 and new_progress <= -tile_width) \
                        or (tile_index == target_tile_index - grid_width and new_progress >= tile_height) \
                        or (tile_index == target_tile_index + grid_width and new_progress <= -tile_height)
                if movement_completed:
                        self.grid_size
                        self.current_array[target_tile_index] = self.current_array[tile_index]
                        self.current_array[tile_index] = len(self.current_array) - 1
                        self.current_movement = (0, 0, 0)
                else:
                        self.current_movement = (new_progress, tile_index, target_tile_index)

        def get_tile_info_grid(self):
                (tile_width, tile_height) = self.tile_size
                result = []
                for index, tile_value in enumerate(self.current_array):
                        if self.is_white_tile(index) and not self.is_game_solved():
                                continue
                        
                        (x_position_on_screen, y_position_on_screen) = self.get_coordinates_from_index(index)
                        (x_move_value, y_move_value) = self.get_current_move_state_for_tile(index)
                        tile_coordinates = (x_position_on_screen * tile_width + x_move_value, y_position_on_screen * tile_height + y_move_value)
                        
                        (x_position_on_image, y_position_on_image) = self.get_coordinates_from_index(tile_value)
                        tile_size_square_to_display = (x_position_on_image * tile_width, y_position_on_image * tile_height, tile_width, tile_height)
                        
                        text = (str(tile_value + 1)) if self.is_showing_figures else ''
                        text_center_coordinates = (x_position_on_screen * tile_width + x_move_value + tile_width/2, y_position_on_screen * tile_height + y_move_value + tile_height/2)

                        result.append((tile_coordinates, tile_size_square_to_display, text, text_center_coordinates))
                return result

        def get_code_for_click(self, pos):
                for handler in self.click_handler_data:
                        (x_start, x_end, y_start, y_end, code) = handler
                        if pos[0] > x_start and pos[0] < x_end and pos[1] > y_start and pos[1] < y_end:
                                return code
                return 'none'

        def handle_click(self, pos):
                handler_code = self.get_code_for_click(pos)
                if handler_code == 'select_tile':
                        self.move_tile_if_possible(pos)
                if handler_code == 'first_button':
                        if self.is_game_solved():
                                self.prepare_for_leaving()
                        else:
                                self.start_showing_hint()
                elif handler_code == 'second_button':
                        if self.is_game_solved():
                                self.shuffle()
                        else:
                                self.start_showing_figures()
                elif handler_code == 'show_score':
                        self.switch_showing_score()
                elif handler_code == 'show_time':
                        self.switch_showing_time()
                elif handler_code == 'background_white':
                        self.select_background_color(white)
                elif handler_code == 'background_black':
                        self.select_background_color(black)
                elif handler_code == 'background_red':
                        self.select_background_color(red)
                elif handler_code == 'background_blue':
                        self.select_background_color(blue)
                elif handler_code == 'background_green':
                        self.select_background_color(green)
        
        def prepare_for_leaving(self):
                self.is_game_leaving = True

        def should_leave_game(self):
                # TODO : dealloc / deactivate params if needed
                return self.is_game_leaving

        def get_code_for_key(self, key):
                for handler in self.shortcut_handler_data:
                        (key_id, code) = handler
                        if key == key_id:
                                return code
                return 'none'

        def handle_shortcut(self, key):
                handler_code = self.get_code_for_key(key)
                if handler_code == 'rotate_chrono':
                       self.rotate_if_possible(True)
                elif handler_code == 'rotate_trigo':
                       self.rotate_if_possible(False)
                elif handler_code == 'move_left':
                       self.move_with_direction_if_possible(0)
                elif handler_code == 'move_right':
                       self.move_with_direction_if_possible(1)
                elif handler_code == 'move_down':
                       self.move_with_direction_if_possible(2)
                elif handler_code == 'move_up':
                       self.move_with_direction_if_possible(3)
                elif handler_code == 'solve_algo':
                       self.solve_algo()
                elif handler_code == 'solve_brute':
                       self.solve_brute_force()

        def solve_brute_force(self):
                next_move = self.solver.get_next_move_brute_force(self.current_array)
                if next_move != -1:
                        self.move_with_direction_if_possible(next_move)

        def solve_algo(self):
                (next_move, rotation) = self.solver.get_next_move_algo(self.current_array)
                if next_move != -1:
                        self.move_with_direction_if_possible(next_move)
                if rotation != None:
                        (rotate_chrono, start_index, end_index) = rotation
                        self.rotate_if_possible(rotate_chrono, start_index, end_index)

# TODO : factorizer les méthodes get UI (tap handler), les variables d'état (dans les classes), ne garder que l'essentiel (ecran, loop)
def playGame():
        pygame.init()
        ecran = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
        #BIG_FONT = pygame.font.SysFont('arial', 50, False, False)
        #SMALL_FONT = pygame.font.SysFont('arial', 20, False, False)
        
        main_view_model = ImagesViewModel((MAX_WIDTH - INTERFACE_BIG_WIDTH, MAX_HEIGHT), (3, 4))
        
        pygame.display.flip()
        loop = True
        
        while loop:
                for event in pygame.event.get():
                        if main_view_model.is_game_running():
                                if game_view_model.is_tile_moving():
                                        continue
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        game_view_model.handle_click(pygame.mouse.get_pos())
                                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                        game_view_model.stop_showing_hint()
                                        game_view_model.stop_showing_figures()
                                if event.type == pygame.KEYDOWN:
                                        game_view_model.handle_shortcut(event.key)

                        else: 
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                                        main_view_model.scroll_up()
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                                        main_view_model.scroll_down()
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        main_view_model.handle_click(pygame.mouse.get_pos())
                        if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): 
                                        loop = False

                ecran.fill(white)
                                
                if main_view_model.is_game_running():
                        if game_view_model.should_leave_game():
                                ecran = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
                                main_view_model.quit_game()
                        else:
                                ecran.fill(game_view_model.get_background_color(), game_view_model.get_game_screen_square())
                                game_view_model.check_if_grid_is_solved()
                                display_game_interface(ecran, game_view_model.should_show_score(), game_view_model.get_move_count(), game_view_model.should_show_time(), game_view_model.get_time_to_display(), game_view_model.is_game_solved())
                                if game_view_model.should_show_hint() or game_view_model.is_game_solved():
                                        show_fullscreen_image(ecran, game_view_model.get_full_screen_image())
                                else:
                                        display_all_tiles(ecran, game_view_model.get_full_screen_image(), game_view_model.get_tile_info_grid())
                                        game_view_model.increment_progress_if_needed()

                else:
                        if main_view_model.should_start_game():
                                game_view_model = GameViewModel(main_view_model.get_selected_image_index(), main_view_model.get_grid_size())
                                ecran = pygame.display.set_mode(game_view_model.get_game_screen_size())
                                
                                main_view_model.start_game()
                        else:
                                display_all_images_to_select(ecran, main_view_model.get_images_displayed_list(), main_view_model.get_image_list_size())
                                display_start_interface(ecran, main_view_model.get_selected_image_position(), main_view_model.get_grid_size(), main_view_model.get_image_list_size())
                pygame.display.update()
        pygame.quit()

playGame()

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

