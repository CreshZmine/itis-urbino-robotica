import time

class Timer():
    def __init__(self):
        self.running = False
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def read(self):
        return time.time() - self.start_time

    def stop(self):
        self.running = False
        return self.read()
