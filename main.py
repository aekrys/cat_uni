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
GROUND_GREEN = (154, 215, 121)
GROUND_BROWN = (84, 53, 33)

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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (237, 151, 205)

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

    def draw(self, screen, camera):
        if not self.collected:
            cam_move = self.rect.x - camera
            if self.image:
                screen.blit(self.image, (cam_move, self.rect.y))
            else:
                pygame.draw.circle(screen, FISH, (cam_move + 40, self.rect.y + 40), 40)


# Преподаватель
class Teacher:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 120)
        self.image = load_image("images/teacher.png", (50, 50))

    def draw(self, screen, camera):
        cam_move = self.rect.x - camera
        if self.image:
            screen.blit(self.image, (cam_move, self.rect.y))
        else:
            pygame.draw.rect(screen, TEACHER, (cam_move, self.rect.y, 120, 120))

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

    def draw(self, screen, camera):
        cam_move = self.rect.x - camera
        # Тело
        pygame.draw.rect(screen, CAT_COLOR, (cam_move, self.rect.y, 100, 100))

        # Уши
        pygame.draw.polygon(screen, CAT_COLOR, [
            (cam_move, self.rect.y),
            (cam_move + 20, self.rect.y - 25),
            (cam_move + 40, self.rect.y)
        ])
        pygame.draw.polygon(screen, CAT_COLOR, [
            (cam_move + 60, self.rect.y),
            (cam_move + 80, self.rect.y - 25),
            (cam_move + 100, self.rect.y)
        ])
        pygame.draw.polygon(screen, PINK, [
            (cam_move + 10, self.rect.y),
            (cam_move + 20, self.rect.y - 15),
            (cam_move + 30, self.rect.y)
        ])
        pygame.draw.polygon(screen, PINK, [
            (cam_move + 70, self.rect.y),
            (cam_move + 80, self.rect.y - 15),
            (cam_move + 90, self.rect.y)
        ])

        # Глаза
        pygame.draw.circle(screen, WHITE, (cam_move + 25, self.rect.y + 40), 12)
        pygame.draw.circle(screen, WHITE, (cam_move + 75, self.rect.y + 40), 12)
        pygame.draw.circle(screen, BLACK, (cam_move + 25, self.rect.y + 40), 6)
        pygame.draw.circle(screen, BLACK, (cam_move + 75, self.rect.y + 40), 6)

        # Нос
        pygame.draw.polygon(screen, PINK, [
            (cam_move + 43, self.rect.y + 55),
            (cam_move + 50, self.rect.y + 62),
            (cam_move + 57, self.rect.y + 55)
        ])


# Платформы
class Platform:
    def __init__(self, x, y, length):
        self.rect = pygame.Rect(x, y, length, 300)

    def draw(self, screen, camera):
        cam_move = self.rect.x - camera
        pygame.draw.rect(screen, GROUND_BROWN, (cam_move, self.rect.y, self.rect.width, self.rect.height))
        pygame.draw.rect(screen, GROUND_GREEN, (cam_move, self.rect.y, self.rect.width, self.rect.height - 200))


# Создание уровня
camera = 0
next_platform = 0
platforms = []

for _ in range(5):
    length = random.randint(400, 800)
    platforms.append(Platform(next_platform, SCREEN_HEIGHT - 300, length))
    hole = random.randint(150, 300)
    next_platform += length + hole


# Главная рабочая часть
FPS = 60
clock = pygame.time.Clock()
player = Player(100, SCREEN_HEIGHT - 600)
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
        camera = 0
        next_platform = 0
        platforms.clear()
        for _ in range(5):
            length = random.randint(400, 800)
            platforms.append(Platform(next_platform, SCREEN_HEIGHT - 300, length))
            hole = random.randint(150, 300)
            next_platform += length + hole

    camera_place = player.rect.centerx - SCREEN_WIDTH // 3
    camera += (camera_place - camera) * 0.1
    if camera < 0:
        camera = 0

    if player.rect.right > next_platform - SCREEN_WIDTH * 1.5:
        for _ in range(5):
            length = random.randint(400, 800)
            platforms.append(Platform(next_platform, SCREEN_HEIGHT - 300, length))
            hole = random.randint(150, 300)
            next_platform += length + hole
    platforms = [platform for platform in platforms if platform.rect.right > camera - 200]


    screen.fill(SKY)
    for platform in platforms:
        platform.draw(screen, camera)
    player.draw(screen, camera)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()