import random

class Food:
    def __init__(self):
        return
     
    def generate(max_width,max_height, size):
        foodx = round(random.randrange(0, max_width - size) / 10.0) * 10.0
        foody = round(random.randrange(0, max_height - size) / 10.0) * 10.0
        return [foodx, foody]
    