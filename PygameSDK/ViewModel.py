class ViewModel:
    def __init__(self):
        self.should_update = False
        self.next_view = None
        self.should_return = False
        self.current_animation = None
            
    def updated(self):
        self.should_update = False
        
    def is_animating(self):
        return self.current_animation != None
        
    def update_animation(self):
        self.current_animation = None
        # Handle animation here
        
    def handle_code(self, code):
        print(code)
        # Handle events here
