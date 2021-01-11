import os.path
import pygame

pygame.font.init()
font = pygame.font.Font(os.path.join('fonts', 'joystix.monospace.ttf'), 50)


class TextButton(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, text, on_click, *groups):
        super().__init__(*groups)
        self.text = text
        self.on_click = on_click
        self.rect = pygame.Rect(0, 0, *font.size(self.get_text(True)))
        self.rect.center = center_x, center_y

    def get_text(self, hover=False):
        if hover:
            return f'> {self.text} <'
        else:
            return f'  {self.text}  '

    def update(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        click = hover and pygame.mouse.get_pressed(3)[0]
        self.image = font.render(self.get_text(hover), False, (255, 255, 255))
        if click:
            self.on_click()
