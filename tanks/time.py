import pygame
_clock = pygame.time.Clock()
_delta_time = 0


def tick():
    global _delta_time
    _delta_time = _clock.tick()


def delta_time():
    return _delta_time