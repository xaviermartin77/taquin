import os
from PygameSDK.ImageRessourceProvider import *

class TaquinImage:
    def __init__(self, path):
        self.file_path = path
        self.image_provider = ImageRessourceProvider()
        self.image_ressource = None
        self.image_size = None
        
    def load_image_ressource(self, view_size, adjustement_size):
        (self.image_ressource, self.image_size) = self.image_provider.get_image_surface(self.file_path, view_size, True, adjustement_size)
    
    def unload_image_ressource(self):
        self.image_ressource = None
        self.image_size = None
