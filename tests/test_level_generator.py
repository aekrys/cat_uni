import pygame
from algorithms.level_generator import generate_platforms


pygame.init()

def test_generate_returns_6_values():
    """
        Проверка возвращения функцией 6 значений
    """

    result = generate_platforms(0, 1080)
    assert len(result) == 6


def test_first_platform_is_clear():
    """
    Проверка отсутствия рыбок и шипов на первой платформе
    """

    platforms, fish, spikes, birds, boosters, next_p = generate_platforms(0, 1080)
    first_platform = platforms[0]
    for f in fish:
        assert f.rect.x < first_platform.rect.x or f.rect.x > first_platform.rect.right
    for s in spikes:
        assert s.rect.x < first_platform.rect.x or s.rect.x > first_platform.rect.right