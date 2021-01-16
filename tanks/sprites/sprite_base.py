import pygame


class SpriteBase(pygame.sprite.Sprite):
    """Базовый класс спрайта, используется для наследования."""
    sheet = None

    def __init__(self, x: float, y: float, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
