import pygame
import random
import os
from datetime import datetime

from food import Food
from score import Score
from snake import Snake

import constants

class Game:
    def __init__(self, screen,font_style, score_font, snakes_paths) -> None:
        self.screen = screen
        self.font_style = font_style
        self.score_font=score_font

        self.score = []
        self.clock = pygame.time.Clock()
        self.snake_paths = snakes_paths
        self.snake = []
        self.game_over = []
        self.food = []
        self.mov_x = []
        self.mov_y = []
        self.color = []

    def display_score(self):
        value = self.score_font.render("Score: " + str(self.score.score), True, constants.YELLOW)
        self.screen.blit(value, [0, 0])

    def display_snake(self, index, position, color):
        last_part = self.snake[index].move(position)
        for part in self.snake[index].snake_list:
            pygame.draw.rect(self.screen, color, [part[0]*constants.SNAKE_BLOCK, part[1]*constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])
        if last_part:
            pygame.draw.rect(self.screen, constants.BLUE, [last_part[0]*constants.SNAKE_BLOCK, last_part[1]*constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])
 
    def display_message(self,msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.screen.blit(mesg, [constants.MAX_WIDTH*constants.SNAKE_BLOCK / 6, constants.MAX_HEIGHT*constants.SNAKE_BLOCK / 3])

    def start_game(self):
        #self.score.reset()

        time = datetime.now()
        SCORE_FOLDER = 'scores/'+time.strftime("%Y%m%d_%H%M%S")
        os.mkdir(SCORE_FOLDER)
        i=0
        for p in self.snake_paths:
            color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            self.color.append(color)
            self.score.append(Score(SCORE_FOLDER, i))
            self.mov_x.append(0)
            self.mov_y.append(0)
            self.game_over.append(False)
            self.snake.append(Snake([constants.MAX_WIDTH / 2,constants.MAX_HEIGHT / 2],p))
            self.food.append(Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK ))

            i+=1
        #self.snake = Snake([constants.MAX_WIDTH / 2,constants.MAX_HEIGHT / 2])
        #self.food = Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,Snake.SNAKE_BLOCK )
        
        self.game_loop()

    def all_ends(self):
        i=0
        while i < len(self.game_over):
            if self.game_over[i] == False:
                return False
            i+=1
        return True
        
    def game_loop(self):

        iteration = 0
        self.screen.fill(constants.BLUE)
        while not self.all_ends():
            i = 0
            for s in self.snake:
                if self.game_over[i] == False:
                    if iteration >len([s.path]):
                        s.path.append(random.randint(1, 4))

                    if s.path[iteration] == 1: #LEFT
                        self.mov_x[i] = -1
                        self.mov_y[i] = 0
                    if s.path[iteration] == 2: #RIGHT
                        self.mov_x[i] = 1
                        self.mov_y[i] = 0
                    if s.path[iteration] == 3: #UP
                        self.mov_x[i] = 0
                        self.mov_y[i] = -1
                    if s.path[iteration] == 4: #DOWN
                        self.mov_x[i] = 0
                        self.mov_y[i] = 1

                    x1 = self.snake[i].head()[0]
                    y1 = self.snake[i].head()[1]

                    x1 += self.mov_x[i]
                    y1 += self.mov_y[i]

                    pygame.draw.rect(self.screen, self.color[i], [self.food[i][0] * constants.SNAKE_BLOCK, self.food[i][1] * constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])

                    self.display_snake(i, [x1,y1], self.color[i])

                    if x1 >= constants.MAX_WIDTH or x1 < 0 or y1 >= constants.MAX_HEIGHT or y1 < 0 or self.snake[i].auto_hit():
                        self.game_over[i] = True
                        print("Snake KO: "+str(i))
                        pygame.draw.rect(self.screen, constants.BLUE, [self.food[i][0], self.food[i][1], constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])
            
                    if x1 == self.food[i][0] and y1 == self.food[i][1]:
                        self.food[i] = Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK )
                        self.score[i].add_score(1000)
                        self.snake[i].grow()
                        print("YUUUM "+str(i))
            
                    if self.mov_x[i] != 0 or self.mov_y[i] != 0:
                        self.score[i].add_score(1)

                    #self.display_score()
                    pygame.display.update()
                i+=1

            self.clock.tick(constants.SNAKE_SPEED)
            iteration+=1

        pygame.quit()
        quit()

## registrar estado del juego en cada loop (mirar como almacenar todo en una matriz) posiblemente un csv
## hacer sistema de score mejorado
## añadir que si se acerca a la manzana da mas puntos