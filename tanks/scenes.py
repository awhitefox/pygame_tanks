import os.path
from math import ceil
import pygame
import tanks.grid as grid
from tanks.constants import SCREEN_SIZE
from tanks.sprites import ConcreteWall, BrickWall, Bush, Water, Tank
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.input import mouse_keys_just_pressed

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
        self.all_sprites.empty()


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        play_btn = TextButton(x, y, 'Играть', font_medium, self.all_sprites)
        play_btn.on_click = lambda b: load_scene(LevelSelectMenu())


class LevelSelectMenu(Scene):
    def __init__(self):
        super().__init__()
        self.levels = Level.get_available()
        self.current_page = 0
        self.level_buttons = []

        x = SCREEN_SIZE[0] // 4
        self.title = Label(x * 2, 50, 'Выбор уровня', font_medium, self.all_sprites)
        for i in range(12):
            btn = TextButton(x * 2, 100 + 45 * (i + 1), '', font_small, self.all_sprites)
            self.level_buttons.append(btn)
        y = SCREEN_SIZE[1] - 80
        self.btn_prev = TextButton(x, y, 'ПРЕД', font_small, self.all_sprites)
        self.page_label = Label(x * 2, y, '', font_medium, self.all_sprites)
        self.btn_next = TextButton(x * 3, y, 'СЛЕД', font_small, self.all_sprites)
        self.btn_back = TextButton(x * 2, y + 40, 'Назад', font_small, self.all_sprites)

        self.bind_events()
        self.render_page()

    def bind_events(self):
        self.btn_prev.on_click = self.on_prev_btn
        self.btn_next.on_click = self.on_next_btn
        self.btn_back.on_click = lambda b: load_scene(MainMenu())
        for btn in self.level_buttons:
            btn.on_click = lambda b: load_scene(Level.load(b.raw_text + '.txt'))

    def render_page(self):
        i = self.current_page
        n = len(self.level_buttons)
        levels = self.levels[n * i:n * (i + 1)]
        self.page_label.text = f'{i + 1}/{ceil(len(self.levels) / n)}'
        for j in range(n):
            if j < len(levels):
                self.level_buttons[j].raw_text = levels[j]
                self.level_buttons[j].enabled = True
            else:
                self.level_buttons[j].enabled = False

    def on_prev_btn(self, btn):
        self.current_page = max(self.current_page - 1, 0)
        self.render_page()

    def on_next_btn(self, btn):
        self.current_page = min(self.current_page + 1, len(self.levels) // len(self.level_buttons))
        self.render_page()


class Level(Scene):
    def __init__(self):
        super().__init__()
        self.flag = True

    def update(self):
        if 1 in mouse_keys_just_pressed:
            pos = pygame.mouse.get_pos()
            if self.flag:
                Tank(pos[0], pos[1], True, self.all_sprites)
                self.flag = False
            else:
                Tank(pos[0], pos[1], False, self.all_sprites)
        super().update()

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
                    Bush(col, row, level.all_sprites)
                if level_map[row][col] == ConcreteWall.char:
                    ConcreteWall(col, row, level.all_sprites)
                if level_map[row][col] == Water.char:
                    Water(col, row, level.all_sprites)
        return level

    @staticmethod
    def get_available():
        def check(f):
            return os.path.isfile(os.path.join('levels', f)) and f.endswith('.txt')
        return list(map(lambda x: x[:-4], filter(check, os.listdir('levels'))))
