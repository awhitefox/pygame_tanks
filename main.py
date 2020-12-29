import pygame
from tanks.constants import *
import tanks.grid as grid
from tanks.load import load_level, create_random_level


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

running = True
create_random_level('test.txt')   # создание рандомной структуры лвла
while running:
    screen.fill((116, 116, 116))  # gray
    pygame.draw.rect(screen, 'black', grid.get_rect())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    load_level('test.txt', all_sprites)    # загрузка лвла
    delta_time = clock.tick() / 1000
    all_sprites.update(delta_time)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
