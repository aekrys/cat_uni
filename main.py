import pygame
import json


pygame.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CatUni - подготовься к экзамену")
FPS = 60

# Цвета фона
SKY = (135, 206, 235)
GROUND = (154, 215, 121)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Цвета котика
CAT_SKINS = {
    "orange": (247, 141, 54),
    "black": (50, 50, 50),
    "white": (240, 240, 240),
    "gray": (128, 128, 128),
    "brown": (133, 87, 56)
}
CURRENT_SKIN = "orange"
CAT_COLOR = CAT_SKINS[CURRENT_SKIN]

# Интерфейс
TEXT = (40, 40, 50)
RIGHT = (42, 224, 6)
WRONG = (224, 42, 6)
WARNING = (224, 224, 6)
