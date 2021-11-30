from math import ceil
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.scenes.speed1 import Speed1
from tanks.scenes.speed2 import Speed2
from tanks.scenes import load_scene, unload_current_scene, SceneBase, Level

class SpeedSelect(SceneBase):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.mode_type = Speed1.get_available()
        self.mode_type = Speed2.get_available()
        self.current_page = 0
        self.mode_buttons = []
        x, y = SCREEN_SIZE[0] // 4, SCREEN_SIZE[1]
        
        self.title = Label(x * 2, 50, 'SPEED SELECTION', font_medium, self.all_sprites)
        btn1 = TextButton(x * 2, 145, '1.5x speed', font_small, self.all_sprites)
        btn2 = TextButton(x * 2, 190, '2.0x speed', font_small, self.all_sprites)

        btn1.on_click = lambda b: load_scene(Speed1(self.filename))
        btn2.on_click = lambda b: load_scene(Speed2(self.filename))

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