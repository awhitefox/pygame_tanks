import pygame
import tanks.grid as grid
from tanks.constants import *
from tanks.time import tick
from tanks.load import load_level


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
all_sprites = pygame.sprite.Group()
load_level(input(), all_sprites)

running = True
while running:
    screen.fill((116, 116, 116))  # gray
    pygame.draw.rect(screen, 'black', grid.get_rect())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    tick()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
