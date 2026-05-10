import pygame
import json
import random
import os

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

# Цвета рыбки и преподавателя (если что-то произойдет с изображениями)
FISH = (77, 97, 106)
TEACHER = (79, 56, 92)

# Интерфейс
TEXT = (40, 40, 50)
RIGHT = (42, 224, 6)
WRONG = (224, 42, 6)
WARNING = (224, 224, 6)

# Физика
GRAVITY = 0.8
JUMP = -10
SPEED = 5


# Загрузка изображений (для рыбки и преподавателя)
def load_image(path, size=(50, 50)):
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception:
            pass
    return None


# Рыбка
class Fish:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = load_image("images/fish.png", (30, 30))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            if self.image:
                screen.blit(self.image, self.rect)
            else:
                pygame.draw.circle(screen, FISH, self.rect.center, 15)

            # Преподаватель


class Teacher:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = load_image("images/teacher.png", (50, 50))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, TEACHER, self.rect)

        # Игрок (котик)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vert_speed = 0
        self.on_ground = False

    def update(self, platforms):
        self.vert_speed += GRAVITY
        self.rect.y += self.vert_speed
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vert_speed > 0 and self.rect.bottom - self.vert_speed <= platform.rect.top + 5:
                    self.rect.bottom = platform.rect.top
                    self.vert_speed = 0
                    self.on_ground = True

        if self.rect.top > SCREEN_HEIGHT:
            return False
        return True

    def jump(self):
        if self.on_ground:
            self.vert_speed = JUMP

    def move(self, dx):
        self.rect.x += dx * SPEED

    def draw(self, screen):
        # Тело
        pygame.draw.rect(screen, CAT_COLOR, self.rect)
        # Уши
        pygame.draw.polygon(screen, CAT_COLOR, [
            (self.rect.x, self.rect.y),
            (self.rect.x + 10, self.rect.y - 12),
            (self.rect.x + 20, self.rect.y)
        ])
        pygame.draw.polygon(screen, CAT_COLOR, [
            (self.rect.x + 10, self.rect.y),
            (self.rect.x + 30, self.rect.y - 12),
            (self.rect.x + 40, self.rect.y)
        ])
        # Глаза
        pygame.draw.circle(screen, WHITE, (self.rect.x + 12, self.rect.y + 15), 4)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 28, self.rect.y + 15), 4)
        pygame.draw.circle(screen, BLACK, (self.rect.x + 12, self.rect.y + 15), 2)
        pygame.draw.circle(screen, BLACK, (self.rect.x + 28, self.rect.y + 15), 2)