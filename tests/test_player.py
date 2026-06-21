import pygame
from algorithms.objects import Player, SPEED, JUMP


pygame.init()

def test_player_position():
    """
    Проверка начальных позиции, скорости и расстояния от земли
    """

    player = Player(100, 200)
    assert player.rect.x == 100
    assert player.rect.y == 200
    assert player.vert_speed == 0
    assert player.on_ground is False


def test_player_move_with_speed_boost():
    """
    Проверка бустера скорости
    """

    player = Player(100, 100)
    player.speed_booster_time = 100
    player.move(1)
    assert player.rect.x == 100 + SPEED * 2


def test_player_jump_with_boost():
    """
    Проверка бустера прыжка
    """

    player = Player(100, 100)
    player.on_ground = True
    player.jump_booster_time = 100
    player.jump()
    assert player.vert_speed == JUMP * 2


def test_player_jump_not_on_ground():
    """
    Проверка невозможности прыжка в воздухе
    """

    player = Player(100, 100)
    player.on_ground = False
    player.jump()
    assert player.vert_speed == 0

