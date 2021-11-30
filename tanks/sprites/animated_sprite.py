import pygame
from tanks.time import delta_time


class AnimatedSprite(pygame.sprite.Sprite):
    """애니메이션 스프라이트의 기본 클래스는 상속에 사용됩니다."""
    frames = None
    seconds_per_frame = None

    def __init__(self, x: float, y: float, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.frame_i = 0
        self.seconds_from_frame_change = 0
        self.image = self.frames[self.frame_i]
        self.rect = pygame.Rect(x, y, *self.image.get_size())

    def update(self) -> None:
        self.seconds_from_frame_change += delta_time()
        if self.seconds_from_frame_change >= self.seconds_per_frame:
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            self.image = self.frames[self.frame_i]
            self.seconds_from_frame_change = 0
