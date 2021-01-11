import pygame
import tanks.scenes as scenes
from tanks.constants import *
from tanks.time import tick

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
scenes.load_scene(scenes.Menu())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    scenes.current_scene().update()
    scenes.current_scene().draw(screen)
    pygame.display.flip()
    tick()
pygame.quit()
