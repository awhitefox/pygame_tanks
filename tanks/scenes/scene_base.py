import pygame


class SceneBase:
    """Базовый класс сцены, используется для наследования."""
    def __init__(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()

    def update(self) -> None:
        """Выполняет обновление всех спрайтов на сцене."""
        self.all_sprites.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Выполняет отрисовку всех спрайтов на сцене."""
        self.all_sprites.draw(surface)

    def teardown(self) -> None:
        """Выполняет очистку ресурсов сцены."""
        self.all_sprites.empty()
