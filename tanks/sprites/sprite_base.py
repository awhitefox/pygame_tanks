import pygame


class SpriteBase(pygame.sprite.Sprite):
    sheet = None

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
