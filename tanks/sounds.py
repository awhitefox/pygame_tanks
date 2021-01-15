import os.path
import pygame.mixer
VOLUME = 0.5
pygame.mixer.init()


def load_sound(filename):
    sound = pygame.mixer.Sound(os.path.join('data', filename))
    sound.set_volume(VOLUME)
    return sound
