import os.path
import pygame
from pygame import Surface, surface
import tanks.grid as grid
from tanks.constants import MAP_SIZE
from tanks.sprites import tank, ConcreteWall, BrickWall, Bush, Water, Spike, Tank, Speedup, Shells, Rainbow, Ghost, shell_Speedup,Shell, Coins,Coin
from tanks.ui import ScreenMessage, font_medium
from tanks.scenes import load_scene, unload_current_scene, SceneBase
from typing import List
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
import time


FPSCLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)


class Coinmode(SceneBase):
    """Сцена уровня"""
    score_to_win = 3
    point = 0
    
    def __init__(self, filename: str, score: List[int] = None):
        """Инициализирует новую сцену уровня, построенную по карте из указанного файла.
        Поиск файла происходит в папке ./levels/"""

        super().__init__()
        self.filename = filename
        self.score = score if score else [0, 0]
        self.game_finished = False

        level_map = [list(line.rstrip('\n')) for line in open(os.path.join('modemap', filename))]

        if(len(level_map[-1])<10):
            Shell.shootrange=int("".join(level_map[-1]))
            del level_map[-1]
        else:
            Shell.shootrange=100000

        blocks = [BrickWall, Bush, ConcreteWall, Water, Spike, Speedup, Rainbow, Ghost, shell_Speedup,Coin,Coins]
        for row in range(len(level_map)):
            for col in range(len(level_map[row])):
                for block in blocks:
                    if level_map[row][col] == block.char:
                        block(col, row, self.all_sprites)

        grid_x = MAP_SIZE[0] // 2 - 1

        self.tank1 = Tank(*grid.cell_to_screen(grid_x, MAP_SIZE[1] - 2), True, self.all_sprites)
        self.tank2 = Tank(*grid.cell_to_screen(grid_x, 0), False, self.all_sprites)

        self.start_message = ScreenMessage("Ready!", font_medium, 2, self.all_sprites)
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
                    load_scene(Coinmode(self.filename, self.score))
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
                end_message_text = 'Draw!'
                self.game_finished = True
            elif self.score[0] == self.score_to_win:
                end_message_text = 'Player 1 win!'
                self.game_finished = True
            elif self.score[1] == self.score_to_win:
                end_message_text = 'Player 2 win!'
                self.game_finished = True
            else:
                end_message_text = f'{self.score[0]} : {self.score[1]}'
            self.end_message = ScreenMessage(end_message_text, font_medium, 3, self.all_sprites)
            return



    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((116, 116, 116))  # gray
        pygame.draw.rect(surface, 'black', grid.get_rect())
        super().draw(surface)

        scorefont1 = pygame.font.SysFont("arial", 25, True, False)
        scorefont2 = pygame.font.SysFont("arial", 25, True, False)
        mess_score1 = scorefont1.render("player1: " + str(self.tank1.point), True, WHITE) 
        mess_score2 = scorefont2.render("player2: " + str(self.tank2.point), True, WHITE) 
        surface.blit(mess_score1, (50, 50))
        surface.blit(mess_score2, (650, 50))
        pygame.display.update()
        FPSCLOCK.tick(60)

    @staticmethod
    def get_available() -> List[str]:
        """Возвращает список названий доступных для загрузки уровней."""
        def check(f):
            return os.path.isfile(os.path.join('modemap', f)) and f.endswith('.txt')
        return list(map(lambda x: x[:-4], filter(check, os.listdir('modemap'))))

