import sys
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, GameLogo, Label, font_medium, font_small
from tanks.scenes import load_scene, SceneBase
from tanks.scenes import load_scene, unload_current_scene
from tanks.scenes.speed_map1 import Speedmap15
from tanks.scenes.speed_map2 import Speedmap20

class SpeedSelect(SceneBase):
    def __init__(self):
        super().__init__()
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2

        x = SCREEN_SIZE[0] // 4
        self.title = Label(x * 2, 50, 'SPEED SELECTION', font_medium, self.all_sprites)
        btn4 = TextButton(x * 2, 145, '1.5x speed', font_small, self.all_sprites)
        btn5 = TextButton(x * 2, 190, '2.0x speed', font_small, self.all_sprites)

        self.btn_back = TextButton(x * 2, SCREEN_SIZE[1] - 40, 'Back', font_small, self.all_sprites)
        self.btn_back.on_click = lambda b: unload_current_scene()

        btn4.on_click = lambda b: load_scene(Speedmap15())
        btn5.on_click = lambda b: load_scene(Speedmap20())
