import os.path
import pygame
import tanks.grid as grid
from tanks.sprites import ConcreteWall, BrickWall, Bush, Water

_current = None


def current_scene():
    return _current


def load_scene(scene):
    global _current
    if _current:
        _current.teardown()
    _current = scene


class Scene:
    def __init__(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()

    def update(self):
        self.all_sprites.update()

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def teardown(self):
        self.all_sprites.remove()


class Level(Scene):
    def draw(self, surface):
        surface.fill((116, 116, 116))  # gray
        pygame.draw.rect(surface, 'black', grid.get_rect())
        super().draw(surface)

    @classmethod
    def load(cls, filename):
        level = cls()
        level_map = [list(line.rstrip('\n')) for line in open(os.path.join('levels', filename))]
        for row in range(len(level_map)):
            for col in range(len(level_map[row])):
                if level_map[row][col] == BrickWall.char:
                    BrickWall(col, row, level.all_sprites)
                if level_map[row][col] == Bush.char:
                    Bush(col, row, )
                if level_map[row][col] == ConcreteWall.char:
                    ConcreteWall(col, row, level.all_sprites)
                if level_map[row][col] == Water.char:
                    Water(col, row, level.all_sprites)
        return level
