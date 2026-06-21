import random
from algorithms.objects import Platform, Fish, Spike, Bird, Booster, create_random_booster


# Создание уровня
def generate_platforms(start_platform, screen_height):
    """
    Генерирует часть уровня - 5 платформ
    Случайная высота
    Вероятность появления рыбки, шипа, птицы и бустера
    """

    new_platforms = []
    new_fish = []
    new_spikes = []
    new_birds = []
    new_boosters = []

    for i in range(5):
        length = random.randint(400, 800)
        height = screen_height - random.randint(250, 350)
        new_platforms.append(Platform(start_platform, height, length))

        if i == 0:
            pass  # Первая платформа без объектов

        else:
            chance = random.random()

            if chance < 0.25:
                fish = start_platform + random.randint(50, length - 80)
                new_fish.append(Fish(fish, height - random.randint(60, 250)))

            elif chance < 0.55:
                spike = start_platform + random.randint(100, length - 150)
                new_spikes.append(Spike(spike, height - 50))

            elif chance < 0.8:
                bird_x = start_platform + random.randint(200, length - 100)
                bird_y = height - random.randint(150, 300)
                new_birds.append(Bird(bird_x, bird_y))

            elif chance < 0.9:
                booster_x = start_platform + random.randint(100, length - 100)
                booster_y = height - random.randint(100, 200)
                new_boosters.append(create_random_booster(booster_x, booster_y))

        hole = random.randint(150, 250)
        start_platform += length + hole

    return new_platforms, new_fish, new_spikes, new_birds, new_boosters, start_platform