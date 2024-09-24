import pygame
import assets


#Load sprites
assets.load_sprites()
sprites = pygame.sprite.LayeredUpdates()

#Khởi tạo pygame
pygame.init()

#Set screen với size = 500, 500
screen = pygame.display.set_mode((500, 500))

#Set title
pygame.display.set_caption("Sokoban")


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()