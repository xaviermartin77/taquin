class Color:
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    orange = (255,128,0)
    violet = (128,0,255)
    yellow = (255,255,0)
    grey = (128,128,128)
    
    color_list = ['w', 'j', 'b', 'r', 'g', 'p', 'v', 'o']

    def __init__(self, code):
        self.color_code = code
    
    def get_color_value(self):
        if self.color_code == 'w':
            return Color.white
        if self.color_code == 'r':
            return Color.red
        if self.color_code == 'b':
            return Color.blue
        if self.color_code == 'v':
            return Color.green
        if self.color_code == 'o':
            return Color.orange
        if self.color_code == 'p':
            return Color.violet
        if self.color_code == 'j':
            return Color.yellow
        if self.color_code == 'g':
            return Color.grey
        if self.color_code == 'n':
            return Color.black
        return None
