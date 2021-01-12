import pygame
import tanks.scenes as scenes
from tanks.constants import *
from tanks.time import tick
from tanks.input import keys_just_pressed, mouse_keys_just_pressed

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
scenes.load_scene(scenes.Level.load('test.txt'))

running = True
while running:
    keys_just_pressed.clear()
    mouse_keys_just_pressed.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys_just_pressed.add(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_keys_just_pressed.add(event.button)
    scenes.current_scene().update()
    scenes.current_scene().draw(screen)
    pygame.display.flip()
    tick()
pygame.quit()
