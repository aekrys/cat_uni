import random
from algorithms.objects import Platform, Fish


# Создание уровня
def generate_platforms(start_platform, screen_height):
    """
    Генерирует часть уровня - 5 платформ
    Случайная высота, вероятность появления рыбки
    """

    new_platforms = []
    new_fish = []

    for _ in range(5):
        length = random.randint(400, 800)
        height = screen_height - random.randint(250, 350)
        new_platforms.append(Platform(start_platform, height, length))

        chance = random.random()

        if chance < 0.4:
            fish = start_platform + random.randint(50, length - 80)
            new_fish.append(Fish(fish, height - random.randint(60, 250)))

        hole = random.randint(150, 250)
        start_platform += length + hole

    return new_platforms, new_fish, start_platform