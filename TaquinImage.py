import os
from PygameSDK.ImageView import *

class TaquinImageProvider:
    def generate_default_images(self):
        file_exist = True
        file_count = 1
        file_list = []
        while file_exist:
            file_name = 'images/image' + str(file_count) + '.jpg'
            if os.path.isfile(file_name):
                new_image = TaquinImage(file_name)
                file_list.append(new_image)
                file_count = file_count + 1
            else:
                file_exist = False
        return file_list
        
    def generate_json_images(self, json_path):
        print('generating images using json file')

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
