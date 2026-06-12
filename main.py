import pygame

from algorithms import (Player, Fish, Platform, Spike, Heart, Bird,
                        generate_platforms, camera_move, CAT_SKINS,
                        load_record, save_record)
from algorithms.button import create_button

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

# Царапины
RED = (225, 50, 50)


# Создание начального уровня
camera = 0
platforms, all_fish, all_spikes, all_birds, next_platform = generate_platforms(0, SCREEN_HEIGHT)
fish_count = 0
lives = 3
attack_timer = 0
best_score = load_record()


font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
font_title = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.2))
FPS = 60
clock = pygame.time.Clock()
player = Player(100, SCREEN_HEIGHT - 600)
running = True

def start_game():
    global player, camera, platforms, all_fish, all_spikes, all_birds, next_platform, fish_count, lives, attack_timer, best_score
    player = Player(100, SCREEN_HEIGHT - 600)
    player.set_skin(current_skin)
    camera = 0
    platforms, all_fish, all_spikes, all_birds, next_platform = generate_platforms(0, SCREEN_HEIGHT)

    if fish_count > best_score:
        best_score = fish_count
        save_record(best_score)

    fish_count = 0
    lives = 3
    attack_timer = 0


def claw(screen, x, y):
    for i, size in enumerate([3, 4, 2]):
        shift_x = i * 15
        start_x = x + 10 + shift_x
        start_y = y + 60 + i * 5
        end_x = x + 50 + shift_x
        end_y = y + 10 + i * 5

        pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), size)



# Главная рабочая часть
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
            if event.key in (pygame.K_s, pygame.K_DOWN):
                attack_timer = 10

            if event.key == pygame.K_SPACE:
                if game_state == STATE_PLAYING:
                    game_state = STATE_PAUSE
                elif game_state == STATE_PAUSE:
                    game_state = STATE_PLAYING
            if event.key == pygame.K_ESCAPE:
                if game_state == STATE_MENU:
                    running = False
                else:
                    game_state = STATE_MENU

        # Мышка
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == STATE_MENU:
                if button_start.collidepoint(event.pos):
                    start_game()
                    game_state = STATE_PLAYING
                elif button_skin_change.collidepoint(event.pos):
                    game_state = STATE_SKIN_CHANGE
                elif button_quit.collidepoint(event.pos):
                    running = False

            elif game_state == STATE_PAUSE:
                if button_resume.collidepoint(event.pos):
                    game_state = STATE_PLAYING
                elif button_restart.collidepoint(event.pos):
                    game_state = STATE_PLAYING
                    start_game()
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
            if fish_count > best_score:
                best_score = fish_count
                save_record(best_score)
            start_game()

        # Собираем рыбу
        for fish in all_fish:
            if not fish.collected and player.rect.colliderect(fish.rect):
                fish.collected = True
                fish_count += 1

        # Движение птиц
        for bird in all_birds:
            bird.update(player.rect)

        # Столкновение с шипами
        for spike in all_spikes:
            if player.rect.colliderect(spike.rect):
                lives -= 1
                if lives < 1:
                    start_game()
                else:
                    player.rect.x -= 150
                    player.rect.y = SCREEN_HEIGHT - 500
                break

        # Столкновение с птицами
        for bird in all_birds:
            if not bird.attacked and player.rect.colliderect(bird.rect):
                bird.attacked = True
                lives -= 1
                if lives < 1:
                    start_game()
                else:
                    player.rect.x -= 150
                    player.rect.y = SCREEN_HEIGHT - 500
                break

        # Атака птицы
        if attack_timer > 0:
            attack_timer -= 1

            attack_rect = pygame.Rect(player.rect.right - 10, player.rect.y + 10, 80, 80)
            for bird in all_birds:
                if not bird.attacked and attack_rect.colliderect(bird.rect):
                    bird.attacked = True


        # Камера
        camera = camera_move(camera, player.rect.centerx, SCREEN_WIDTH)

        if player.rect.right > next_platform - SCREEN_WIDTH * 2:
            new_platforms, new_fish, new_spikes, new_birds, next_platform = generate_platforms(next_platform, SCREEN_HEIGHT)
            platforms.extend(new_platforms)
            all_fish.extend(new_fish)
            all_spikes.extend(new_spikes)
            all_birds.extend(new_birds)

        # Очистка для оптимизации
        platforms = [platform for platform in platforms if platform.rect.right > camera - 200]
        all_fish = [fish for fish in all_fish if fish.rect.right > camera - 200]
        all_spikes = [spike for spike in all_spikes if spike.rect.right > camera - 200]
        all_birds = [bird for bird in all_birds if bird.rect.right > camera - 200]

        # Отрисовка
        screen.fill(SKY)
        for platform in platforms:
            platform.draw(screen, camera)
        for fish in all_fish:
            fish.draw(screen, camera)
        for spike in all_spikes:
            spike.draw(screen, camera)
        for bird in all_birds:
            bird.draw(screen, camera)
        player.draw(screen, camera)

        if attack_timer > 0:
            claw(screen, player.rect.right - 10 - camera, player.rect.y + 10)

        score_fish = font.render(f"Рыбок собрано: {fish_count}", True, TEXT)
        screen.blit(score_fish, (15, 15))

        record_text = font.render(f"Рекорд: {best_score}", True, TEXT)
        screen.blit(record_text, (15, 50))

        heart_size = 20
        heart_space = 80
        first_heart_x = SCREEN_WIDTH - 250

        for i in range(lives):
            heart = Heart(first_heart_x + i * heart_space, 30, heart_size)
            heart.draw(screen)


    if game_state == STATE_MENU:
        screen.fill(SKY)

        title = font_title.render("CatUni", True, TEXT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2,
                            SCREEN_HEIGHT // 2 - 350))

        record_text = font.render(f"Рекорд: {best_score}", True, TEXT)
        screen.blit(record_text, (SCREEN_WIDTH // 2 - record_text.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - 200))

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
                                 SCREEN_HEIGHT // 2 - 300))

        center_x = SCREEN_WIDTH // 2

        # Кнопка "Продолжить"
        center_y = SCREEN_HEIGHT // 2 - 40
        button_resume = create_button(screen, center_x, center_y, "Продолжить", font, mouse_pos)

        # Кнопка "Начать заново"
        center_y = SCREEN_HEIGHT // 2 + 80
        button_restart = create_button(screen, center_x, center_y, "Начать заново", font, mouse_pos)

        # Кнопка "Закончить игру"
        center_y = SCREEN_HEIGHT // 2 + 200
        button_menu = create_button(screen, center_x, center_y, "Закончить игру", font, mouse_pos)


    elif game_state == STATE_SKIN_CHANGE:
        screen.fill(SKY)

        skin_text = font_title.render("Выбери цвет котика", True, TEXT)
        screen.blit(skin_text, (SCREEN_WIDTH // 2 - skin_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - 350))

        skin_names = list(CAT_SKINS.keys())
        skin_size = 200
        gap = 50
        width = len(skin_names) * skin_size + (len(skin_names) - 1) * gap
        first_skin_x = SCREEN_WIDTH // 2 - width // 2
        skin_y = SCREEN_HEIGHT // 2 - 150

        skin_rects = []

        # Выбор цвета котика
        for i, skin_name in enumerate(skin_names):
            x = first_skin_x + i * (skin_size + gap)

            color = CAT_SKINS[skin_name]
            skin_rect = pygame.Rect(x, skin_y, skin_size, skin_size)

            border_color = GREEN if skin_name == current_skin else WHITE
            border_width = 5 if skin_name == current_skin else 3

            pygame.draw.rect(screen, color, skin_rect, border_radius=20)
            pygame.draw.rect(screen, border_color, skin_rect, border_width, border_radius=20)

            skin_color = font.render(skin_name.capitalize(), True, TEXT)
            screen.blit(skin_color, (x + skin_size // 2 - skin_color.get_width() // 2,
                                skin_y + skin_size + 15))

            skin_rects.append((skin_rect, skin_name))


        # Котик выбранного цвета на платформе
        player.rect.x = SCREEN_WIDTH // 2 - 150
        player.rect.y = SCREEN_HEIGHT // 2 + 150
        player.set_skin(current_skin)
        player.draw(screen, 0)

        platform = Platform(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 250, 400)
        platform.draw(screen, 0)


        # Возвращаемся в меню
        center_x = SCREEN_WIDTH // 2 + 500
        center_y = SCREEN_HEIGHT // 2 + 350
        button_back = create_button(screen, center_x, center_y, "Назад в меню", font, mouse_pos)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()