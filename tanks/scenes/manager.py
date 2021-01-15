import pygame.draw
from tanks.constants import DEBUG
_loaded = []


def update_and_draw_current_scene(screen):
    current = _loaded[-1]
    current.update()
    if current == _loaded[-1]:  # if scene have not changed during update
        current.draw(screen)
        if DEBUG:
            for sprite in current.all_sprites:
                if sprite.rect.w > 0 and sprite.rect.h > 0:
                    # draws debug outlines for sprites
                    pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 1)


def load_scene(scene):
    _loaded.append(scene)


def unload_current_scene():
    if len(_loaded) == 0:
        return
    _loaded.pop(-1).teardown()
