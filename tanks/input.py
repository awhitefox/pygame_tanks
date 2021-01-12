import pygame


def is_pressed(key):
    return pygame.key.get_pressed()[key]


def is_just_pressed(key):
    return


def is_mouse_pressed(key):
    return pygame.mouse.get_pressed(5)[key]


def is_mouse_just_pressed(key):
    return
