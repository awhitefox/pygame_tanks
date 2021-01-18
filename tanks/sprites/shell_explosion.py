import pygame
from tanks.images import load_image, cut_sheet
from tanks.sprites import AnimatedSprite
from tanks.sounds import load_sound


class ShellExplosion(AnimatedSprite):
    """Класс взрыва снаряда"""
    frames = cut_sheet(load_image('explosion.png'), 3, 1)
    sound = load_sound('shell_explosion.wav')
    seconds_per_frame = 0.125
    layer = 3

    def __init__(self, x: float, y: float, *groups: pygame.sprite.Group):
        w, h = self.frames[0].get_size()
        super().__init__(x - w / 2, y - h / 2, *groups)
        self.looped = False
        self.sound.play()

    def update(self) -> None:
        if self.frame_i == len(self.frames) - 1:
            self.looped = True
        elif self.frame_i == 0 and self.looped:
            self.kill()
            return
        super().update()
