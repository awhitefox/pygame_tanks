import pygame


class SceneBase:
    def __init__(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()

    def update(self):
        self.all_sprites.update()

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def teardown(self):
        self.all_sprites.empty()
