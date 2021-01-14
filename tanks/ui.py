import os.path
import pygame
from tanks.constants import SCREEN_SIZE
from tanks.time import delta_time
from tanks.sprites import SpriteBase, load_image
from tanks.input import mouse_keys_just_pressed

pygame.font.init()
font_medium = pygame.font.Font(os.path.join('fonts', 'joystix.monospace.ttf'), 50)
font_small = pygame.font.Font(os.path.join('fonts', 'joystix.monospace.ttf'), 25)


class Label(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, text, font, *groups):
        super().__init__(*groups)
        self.text = text
        self.font = font
        self.rect = pygame.Rect(0, 0, *self.font.size(self.text))
        self.rect.center = center_x, center_y
        self.image = pygame.surface.Surface(self.rect.size)

    def update(self):
        self.image = self.font.render(self.text, True, (255, 255, 255))
        w, h = self.image.get_size()
        self.rect.inflate_ip(w - self.rect.w, h - self.rect.h)


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


class GameLogo(SpriteBase):
    sheet = load_image('logo.png')

    def __init__(self, center_x, center_y, *groups):
        super().__init__(0, 0, *groups)
        self.rect.center = center_x, center_y


class ScreenMessage(pygame.sprite.Sprite):
    layer = 10
    border_thickness = 10
    padding = 75

    def __init__(self, text, font, duration, *groups):
        super().__init__(*groups)
        w, h = font.size(text)
        self.rect = pygame.Rect(0, 0, w + self.padding, h + self.padding)
        self.rect.center = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        self.text = text
        self.font = font
        self.duration = duration

        self.image = pygame.surface.Surface(self.rect.size)
        pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect(0, 0, *self.rect.size))
        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(0, 0, *self.rect.size),
                         self.border_thickness)
        w, h = self.rect.size
        tw, th = self.font.size(self.text)
        text_rect = pygame.Rect((w - tw) / 2, (h - th) / 2, tw, th)
        self.image.blit(self.font.render(self.text, True, (255, 255, 255)), text_rect)

    def update(self):
        self.duration -= delta_time()
        if self.duration <= 0:
            self.kill()
