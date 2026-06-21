import pygame


# Интерфейс
WHITE = (255, 255, 255)
BUTTON_CURSOR = (80, 80, 100)
BUTTON = (40, 40, 50)


def draw_button(screen, x, y, width, height, text, font, cursor=False):
    """
    Отрисовывает кнопку с текстом по центру
    """

    color = BUTTON_CURSOR if cursor else BUTTON
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    text = font.render(text, True, WHITE)
    screen.blit(text, (
        rect.centerx - text.get_width() // 2,
        rect.centery - text.get_height() // 2
    ))

    return rect


def create_button(screen, center_x, center_y, text, font, mouse_pos, width=400, height=80):
    """
    "Оживляет" кнопку - подсветка при наведении курсором
    """

    x = center_x - width // 2
    y = center_y - height // 2

    rect = pygame.Rect(x, y, width, height)
    curs_on_but = rect.collidepoint(mouse_pos)

    draw_button(screen, x, y, width, height, text, font, cursor=curs_on_but)
    return rect