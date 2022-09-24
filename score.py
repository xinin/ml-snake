import os

class Score:

    def __init__(self, folder, snake_number):
        self.score = 0
        self.score_folder = folder
        self.snake_number = snake_number
        return

    def add_score(self,points, display=True):
            self.score += points
            

    def reset(self):
        self.score = 0
