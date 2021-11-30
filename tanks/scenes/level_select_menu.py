from math import ceil
from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.scenes import load_scene, unload_current_scene, SceneBase, Level


class LevelSelectMenu(SceneBase):
    """레벨 선택 메뉴 장면"""

    def __init__(self):
        super().__init__()
        self.levels = Level.get_available()
        self.current_page = 0
        self.level_buttons = []

        x = SCREEN_SIZE[0] // 4
        self.title = Label(x * 2, 50, 'Level selection', font_medium, self.all_sprites)
        for i in range(12):
            btn = TextButton(x * 2, 100 + 45 * (i + 1), '', font_small, self.all_sprites)
            self.level_buttons.append(btn)
        y = SCREEN_SIZE[1] - 80
        self.btn_prev = TextButton(x, y, 'Previous', font_small, self.all_sprites)
        self.page_label = Label(x * 2, y, '', font_medium, self.all_sprites)
        self.btn_next = TextButton(x * 3, y, 'Next', font_small, self.all_sprites)
        self.btn_back = TextButton(x * 2, y + 40, 'Back', font_small, self.all_sprites)

        self.btn_prev.on_click = lambda b: self.prev_page()
        self.btn_next.on_click = lambda b: self.next_page()
        self.btn_back.on_click = lambda b: unload_current_scene()
        for btn in self.level_buttons:
            btn.on_click = lambda b: load_scene(Level(b.raw_text + '.txt'))

        self.render_page()

    def render_page(self) -> None:
        """Обновляет интерфейс в соответствии с текущей страницей списка уровней."""
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

    def prev_page(self) -> None:
        """Перелистывает список уровней на предыдущую страницу, если это возможно."""
        self.current_page = max(self.current_page - 1, 0)
        self.render_page()

    def next_page(self) -> None:
        """Перелистывает список уровней на следующую страницу, если это возможно."""
        self.current_page = min(self.current_page + 1, len(self.levels) // len(self.level_buttons))
        self.render_page()
