import pygame
from tanks.input import mouse_keys_just_pressed


class TextButton(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, text, font, *groups):
        super().__init__(*groups)
        self.enabled = True
        self.raw_text = text
        self.font = font
        self.on_click = None
        self.rect = pygame.Rect(0, 0, *self.font.size(self.get_text()))
        self.rect.center = center_x, center_y
        self.image = pygame.surface.Surface(self.rect.size)

    def get_text(self, hover=False):
        return (f'> {self.raw_text} <' if hover else f'  {self.raw_text}  ') if self.enabled else ''

    def update(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        click = self.enabled and hover and 1 in mouse_keys_just_pressed
        self.image = self.font.render(self.get_text(hover), True, (255, 255, 255))
        w, h = self.image.get_size()
        self.rect.inflate_ip(w - self.rect.w, h - self.rect.h)
        if self.on_click and click:
            self.on_click(self)