import os.path
import pygame.mixer
VOLUME = 0.75
pygame.mixer.init()


def load_sound(filename: str) -> pygame.mixer.Sound:
    """Возвращает звук, загруженный из указанного файла. Поиск файла происходит в папке ./data/"""
    sound = pygame.mixer.Sound(os.path.join('data', filename))
    sound.set_volume(VOLUME)
    return sound
