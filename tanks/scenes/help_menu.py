from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.scenes import unload_current_scene, SceneBase


class HelpMenu(SceneBase):
    help_text = [
        'Для победы уничтожьте танк',
        'противника 3 раза',
        '',
        'Игрок 1',
        'Передвижение: WASD',
        'Огонь: Пробел',
        '',
        'Игрок 2',
        'Передвижение: Стрелки',
        'Огонь: Enter'
    ]

    def __init__(self):
        super().__init__()
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]

        Label(x, 50, 'Помощь', font_medium, self.all_sprites)
        for i in range(len(self.help_text)):
            Label(x, 150 + 40 * i, self.help_text[i], font_small, self.all_sprites)

        back_btn = TextButton(x, y - 40, 'Назад', font_small, self.all_sprites)
        back_btn.on_click = lambda b: unload_current_scene()
