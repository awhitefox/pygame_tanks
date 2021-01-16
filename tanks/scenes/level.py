import os.path
import pygame
import tanks.grid as grid
from tanks.constants import MAP_SIZE
from tanks.sprites import ConcreteWall, BrickWall, Bush, Water, Spike, Tank
from tanks.ui import ScreenMessage, font_medium
from tanks.scenes import load_scene, unload_current_scene, SceneBase
from typing import List


class Level(SceneBase):
    """Сцена уровня"""
    score_to_win = 3

    def __init__(self, filename: str, score: List[int] = None):
        super().__init__()
        self.filename = filename
        self.score = score if score else [0, 0]
        self.game_finished = False

        grid_x = MAP_SIZE[0] // 2 - 1
        self.tank1 = Tank(*grid.cell_to_screen(grid_x, MAP_SIZE[1] - 2), True, self.all_sprites)
        self.tank2 = Tank(*grid.cell_to_screen(grid_x, 0), False, self.all_sprites)

        self.start_message = ScreenMessage("Приготовится!", font_medium, 2, self.all_sprites)
        self.end_message = None

    def update(self) -> None:
        if self.start_message.alive():
            self.start_message.update()
            return
        if self.end_message:
            self.end_message.update()
            if not self.end_message.alive():
                if not self.game_finished:
                    unload_current_scene()
                    load_scene(Level.load(self.filename, self.score))
                else:
                    unload_current_scene()
            return
        super().update()

        finish_round = False
        if not self.tank1.alive():
            self.score[1] += 1
            finish_round = True
        if not self.tank2.alive():
            self.score[0] += 1
            finish_round = True

        if finish_round:
            if self.score == [self.score_to_win, self.score_to_win]:
                end_message_text = 'Ничья!'
                self.game_finished = True
            elif self.score[0] == self.score_to_win:
                end_message_text = 'Игрок 1 победил!'
                self.game_finished = True
            elif self.score[1] == self.score_to_win:
                end_message_text = 'Игрок 2 победил!'
                self.game_finished = True
            else:
                end_message_text = f'{self.score[0]} : {self.score[1]}'
            self.end_message = ScreenMessage(end_message_text, font_medium, 3, self.all_sprites)
            return

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((116, 116, 116))  # gray
        pygame.draw.rect(surface, 'black', grid.get_rect())
        super().draw(surface)

    @classmethod
    def load(cls, filename: str, score: List[int] = None) -> 'Level':
        """Возвращает новую сцену уровня, построенную по карте из указанного файла.
        Поиск файла происходит в папке ./levels/"""
        level = cls(filename, score)
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
                if level_map[row][col] == Spike.char:
                    Spike(col, row, level.all_sprites)
        return level

    @staticmethod
    def get_available() -> List[str]:
        """Возвращает список названий доступных для загрузки уровней."""
        def check(f):
            return os.path.isfile(os.path.join('levels', f)) and f.endswith('.txt')
        return list(map(lambda x: x[:-4], filter(check, os.listdir('levels'))))
