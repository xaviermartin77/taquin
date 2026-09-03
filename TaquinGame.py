from TaquinImagesScreen import *
from TaquinImagesViewModel import *
from PygameSDK.Game import *


view_model = TaquinImagesViewModel()
screen_size = (1500, 1000)
screen = TaquinImagesScreen(view_model, screen_size)
game = Game()
game.start_game(screen)

