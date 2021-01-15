import sys
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, GameLogo, font_medium
from . import load_scene, SceneBase, HelpMenu, LevelSelectMenu


class MainMenu(SceneBase):
    def __init__(self):
        super().__init__()
        GameLogo(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4, self.all_sprites)
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2

        play_btn = TextButton(x, y, 'Играть', font_medium, self.all_sprites)
        help_btn = TextButton(x, y + 70, 'Помощь', font_medium, self.all_sprites)
        exit_btn = TextButton(x, y + 140, 'Выход', font_medium, self.all_sprites)

        play_btn.on_click = lambda b: load_scene(LevelSelectMenu())
        help_btn.on_click = lambda b: load_scene(HelpMenu())
        exit_btn.on_click = lambda b: sys.exit()
