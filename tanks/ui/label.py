import pygame


class Label(pygame.sprite.Sprite):
    """Элемент UI, отображает строку текста на экране."""

    def __init__(self, center_x: float, center_y: float, text: str, font: pygame.font.Font,
                 *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.text = text
        self.font = font
        self.rect = pygame.Rect(0, 0, *self.font.size(self.text))
        self.rect.center = center_x, center_y
        self.image = pygame.surface.Surface(self.rect.size)

    def update(self) -> None:
        self.image = self.font.render(self.text, True, (255, 255, 255))
        w, h = self.image.get_size()
        self.rect.inflate_ip(w - self.rect.w, h - self.rect.h)
