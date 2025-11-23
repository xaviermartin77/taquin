import pygame
from taquinConstants import *


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
