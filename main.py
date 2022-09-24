import pygame
import game
import constants

import multiprocessing

pygame.init()

screen = pygame.display.set_mode((constants.MAX_WIDTH * constants.SNAKE_BLOCK, constants.MAX_HEIGHT * constants.SNAKE_BLOCK))
pygame.display.set_caption('Snake Game')

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

snakes_paths = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3,3],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4]
]

g = game.Game(screen, font_style, score_font,snakes_paths)
g.start_game()
