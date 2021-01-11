import pygame
import tanks.scenes as scenes
from tanks.constants import *
from tanks.time import tick
from tanks.sprites import Shell, Tank
from random import randint

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
scenes.load_scene(scenes.Level.load('test.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # Shell(pos[0], pos[1], randint(1, 4), scenes.current_scene().all_sprites)
            Tank(pos[0], pos[1], True, scenes.current_scene().all_sprites)
            # Tank(pos[0], pos[1]+100, False, scenes.current_scene().all_sprites)
    scenes.current_scene().update()
    scenes.current_scene().draw(screen)
    pygame.display.flip()
    tick()
pygame.quit()
