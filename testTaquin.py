'''
import pygame
from pygame.locals import *
from taquinConstants import *
from taquinImages import *
from taquinGame import *
from taquinUI import *


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
from TaquinImagesView import *
from TaquinImagesViewModel import *
from PygameSDK.Game import *


view_model = TaquinImagesViewModel()
screen_size = (1500, 1000)
view = TaquinImagesView(view_model, screen_size)
game = Game()
game.start_game(view)


'''

TODO
1) image list -> Done

2) game grid
créer le VM et la view, gérer la transition, récupérer les règles métiers
  interface : background color (merge), show/hide score + time, show/hide hint + figures, shuffle, return
  grid : move tile (4 directions), rotate
  display : display_game_interface, show_fullscreen_image, display_all_tiles (warning : animation)
créer les entity : game grid -> Done (à améliorer)
mettre à jour le SDK : long press -> Done, animations

3) clean
virer les utils, les constants, les methodes UI, les VMs, garder uniquement le solver
'''
