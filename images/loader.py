import pygame
import os


# Загрузка изображений
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