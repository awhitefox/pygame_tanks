import pygame
import tanks.grid as grid
from tanks.constants import *
from tanks.time import tick
from tanks.load import load_level
from tanks.sprites import Shell
import random


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
all_sprites = pygame.sprite.Group()

load_level('test.txt', all_sprites)

running = True
while running:
    screen.fill((116, 116, 116))  # gray
    pygame.draw.rect(screen, 'black', grid.get_rect())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            Shell(pos[0], pos[1], random.randint(1, 4), all_sprites)
    tick()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
