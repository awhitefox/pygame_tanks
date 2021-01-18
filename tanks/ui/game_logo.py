import pygame.sprite
from tanks.images import load_image


class GameLogo(pygame.sprite.Sprite):
    """Спрайт логотипа игры"""
    sheet = load_image('logo.png')

    def __init__(self, center_x: float, center_y: float, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = self.image.get_rect()
        self.rect.center = center_x, center_y
