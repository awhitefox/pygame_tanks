import pygame
_clock = pygame.time.Clock()
_delta_time = 0


def tick() -> None:
    """Задает количество секунд, прошедших в прошлого кадра. Вызывается только в main!"""
    global _delta_time
    _delta_time = _clock.tick() / 1000


def delta_time() -> float:
    """이전 프레임에서 경과한 시간(초)을(를) 반환합니다."""
    return _delta_time
