class AutoClicker:
    def __init__(self):
        self.clicking = False

    def start_clicking(self):
        self.clicking = True
        # Logic to start clicking goes here

    def stop_clicking(self):
        self.clicking = False
        # Logic to stop clicking goes here

    def is_clicking(self):
        return self.clicking