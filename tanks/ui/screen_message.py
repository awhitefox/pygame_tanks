import pygame
from tanks.constants import SCREEN_SIZE
from tanks.time import delta_time


class ScreenMessage(pygame.sprite.Sprite):
    """UI 요소는 지정된 시간 동안 화면에 메시지를 표시합니다."""
    layer = 10
    border_thickness = 10
    padding = 75

    def __init__(self, text: str, font: pygame.font.Font, duration: float,
                 *groups: pygame.font.Font):
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

    def update(self) -> None:
        self.duration -= delta_time()
        if self.duration <= 0:
            self.kill()