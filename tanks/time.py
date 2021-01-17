import pygame
_clock = pygame.time.Clock()
_delta_time = 0


def tick() -> None:
    """Задает количество секунд, прошедших в прошлого кадра. Вызывается только в main!"""
    global _delta_time
    _delta_time = _clock.tick() / 1000


def delta_time() -> float:
    """Возвращает количество секунд, прошедших в прошлого кадра."""
    return _delta_time
