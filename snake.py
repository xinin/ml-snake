class Snake:

    SNAKE_BLOCK = 10
    SNAKE_SPEED = 15

    def __init__(self, initial_position, path):
        self.snake_list = [initial_position]
        self.length = 1
        self.path = path
        return

    def move(self, new_position):
        self.snake_list.append(new_position)
        if len(self.snake_list) > self.length:
            return self.snake_list.pop(0)

    def grow(self):
        self.length+=1

    def auto_hit(self):
        head = self.snake_list[-1]
        
        for part in self.snake_list[:-1]:
            if part == head:
                return True

        return False

    def head(self):
        return self.snake_list[-1]