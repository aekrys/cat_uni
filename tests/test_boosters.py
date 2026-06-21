from algorithms.objects import SpeedBooster, ShieldBooster, JumpBooster, Player, create_random_booster, Booster

def test_speed_booster_apply():
    player = Player(100, 100)
    booster = SpeedBooster(0, 0)
    booster.apply(player)
    assert player.speed_booster_time == 400


def test_shield_booster_apply():
    player = Player(100, 100)
    booster = ShieldBooster(0, 0)
    booster.apply(player)
    assert player.shield_booster_time == 400


def test_jump_booster_apply():
    player = Player(100, 100)
    booster = JumpBooster(0, 0)
    booster.apply(player)
    assert player.jump_booster_time == 400


def test_create_random_booster_type():
    booster = create_random_booster(100, 100)
    assert isinstance(booster, (SpeedBooster, ShieldBooster, JumpBooster))