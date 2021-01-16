import pygame.sprite
from tanks.sprites import SpriteBase
from tanks.images import load_image


class GameLogo(SpriteBase):
    """Спрайт логотипа игры"""
    sheet = load_image('logo.png')

    def __init__(self, center_x: float, center_y: float, *groups: pygame.sprite.Group):
        super().__init__(0, 0, *groups)
        self.rect.center = center_x, center_y
