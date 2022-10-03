from xxlimited import foo
import pygame
import random
import os
from datetime import datetime

from food import Food
from score import Score
from snake import Snake

import constants

class Game:
    def __init__(self, screen,font_style, score_font, snakes_paths, food_coords) -> None:
        self.screen = screen
        self.font_style = font_style
        self.score_font=score_font

        self.score = []
        self.clock = pygame.time.Clock()
        self.snake_paths = snakes_paths
        self.snake = []
        self.game_over = []
        self.food_iteration = []
        self.mov_x = []
        self.mov_y = []
        self.color = []
        self.food_coords = food_coords

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
            #self.food.append(Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK ))
            self.food_iteration.append(0)

            i+=1
        #self.snake = Snake([constants.MAX_WIDTH / 2,constants.MAX_HEIGHT / 2])
        #self.food = Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,Snake.SNAKE_BLOCK )
        
        if len(self.food_coords) == 0:
            self.food_coords.append(Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK ))

        self.game_loop()

    def all_ends(self):
        i=0
        while i < len(self.game_over):
            if self.game_over[i] == False:
                return False
            i+=1
        return True


    #Check aldedor de la serpiente
    # #0 nada
    # #1 final
    # #2 cola
    # #3 manzana    
    #  sistema de coordenadas
    #   [ 00,  01,    02 ]
    #   [ 10, cabeza, 12 ]
    #   [ 20, 21,     22 ]
    #
    #
    def check_coord(self, coord, snake_number):
        if coord[0]<0 or coord[1]<0 or coord[0]>=constants.MAX_WIDTH or coord[1] >= constants.MAX_HEIGHT: #final del mapa
            return 1
        elif coord in self.snake[snake_number].snake_list:
            return 2
        elif coord[0] == self.food_coords[self.food_iteration[snake_number]][0] and coord[1] == self.food_coords[self.food_iteration[snake_number]][1]:
            return 3
        else:
            return 0

    def game_loop(self):

        iteration = 0
        self.screen.fill(constants.BLUE)
        while not self.all_ends():
            i = 0
            for s in self.snake:
                if self.game_over[i] == False:
                    training_data = [
                            self.snake[i].head()[0], #headX
                            self.snake[i].head()[1],  #headY
                            self.check_coord([self.snake[i].head()[0] -1 ,self.snake[i].head()[1] +1], i),# 00  
                            self.check_coord([self.snake[i].head()[0],self.snake[i].head()[1] +1 ], i),# 01
                            self.check_coord([self.snake[i].head()[0] +1 ,self.snake[i].head()[1] +1 ], i),# 02
                            self.check_coord([self.snake[i].head()[0] -1 ,self.snake[i].head()[1]], i),# 11
                            self.check_coord([self.snake[i].head()[0] +1,self.snake[i].head()[1]], i),# 12
                            self.check_coord([self.snake[i].head()[0] -1,self.snake[i].head()[1] -1], i),# 20
                            self.check_coord([self.snake[i].head()[0],self.snake[i].head()[1] -1], i),# 21
                            self.check_coord([self.snake[i].head()[0] +1,self.snake[i].head()[1] -1], i),# 22 
                            self.snake[i].length, #len snake    
                            self.food_coords[self.food_iteration[i]][0], #foodX
                            self.food_coords[self.food_iteration[i]][1] #foodY
                            ]

                    if iteration >len([s.path]):
                        s.path.append(random.randint(1, 4))

                    if s.path[iteration] == 1: #LEFT
                        self.mov_x[i] = -1
                        self.mov_y[i] = 0
                        training_data.append(1) #Append decision for training purpose
                    if s.path[iteration] == 2: #RIGHT
                        self.mov_x[i] = 1
                        self.mov_y[i] = 0
                        training_data.append(2) #Append decision for training purpose
                    if s.path[iteration] == 3: #UP
                        self.mov_x[i] = 0
                        self.mov_y[i] = -1
                        training_data.append(3) #Append decision for training purpose
                    if s.path[iteration] == 4: #DOWN
                        self.mov_x[i] = 0
                        self.mov_y[i] = 1
                        training_data.append(4) #Append decision for training purpose
                    
                    x1 = self.snake[i].head()[0]
                    y1 = self.snake[i].head()[1]

                    x1 += self.mov_x[i]
                    y1 += self.mov_y[i]

                    pygame.draw.rect(self.screen, self.color[i], [self.food_coords[self.food_iteration[i]][0] * constants.SNAKE_BLOCK, self.food_coords[self.food_iteration[i]][1] * constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])

                    self.display_snake(i, [x1,y1], self.color[i])

                    if x1 >= constants.MAX_WIDTH or x1 < 0 or y1 >= constants.MAX_HEIGHT or y1 < 0 or self.snake[i].auto_hit():
                        self.game_over[i] = True
                        new_points -= 10000
                        self.score[i].add_score(new_points,training_data)
                        self.score[i].close()
                        print("Snake #"+str(i)+" has died")
                        for part in self.snake[i].snake_list:
                            pygame.draw.rect(self.screen, constants.BLUE, [part[0]* constants.SNAKE_BLOCK, part[1]* constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])
                        pygame.draw.rect(self.screen, constants.BLUE, [self.food_coords[self.food_iteration[i]][0]* constants.SNAKE_BLOCK, self.food_coords[self.food_iteration[i]][1]* constants.SNAKE_BLOCK, constants.SNAKE_BLOCK, constants.SNAKE_BLOCK])

                    if(self.game_over[i] != True):
                        new_points = 0
                        if x1 == self.food_coords[self.food_iteration[i]][0] and y1 == self.food_coords[self.food_iteration[i]][1]:
                            self.food_iteration[i] += 1
                            if (self.food_iteration[i] +1) > len(self.food_coords):
                                self.food_coords.append(Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK )) 

                            #self.food[i] = Food.generate(constants.MAX_WIDTH,constants.MAX_HEIGHT,constants.SNAKE_BLOCK )
                            new_points += 1000
                            self.snake[i].grow()
                            print("Snake #"+str(i)+" has eaten the food.")
                
                        if self.mov_x[i] != 0 or self.mov_y[i] != 0:
                            new_points +=1 #que se siga moviendo, esto hay que revisarlo y darle puntos por acercarse a la manzana

                        self.score[i].add_score(new_points,training_data)
                    pygame.display.update()
                i+=1

            self.clock.tick(constants.SNAKE_SPEED)
            iteration+=1

        pygame.quit()
        quit()