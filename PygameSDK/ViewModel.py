class ViewModel:
    def __init__(self):
        self.should_update = True
        self.next_view = None
            
    def updated(self):
        self.should_update = False
        
    def handle_code(self, code):
        print(code)
        # Handle events here
