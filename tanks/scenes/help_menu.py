from tanks.constants import SCREEN_SIZE
from tanks.ui import TextButton, Label, font_medium, font_small
from tanks.scenes import unload_current_scene, SceneBase


class HelpMenu(SceneBase):
    """도움말 메뉴 장면. 게임 및 제어에 대한 기본 정보를 포함합니다."""
    help_text = [
        'Destroy the tank to win',
        'You have three lives.',
        '',
        'Player 1',
        'Move: WASD',
        'Fire: Space',
        '',
        'Player 2',
        'Move: Arrow Key',
        'Fire: Enter'
    ]

    def __init__(self):
        super().__init__()
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]

        Label(x, 50, 'Help', font_medium, self.all_sprites)
        for i in range(len(self.help_text)):
            if self.help_text[i]:
                Label(x, 150 + 40 * i, self.help_text[i], font_small, self.all_sprites)

        back_btn = TextButton(x, y - 40, 'Back', font_small, self.all_sprites)
        back_btn.on_click = lambda b: unload_current_scene()