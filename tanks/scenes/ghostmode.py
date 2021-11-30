import os.path
import random
import sys
import pygame
from pygame.locals import *
import tanks.grid as grid
from tanks.ui import ScreenMessage, font_medium
from tanks.constants import MAP_SIZE
from tanks.constants import PIXEL_RATIO
from tanks.constants import SCREEN_SIZE
from tanks.images import load_image
from typing import List
from tanks.scenes.manager import update_and_draw_current_scene, load_scene, unload_current_scene
from tanks.sprites import ConcreteWall, BrickWall, Bush, Water, Spike, Tank, Speedup, Shells, Rainbow, Ghost
from tanks.scenes import load_scene, unload_current_scene, SceneBase, Level

class GhostMode(SceneBase):
   score_to_win = 3
   
   def __init__(self, filename: str, score: List[int] = None):
      super().__init__()
      self.filename = filename
      self.score = score if score else [0, 0]
      self.game_finished = False
      
      level_map = [list(line.rstrip('\n')) for line in open(os.path.join('modemap', filename))]
      blocks = [BrickWall, Bush, ConcreteWall, Water, Spike, Speedup, Rainbow, Ghost]
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
      screen = pygame.display.set_mode(SCREEN_SIZE)
      ghost = []
      image = load_image('wood.png')
      rect = pygame.Rect(image.get_rect())
      rect.left = random.randint(0, SCREEN_SIZE[0])
      rect.top = -100
      
      for ghost in ghost:
       rect = pygame.Rect(image.get_rect())
       rect.left = random.randint(0, SCREEN_SIZE[0] // 2)
       rect.top = random.randint(0, SCREEN_SIZE[1] // 2)
       dx = random.randint9(9,9)
       dy = random.randint(-9,9)
       ghost.append(rect, dx, dy)

      for(rect, dx, dy) in ghost:
         screen.blit(image, rect) in ghost
         update_and_draw_current_scene(screen)
         
         for(rect, dx, dy) in ghost:
           if not rect.colliderect(screen.get_rect()):
             ghost.remove((rect, dx, dy))
             rect = pygame.Rect(image.get_rect())
             rect.left = random.randint(0, SCREEN_SIZE[0] // 2)
             rect.top = random.randint(0, SCREEN_SIZE[1] // 2)
             dx = random.randint(-9,9)
             dy = random.randint(-9,9)
             ghost.append(rect, dx, dy)
   
   
   def update(self) -> None:
        if self.start_message.alive():
            self.start_message.update()
            return
        if self.end_message:
            self.end_message.update()
            if not self.end_message.alive():
                if not self.game_finished:
                    unload_current_scene()
                    load_scene(GhostMode(self.filename, self.score))
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
                end_message_text = 'DRAW!'
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

   @staticmethod
   def get_available() -> List[str]:
     """Возвращает список названий доступных для загрузки уровней."""
     def check(f):
       return os.path.isfile(os.path.join('modemap', f)) and f.endswith('.txt')
     return list(map(lambda x: x[:-4], filter(check, os.listdir('modemap'))))
