import pygame
import sprites
from settings import *


pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Jumper")
clock = pygame.time.Clock()

layout = sprites.Layout(LAYOUT, screen)

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(SKY_BLUE)
    layout.update()
    # player.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
