import os
from TaquinEntity.TaquinImage import *

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
