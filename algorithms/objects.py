import pygame
import random
from images import load_image

# Цвета фона
SKY = (135, 206, 235)
GROUND_GREEN = (154, 215, 121)
GROUND_BROWN = (84, 53, 33)

# Цвета котика
CAT_SKINS = {
    "orange": (247, 141, 54),
    "black": (30, 30, 30),
    "cream": (225, 215, 195),
    "gray": (128, 128, 128),
    "brown": (133, 87, 56)
}
CURRENT_SKIN = "orange"
CAT_COLOR = CAT_SKINS[CURRENT_SKIN]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (237, 151, 205)

# Цвета рыбки, сердец, птицы, бустера (если что-то произойдет с изображениями) и шипов
FISH = (77, 97, 106)
RED = (225, 50, 50)
BIRD = (75, 70, 90)
BOOSTER = (240, 230, 5)
SPIKE = (90, 20, 20)

# Цвета бустеров
SPEED_COLOR = (195, 130, 245)
SHIELD_COLOR = (25, 90, 120)
JUMP_COLOR = (170, 210, 85)

# Интерфейс
TEXT = (40, 40, 50)

# Физика
GRAVITY = 0.8
JUMP = -15
SPEED = 8



# Рыбка
class Fish:
    def __init__(self, x, y):
        """
        Создаёт объект рыбки: задаёт прямоугольник, загружает спрайт, флаг collected=False
        """

        self.rect = pygame.Rect(x, y, 75, 75)
        self.image = load_image("images/fish.png", (75, 75))
        self.collected = False

    def draw(self, screen, camera):
        """
        Отрисовывает рыбку: картинка или круг-заглушка
        """

        if not self.collected:
            cam_move = self.rect.x - camera
            if self.image:
                screen.blit(self.image, (cam_move, self.rect.y))
            else:
                pygame.draw.circle(screen, FISH, (cam_move + 75, self.rect.y + 75), 40)



# Игрок (котик)
class Player:
    def __init__(self, x, y):
        """
        Инициализирует котика: позиция, скорость, флаг on_ground
        """

        self.rect = pygame.Rect(x, y, 100, 100)
        self.vert_speed = 0
        self.on_ground = False

        self.speed_booster_time = 0
        self.shield_booster_time = 0
        self.jump_booster_time = 0


    def update(self, platforms, screen_height):
        """
        Применяет гравитацию, проверяет коллизии с платформами, возвращает False при падении в яму
        """

        # Уменьшаем время бустеров, если они есть
        if self.speed_booster_time > 0:
            self.speed_booster_time -= 1
        if self.shield_booster_time > 0:
            self.shield_booster_time -= 1
        if self.jump_booster_time > 0:
            self.jump_booster_time -= 1

        self.vert_speed += GRAVITY
        self.rect.y += self.vert_speed
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vert_speed > 0 and self.rect.bottom - self.vert_speed <= platform.rect.top + 5:
                    self.rect.bottom = platform.rect.top
                    self.vert_speed = 0
                    self.on_ground = True

        if self.rect.top > screen_height:
            return False
        return True


    def jump(self):
        """
        Прыжок только если котик на земле
        Прыжок вдвое выше при наличии бустера
        """

        if self.on_ground:
            current_jump = JUMP if self.jump_booster_time == 0 else JUMP * 2
            self.vert_speed = current_jump


    def move(self, dx):
        """
        Сдвигает котика по горизонтали с учётом SPEED
        Скорость вдвое больше при наличии бустера
        """

        current_speed = SPEED if self.speed_booster_time == 0 else SPEED * 2
        self.rect.x += dx * current_speed


    def draw(self, screen, camera):
        """
        Отрисовывает котика
        """

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


    def set_skin(self, skin_name):
        """
        Меняет цвет котика
        """

        global CAT_COLOR
        if skin_name in CAT_SKINS:
            CAT_COLOR = CAT_SKINS[skin_name]

    def draw_boosters(self, screen, x, y):
        """
        Отрисовывает шкалы бустеров (если есть)
        """

        timer = 400
        bar_width = 200
        bar_height = 30
        shift = 0

        active_boosters = [
            (self.speed_booster_time, SPEED_COLOR),
            (self.shield_booster_time, SHIELD_COLOR),
            (self.jump_booster_time, JUMP_COLOR)
        ]

        for time, color in active_boosters:
            if time > 0:
                fill_width = int(bar_width * (time / timer))
                pygame.draw.rect(screen, color, (x, y + shift, fill_width, bar_height))
                pygame.draw.rect(screen, WHITE, (x, y + shift, bar_width, bar_height), 2)
                shift += 40


# Платформы
class Platform:
    def __init__(self, x, y, length):
        """
        Создаёт платформу: прямоугольник с заданной длиной и фиксированной высотой
        """

        self.rect = pygame.Rect(x, y, length, 200)

    def draw(self, screen, camera):
        """
        Отрисовывает платформу - земля с травой
        """

        cam_move = self.rect.x - camera
        brown_height = self.rect.height
        pygame.draw.rect(screen, GROUND_BROWN, (cam_move, self.rect.y, self.rect.width, brown_height))
        pygame.draw.rect(screen, GROUND_GREEN, (cam_move, self.rect.y, self.rect.width, self.rect.height - 120))



# Шипы
class Spike:
    def __init__(self, x, y):
        """
        Инициализирует шип
        """

        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, screen, camera):
        """
        Отрисовывает шип: треугольник
        """
        cam_move = self.rect.x - camera
        pygame.draw.polygon(screen, SPIKE, [
            (cam_move + 25, self.rect.y),
            (cam_move, self.rect.y + 50),
            (cam_move + 50, self.rect.y + 50)
        ])



# Жизни
class Heart:
    def __init__(self, x, y, size=20):
        """
        Инициализирует сердечко-жизнь
        """

        self.x = x
        self.y = y
        self.size = size
        self.image = load_image("images/heart.png", (75, 75))

    def draw(self, screen):
        """
        Отрисовывает сердце: картинка или заглушка
        """
        if self.image:
            screen.blit(self.image, (
                self.x - self.size,
                self.y - self.size
            ))
        else:
            left_center = (self.x - self.size // 2, self.y)
            right_center = (self.x + self.size // 2, self.y)

            pygame.draw.circle(screen, RED, left_center, self.size // 2)
            pygame.draw.circle(screen, RED, right_center, self.size // 2)

            triangle_points = [
                (self.x - self.size, self.y),  # Левый край
                (self.x + self.size, self.y),  # Правый край
                (self.x, self.y + int(self.size * 1.5))  # Нижний кончик
            ]
            pygame.draw.polygon(screen, RED, triangle_points)



# Птица
BIRD_FLYING = 0
BIRD_DOWN = 1
BIRD_UP = 2

class Bird:
    def __init__(self, x, y):
        """
        Создаёт объект птицы: задаёт прямоугольник, загружает спрайт
        """

        self.rect = pygame.Rect(x, y, 90, 90)
        self.image = load_image("images/bird.png", (90, 90))
        self.attacked = False

        self.state = BIRD_FLYING
        self.height = y
        self.speed = -7

        self.down_speed = [0, 0]
        self.detect = 500
        self.range_down = 200


    def update(self, player_rect):
        """
        Обновление состояний: полет - вниз на игрока - вверх на свою высоту
        """

        if self.attacked:
            return

        if self.state == BIRD_FLYING:
            self.rect.x +=self.speed

            bird_center_x = self.rect.centerx
            player_center_x = player_rect.centerx

            # Обнаружение игрока
            if abs(player_center_x - bird_center_x) < self.detect:
                if player_rect.y > self.rect.y:
                    self.state = BIRD_DOWN

                    # Изменение направления
                    dx = player_center_x - bird_center_x
                    dy = player_rect.centery - self.rect.centery

                    distance = max(1, (dx**2 + dy**2)**0.5)
                    self.down_speed[0] = (dx / distance) * 8
                    self.down_speed[1] = (dy / distance) * 8

        elif self.state == BIRD_DOWN:
            self.rect.x += self.down_speed[0]
            self.rect.y += self.down_speed[1]

            if self.rect.y > self.height + self.range_down:
                self.state = BIRD_UP

        elif self.state == BIRD_UP:
            self.rect.x += self.speed
            self.rect.y -= 3

            if self.rect.y <= self.height:
                self.rect.y = self.height
                self.state = BIRD_FLYING


    def draw(self, screen, camera):
        """
        Отрисовывает птицу: картинка или заглушка
        """

        if not self.attacked:
            cam_move = self.rect.x - camera
            if self.image:
                screen.blit(self.image, (cam_move, self.rect.y))
            else:
                # Тело
                pygame.draw.rect(screen, BIRD, (cam_move + 25, self.rect.y + 25, 45, 45))

                # Клюв
                pygame.draw.polygon(screen, BIRD, [
                    (cam_move + 25, self.rect.y + 35),
                    (cam_move + 25, self.rect.y + 50),
                    (cam_move + 10, self.rect.y + 40)
                ])

                # Крыло
                pygame.draw.polygon(screen, BIRD, [
                    (cam_move + 35, self.rect.y + 25),
                    (cam_move + 60, self.rect.y + 25),
                    (cam_move + 45, self.rect.y)
                ])

                # Глаз
                pygame.draw.circle(screen, BLACK, (cam_move + 35, self.rect.y + 35), 3)



# Бустеры
class Booster:
    def __init__(self, x, y):
        """
        Родительский класс бустера
        """

        self.rect = pygame.Rect(x, y, 80, 80)
        self.image = load_image("images/booster.png", (80, 80))
        self.collected = False

    def draw(self, screen, camera):
        """
        Отрисовывает бустер: картинка или круг-заглушка
        """
        if not self.collected:
            cam_move = self.rect.x - camera
            if self.image:
                screen.blit(self.image, (cam_move, self.rect.y))
            else:
                pygame.draw.circle(screen, BOOSTER, (cam_move + 30, self.rect.y + 30), 28)

    def apply(self, player):
        """
        Игрок получает эффект (метод переопределяется в классах-наследниках)
        """

        pass


class SpeedBooster(Booster):
    """
    Бустер скорости на 400 кадров (наследник от Booster)
    """

    def apply(self, player):
        player.speed_booster_time = 400

class ShieldBooster(Booster):
    """
    Бустер щит на 400 кадров (наследник от Booster)
    """

    def apply(self, player):
        player.shield_booster_time = 400

class JumpBooster(Booster):
    """
    Бустер прыжка на 400 кадров (наследник от Booster)
    """

    def apply(self, player):
        player.jump_booster_time = 400

ALL_BOOSTERS = [SpeedBooster, ShieldBooster, JumpBooster]

def create_random_booster(x, y):
    """
    Создание случайного бустера
    """

    booster_class = random.choice(ALL_BOOSTERS)
    return booster_class(x, y)
