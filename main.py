import pygame
import json
import random
import os
import sys


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
    """
    Загружает изображение, масштабирует до size, возвращает None при ошибке
    """

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


# Преподаватель
class Teacher:
    def __init__(self, x, y):
        """
        Создаёт преподавателя: прямоугольник, спрайт, флаг interacted=False
        """

        self.rect = pygame.Rect(x, y, 200, 200)
        self.image = load_image("images/teacher.png", (200, 200))
        self.interacted = False

    def draw(self, screen, camera):
        """
        Отрисовывает учителя: картинка или цветной прямоугольник
        """

        cam_move = self.rect.x - camera
        if self.image:
            screen.blit(self.image, (cam_move, self.rect.y))
        else:
            pygame.draw.rect(screen, TEACHER, (cam_move, self.rect.y, 200, 200))


# Игрок (котик)
class Player:
    def __init__(self, x, y):
        """
        Инициализирует котика: позиция, скорость, флаг on_ground
        """

        self.rect = pygame.Rect(x, y, 100, 100)
        self.vert_speed = 0
        self.on_ground = False

    def update(self, platforms):
        """
        Применяет гравитацию, проверяет коллизии с платформами, возвращает False при падении в яму
        """

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
        """
        Задаёт отрицательную вертикальную скорость (прыжок), только если котик на земле
        """

        if self.on_ground:
            self.vert_speed = JUMP

    def move(self, dx):
        """
        Сдвигает котика по горизонтали с учётом SPEED
        """

        self.rect.x += dx * SPEED

    def draw(self, screen, camera):
        """
        Рисует котика
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


# Платформы
class Platform:
    def __init__(self, x, y, length):
        """
        Создаёт платформу: прямоугольник с заданной длиной и фиксированной высотой
        """

        self.rect = pygame.Rect(x, y, length, 200)

    def draw(self, screen, camera):
        """
        Рисует платформу - земля с травой
        """

        cam_move = self.rect.x - camera
        brown_height = self.rect.height
        pygame.draw.rect(screen, GROUND_BROWN, (cam_move, self.rect.y, self.rect.width, brown_height))
        pygame.draw.rect(screen, GROUND_GREEN, (cam_move, self.rect.y, self.rect.width, self.rect.height - 120))


# Создание уровня
def generate_platforms(start_platform):
    """
    Генерирует часть уровня - 5 платформ
    Случайная высота, вероятность появления рыбки/преподавателя
    """

    new_platforms = []
    new_fish = []
    new_teachers = []

    for _ in range(5):
        length = random.randint(400, 800)
        height = SCREEN_HEIGHT - random.randint(250, 350)
        new_platforms.append(Platform(start_platform, height, length))

        chance = random.random()

        if chance < 0.4:
            fish = start_platform + random.randint(50, length - 80)
            new_fish.append(Fish(fish, height - random.randint(60, 250)))

        elif chance < 0.7:
            teacher = start_platform + random.randint(50, length - 160)
            new_teachers.append(Teacher(teacher, height - 180))

        hole = random.randint(150, 250)
        start_platform += length + hole

    return new_platforms, new_fish, new_teachers, start_platform


def load_questions(discipline_name="kol"):
    """
    Загружает вопросы из data/{name}.json, валидирует формат, завершает игру при ошибке
    """

    path = os.path.join("data", f"{discipline_name}.json")
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            questions = data.get("questions", [])
            if not questions:
                print("Список вопросов пуст")
                sys.exit(1)
            return questions
    except FileNotFoundError:
        print("Файл не найден")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Неверный формат файла")
        sys.exit(1)


# Создание начального уровня
camera = 0
platforms, all_fish, all_teachers, next_platform = generate_platforms(0)

fish_count = 0

pause = False
active_teacher = None
questions = load_questions("kol")
current_question = None

question_state = 1  # 1 - вопрос, 2 - ответ, 3 - результат
last_answer_correct = False
button_show_answer = None
button_correct_answer = None
button_wrong_answer = None
button_continue = None


def draw_button(screen, x, y, width, height, text, color, text_color=WHITE, font_size=None):
    """
    Рисует кнопку с рамкой, текстом по центру, возвращает Rect для кликов
    """

    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=10)
    fnt = font if font_size is None else pygame.font.Font(None, font_size)
    text_surf = fnt.render(text, True, text_color)
    screen.blit(text_surf, (x + width // 2 - text_surf.get_width() // 2,
                           y + height // 2 - text_surf.get_height() // 2))
    return pygame.Rect(x, y, width, height)


def parse_answer(answer_data, max_line_length=60):
    """
    Принимает строку/список/\n, возвращает список строк для отрисовки с переносом
    """
    if isinstance(answer_data, list):
        result = []
        for item in answer_data:
            if len(item) <= max_line_length:
                result.append(item)
            else:
                words = item.split()
                current = ""
                for word in words:
                    if len(current) + len(word) + 1 <= max_line_length:
                        current += (" " if current else "") + word
                    else:
                        if current:
                            result.append(current)
                        current = word
                if current:
                    result.append(current)
        return result
    elif isinstance(answer_data, str):
        lines = answer_data.split("\n")
        result = []
        for line in lines:
            if len(line) <= max_line_length:
                result.append(line)
            else:
                words = line.split()
                current = ""
                for word in words:
                    if len(current) + len(word) + 1 <= max_line_length:
                        current += (" " if current else "") + word
                    else:
                        if current:
                            result.append(current)
                        current = word
                if current:
                    result.append(current)
        return result
    else:
        return [str(answer_data)]

# Главная рабочая часть
font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
FPS = 60
clock = pygame.time.Clock()
player = Player(100, SCREEN_HEIGHT - 600)
running = True

while running:
    # Действия кнопок
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                player.jump()
            if event.key == pygame.K_ESCAPE:
                running = False

    # Игра на паузе (задается вопрос)
    if pause:
        # Отрисовка
        screen.fill(SKY)
        for platform in platforms:
            platform.draw(screen, camera)
        for fish in all_fish:
            fish.draw(screen, camera)
        for teacher in all_teachers:
            teacher.draw(screen, camera)
        player.draw(screen, camera)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = font.render("Встреча с преподавателем", True, WARNING)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        answer_start_y = 120
        if current_question:
            question_text = current_question["question"]
            lines = [question_text[i:i+60] for i in range(0, len(question_text), 60)]
            question_y = 120
            for line in lines:
                question_surf = font.render(line, True, WHITE)
                screen.blit(question_surf, (SCREEN_WIDTH // 2 - question_surf.get_width() // 2, question_y))
                question_y += 50
            answer_start_y = question_y + 30

        button_show_answer = None
        button_correct_answer = None
        button_wrong_answer = None
        button_continue = None

        # Вопрос
        if question_state == 1:
            button_show_answer = draw_button(screen,
                                             SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50,
                                             300, 60, "Показать ответ", WARNING)

        # Ответ
        elif question_state == 2:
            raw_answer = current_question.get("answer", "")
            answer_lines = parse_answer(raw_answer, max_line_length=60)
            answer_y = answer_start_y
            for line in answer_lines:
                answer_surf = font.render(line, True, RIGHT)
                text_x = max(SCREEN_WIDTH * 0.05,
                             SCREEN_WIDTH // 2 - answer_surf.get_width() // 2)
                text_x = min(text_x, SCREEN_WIDTH * 0.95 - answer_surf.get_width())
                screen.blit(answer_surf, (SCREEN_WIDTH // 2 - answer_surf.get_width() // 2, answer_y))
                answer_y += 50

            button_correct_answer = draw_button(screen,
                                                SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT - 150,
                                                320, 70, "Мой ответ ВЕРНЫЙ", RIGHT, font_size=40)
            button_wrong_answer = draw_button(screen,
                                                SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT - 150,
                                                320, 70, "Мой ответ НЕВЕРНЫЙ", WRONG, font_size=40)

        # Результат
        elif question_state == 3:
            message = "Так держать!" if last_answer_correct else "Повтори материал"
            color = RIGHT if last_answer_correct else WRONG
            message_surf = font.render(message, True, color)
            screen.blit(message_surf, (SCREEN_WIDTH // 2 - message_surf.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
            button_continue = draw_button(screen,
                                      SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 150,
                                      300, 70, "Продолжить", TEXT, font_size=40)

        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if question_state == 1 and button_show_answer and button_show_answer.collidepoint(mouse_position):
                    question_state = 2
                elif question_state == 2 and button_correct_answer and button_correct_answer.collidepoint(mouse_position):
                    last_answer_correct = True
                    question_state = 3
                elif question_state == 2 and button_wrong_answer and button_wrong_answer.collidepoint(mouse_position):
                    last_answer_correct = False
                    question_state = 3
                elif question_state == 3 and button_continue and button_continue.collidepoint(mouse_position):
                    pause = False
                    question_state = 1
                    current_question = None


        pygame.display.flip()
        clock.tick(FPS)
        continue


    # Направление движения
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move(1)

    # Действия при падении в яму (рестарт)
    if not player.update(platforms):
        player = Player(100, SCREEN_HEIGHT - 600)
        camera = 0
        platforms, all_fish, all_teachers, next_platform = generate_platforms(0)
        fish_count = 0
        pause = False
        question_state = 1

    # Собираем рыбу
    for fish in all_fish:
        if not fish.collected and player.rect.colliderect(fish.rect):
            fish.collected = True
            fish_count += 1

    # Столкновение с преподавателем
    for teacher in all_teachers:
        if not teacher.interacted and player.rect.colliderect(teacher.rect):
            pause = True
            active_teacher = teacher
            teacher.interacted = True
            if questions:
                current_question = random.choice(questions)
            break

    # Движение камеры
    camera_place = player.rect.centerx - SCREEN_WIDTH // 3
    camera += (camera_place - camera) * 0.1
    if camera < 0:
        camera = 0

    if player.rect.right > next_platform - SCREEN_WIDTH * 2:
        new_platforms, new_fish, new_teachers, next_platform = generate_platforms(next_platform)
        platforms.extend(new_platforms)
        all_fish.extend(new_fish)
        all_teachers.extend(new_teachers)

    platforms = [platform for platform in platforms if platform.rect.right > camera - 200]
    all_fish = [fish for fish in all_fish if fish.rect.right > camera - 200]

    # Отрисовка
    screen.fill(SKY)
    for platform in platforms:
        platform.draw(screen, camera)
    for fish in all_fish:
        fish.draw(screen, camera)
    for teacher in all_teachers:
        teacher.draw(screen, camera)
    player.draw(screen, camera)

    score_fish = font.render(f"Рыбок собрано: {fish_count}", True, TEXT)
    screen.blit(score_fish, (15, 15))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()