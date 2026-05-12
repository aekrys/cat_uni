import pygame
import json
import random
import os

pygame.init()

# Константы экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("CatUni - подготовься к экзамену")

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
JUMP = -15
SPEED = 8


# Загрузка изображений (для рыбки и преподавателя)
def load_image(path, size=(100, 100)):
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
        self.rect = pygame.Rect(x, y, 80, 80)
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
        self.rect = pygame.Rect(x, y, 120, 120)
        self.image = load_image("images/teacher.png", (50, 50))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, TEACHER, self.rect)

        # Игрок (котик)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
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


# Платформы
class Platform:
    def __init__(self, x, y, length):
        self.rect = pygame.Rect(x, y, length, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, GROUND, self.rect)


# Создание уровня
def generate_level():
    platforms = []
    x = 0
    while x < SCREEN_WIDTH:
        length = random.randint(400, 800)
        platforms.append(Platform(x, SCREEN_HEIGHT - 300, length))

        hole = random.randint(150, 300)
        x += length + hole

    return platforms


# Главная рабочая часть
FPS = 60
clock = pygame.time.Clock()
player = Player(100, SCREEN_HEIGHT - 600)
platforms = generate_level()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                player.jump()
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move(1)

    if not player.update(platforms):
        player = Player(100, SCREEN_HEIGHT - 600)
        platforms = generate_level()

    screen.fill(SKY)
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()