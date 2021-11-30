import os.path
import pygame.font
pygame.font.init()
"""폰트 모듈을 초기화 하고 종료한다"""
font_medium = pygame.font.Font(os.path.join('fonts', 'joystix.monospace.ttf'), 50)
font_small = pygame.font.Font(os.path.join('fonts', 'joystix.monospace.ttf'), 25)
