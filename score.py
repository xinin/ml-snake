class Score:

    def __init__(self):
        self.score = 0
        return

    def add_score(self,points, display=True):
            self.score += points

    def reset(self):
        self.score = 0

    