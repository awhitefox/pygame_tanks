import pygame
from tanks.constants import DEBUG
from tanks.scenes import SceneBase
_loaded = []


def update_and_draw_current_scene(screen: pygame.Surface) -> None:
    """Выполняет обновление текущей сцены, и если она не была изменена в процессе, то и ее
    отрисовку. Если программа в режиме DEBUG, то обрисовывает все спрайты сцены красными
    прямоугольниками."""
    current = _loaded[-1]
    current.update()
    if current == _loaded[-1]:  # if scene have not changed during update
        current.draw(screen)
        if DEBUG:
            for sprite in current.all_sprites:
                if sprite.rect.w > 0 and sprite.rect.h > 0:
                    # draws debug outlines for sprites
                    pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 1)


def load_scene(scene: SceneBase) -> None:
    """Загружает переданную сцену в конец стека сцен."""
    _loaded.append(scene)


def unload_current_scene() -> None:
    """Удаляет последнюю сцену из стека сцен."""
    if len(_loaded) == 0:
        return
    _loaded.pop(-1).teardown()
