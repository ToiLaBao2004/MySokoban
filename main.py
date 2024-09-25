import pygame
import assets
from game import Game

A = """  #####
###   #
# $ # ##
# #  . #
#    # #
## #   #
 #@   ###
 #####"""

matrix = [list(row) for row in A.splitlines()]

assets.load_sprites()
sprites = pygame.sprite.LayeredUpdates()

pygame.init()

pygame.display.set_caption("Sokoban")

gameSokoban = Game(matrix)

size = gameSokoban.load_size()
screen = pygame.display.set_mode(size)

running = True

while running:
    gameSokoban.print_game(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()