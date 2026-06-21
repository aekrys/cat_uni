# Движение камеры
def camera_move(camera, centerx, screen_width):
    """
    Камера плавно следует за игроком
    "Плавно" благодаря коэффициенту 0.1, а не прыгает
    """

    camera_place = centerx - screen_width // 3
    camera += (camera_place - camera) * 0.1
    if camera < 0:
        camera = 0
    return camera