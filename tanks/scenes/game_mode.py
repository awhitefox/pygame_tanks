from math import ceil
from tanks import scenes
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.scenes.mode_type import ModeType
from tanks.scenes.ghostmode import GhostMode
from tanks.scenes.coinmode import Coinmode
from tanks.scenes.speedselect import SpeedSelect
from tanks.scenes import load_scene, unload_current_scene, SceneBase, Level

class GameMode(SceneBase):
    def __init__(self):
        super().__init__()
        self.mode_type = ModeType.get_available()
        self.current_page = 0
        self.mode_buttons = []
        x, y = SCREEN_SIZE[0] // 4, SCREEN_SIZE[1]

        self.title = Label(x * 2, 50, 'MODE SELECTION', font_medium, self.all_sprites)
        btn1 = TextButton(x * 2, 145, 'item', font_small, self.all_sprites)
        btn2 = TextButton(x * 2, 190, 'speed', font_small, self.all_sprites)
        btn3 = TextButton(x * 2, 235, 'ghost', font_small, self.all_sprites)
        btn4 = TextButton(x * 2, 280, 'coin battle', font_small, self.all_sprites)

        btn1.on_click = lambda b: load_scene(ModeType(b.raw_text + '.txt'))
        btn2.on_click = lambda b: load_scene(SpeedSelect(b.raw_text + '.txt'))
        btn3.on_click = lambda b: load_scene(GhostMode(b.raw_text + '.txt'))
        btn4.on_click = lambda b: load_scene(Coinmode(b.raw_text + '.txt'))

        back_btn = TextButton(SCREEN_SIZE[0] // 2, y - 40, 'Back', font_small, self.all_sprites)
        back_btn.on_click = lambda b: unload_current_scene()

        self.render_page()


    
    def render_page(self) -> None:
        """Обновляет интерфейс в соответствии с текущей страницей списка уровней."""
        i = self.current_page
        n = len(self.mode_buttons)
        mode_type = self.mode_type[n * i:n * (i + 1)]
        for j in range(n):
            if j < len(mode_type):
                self.mode_buttons[j].raw_text = mode_type[j]
                self.mode_buttons[j].enabled = True
            else:
                self.mode_buttons[j].enabled = False
