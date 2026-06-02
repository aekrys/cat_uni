import pygame
from algorithms import Player, Fish, Platform, generate_platforms, camera_move, CAT_SKINS
from algorithms.button import draw_button, create_button

pygame.init()

# Константы экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("CatUni")

# Состояния игры
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSE = 2
STATE_SKIN_CHANGE = 3

game_state = STATE_MENU
current_skin = "orange"

# Цвет фона
SKY = (135, 206, 235)

# Интерфейс
TEXT = (40, 40, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (110, 240, 40)

# Создание начального уровня
camera = 0
platforms, all_fish,  next_platform = generate_platforms(0, SCREEN_HEIGHT)

fish_count = 0


# Главная рабочая часть
font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
font_title = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.2))
FPS = 60
clock = pygame.time.Clock()
player = Player(100, SCREEN_HEIGHT - 600)
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    # Действия кнопок
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Клавиатура
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                player.jump()
            if event.key == pygame.K_SPACE:
                if game_state == STATE_PLAYING:
                    game_state = STATE_PAUSE
                elif game_state == STATE_PAUSE:
                    game_state = STATE_PLAYING
            if event.key == pygame.K_ESCAPE:
                if game_state == STATE_PLAYING or game_state == STATE_PAUSE:
                    game_state = STATE_MENU
                else:
                    running = False

        # Мышка
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == STATE_MENU:
                if button_start.collidepoint(event.pos):
                    game_state = STATE_PLAYING
                elif button_skin_change.collidepoint(event.pos):
                    game_state = STATE_SKIN_CHANGE
                elif button_quit.collidepoint(event.pos):
                    running = False

            elif game_state == STATE_PAUSE:
                if button_resume.collidepoint(event.pos):
                    game_state = STATE_PLAYING
                elif button_menu.collidepoint(event.pos):
                    game_state = STATE_MENU

            elif game_state == STATE_SKIN_CHANGE:
                for skin_rect, skin_name in skin_rects:
                    if skin_rect.collidepoint(event.pos):
                        current_skin = skin_name
                        player.set_skin(skin_name)
                if button_back.collidepoint(event.pos):
                    game_state = STATE_MENU



    if game_state == STATE_PLAYING:
        # Направление движения
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move(1)

        # Действия при падении в яму (рестарт)
        if not player.update(platforms, SCREEN_HEIGHT):
            player = Player(100, SCREEN_HEIGHT - 600)
            camera = 0
            platforms, all_fish, next_platform = generate_platforms(0, SCREEN_HEIGHT)
            fish_count = 0

        # Собираем рыбу
        for fish in all_fish:
            if not fish.collected and player.rect.colliderect(fish.rect):
                fish.collected = True
                fish_count += 1

        # Камера
        camera = camera_move(camera, player.rect.centerx, SCREEN_WIDTH)

        if player.rect.right > next_platform - SCREEN_WIDTH * 2:
            new_platforms, new_fish, next_platform = generate_platforms(next_platform, SCREEN_HEIGHT)
            platforms.extend(new_platforms)
            all_fish.extend(new_fish)

        platforms = [platform for platform in platforms if platform.rect.right > camera - 200]
        all_fish = [fish for fish in all_fish if fish.rect.right > camera - 200]

        # Отрисовка
        screen.fill(SKY)
        for platform in platforms:
            platform.draw(screen, camera)
        for fish in all_fish:
            fish.draw(screen, camera)
        player.draw(screen, camera)

        score_fish = font.render(f"Рыбок собрано: {fish_count}", True, TEXT)
        screen.blit(score_fish, (15, 15))


    if game_state == STATE_MENU:
        screen.fill(SKY)

        title = font_title.render("CatUni", True, TEXT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2,
                            SCREEN_HEIGHT // 2 - 350))

        mouse_pos = pygame.mouse.get_pos()

        center_x = SCREEN_WIDTH // 2

        # Кнопка "Начать игру"
        center_y = SCREEN_HEIGHT // 2 - 40
        button_start = create_button(screen, center_x, center_y,"Начать игру", font, mouse_pos)

        # Кнопка "Изменить скин"
        center_y = SCREEN_HEIGHT // 2 + 80
        button_skin_change = create_button(screen, center_x, center_y, "Изменить скин", font, mouse_pos)

        # Кнопка "Выйти из игры"
        center_y = SCREEN_HEIGHT // 2 + 200
        button_quit = create_button(screen, center_x, center_y, "Выйти из игры", font, mouse_pos)


    elif game_state == STATE_PAUSE:
        # Отрисовка
        screen.fill(SKY)
        for platform in platforms:
            platform.draw(screen, camera)
        for fish in all_fish:
            fish.draw(screen, camera)
        player.draw(screen, camera)

        pause_text = font_title.render("ПАУЗА", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - 250))

        center_x = SCREEN_WIDTH // 2

        # Кнопка "Продолжить"
        center_y = SCREEN_HEIGHT // 2 - 40
        button_resume = create_button(screen, center_x, center_y, "Продолжить", font, mouse_pos)

        # Кнопка "В меню"
        center_y = SCREEN_HEIGHT // 2 + 80
        button_menu = create_button(screen, center_x, center_y, "В меню", font, mouse_pos)


    elif game_state == STATE_SKIN_CHANGE:
        screen.fill(SKY)

        skin_text = font_title.render("Выбери цвет котика", True, TEXT)
        screen.blit(skin_text, (SCREEN_WIDTH // 2 - skin_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - 250))

        skin_names = list(CAT_SKINS.keys())
        skin_size = 200
        gap = 50
        width = len(skin_names) * skin_size + (len(skin_names) - 1) * gap
        first_skin_x = SCREEN_WIDTH // 2 - width // 2
        skin_y = SCREEN_HEIGHT // 2 - 50

        skin_rects = []

        for i, skin_name in enumerate(skin_names):
            x = first_skin_x + i * (skin_size + gap)

            color = CAT_SKINS[skin_name]
            skin_rect = pygame.Rect(x, skin_y, skin_size, skin_size)

            # Обводка выбранного скина
            border_color = GREEN if skin_name == current_skin else WHITE
            border_width = 5 if skin_name == current_skin else 3

            pygame.draw.rect(screen, color, skin_rect, border_radius=20)
            pygame.draw.rect(screen, border_color, skin_rect, border_width, border_radius=20)

            skin_color = font.render(skin_name.capitalize(), True, TEXT)
            screen.blit(skin_color, (x + skin_size // 2 - skin_color.get_width() // 2,
                                skin_y + skin_size + 15))

            skin_rects.append((skin_rect, skin_name))

        center_x = SCREEN_WIDTH // 2 + 400
        center_y = SCREEN_HEIGHT // 2 + 300
        button_back = create_button(screen, center_x, center_y, "Назад в меню", font, mouse_pos)




    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()