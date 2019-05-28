import random
import pygame
import sys

from pygame.locals import *

# constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# colors
TEXT_COLOR = (255, 0, 0)  # red
BACKGROUND_COLOR = (50, 100, 120)  # TODO: картинку на бэкграунд

FPS = 40

# magic
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 6
PLAYER_MOVE_RATE = 12


def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate()
                return


def player_has_hit_baddie(player, baddies):
    for b in baddies:
        if player.colliderect(b['rect']):
            return True
    return False


def draw_text(text, font, surface, x, y):
    text_object = font.render(text, 1, TEXT_COLOR)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)


def game_loop():
    top_score = 0
    while True:
        # set up the start of the game
        baddies = []
        score = 0
        player_rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        move_left = move_right = move_up = move_down = False
        reverse_cheat = slow_cheat = False
        baddie_add_counter = 0
        pygame.mixer.music.play(-1, 0.0)

        while True:  # the game loop runs while the game part is playing
            score += 1  # increase score

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == ord('z'):
                        reverse_cheat = True
                    if event.key == ord('x'):
                        slow_cheat = True
                    if event.key == K_LEFT or event.key == ord('a'):
                        move_right = False
                        move_left = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_left = False
                        move_right = True
                    if event.key == K_UP or event.key == ord('w'):
                        move_down = False
                        move_up = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_up = False
                        move_down = True

                if event.type == KEYUP:
                    if event.key == ord('z'):
                        reverse_cheat = False
                        score = 0
                    if event.key == ord('x'):
                        slow_cheat = False
                        score = 0
                    if event.key == K_ESCAPE:
                        terminate()

                    if event.key == K_LEFT or event.key == ord('a'):
                        move_left = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_right = False
                    if event.key == K_UP or event.key == ord('w'):
                        move_up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_down = False

                if event.type == MOUSEMOTION:
                    # If the mouse moves, move the player where the cursor is.
                    player_rect.move_ip(event.pos[0] - player_rect.centerx, event.pos[1] - player_rect.centery)

            # Add new baddies at the top of the screen, if needed.
            if not reverse_cheat and not slow_cheat:
                baddie_add_counter += 1
            if baddie_add_counter == ADD_NEW_BADDIE_RATE:
                baddie_add_counter = 0
                baddie_size = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
                new_baddie = {
                    'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH - baddie_size), 0 - baddie_size, baddie_size,
                                        baddie_size),
                    'speed': random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                    'surface': pygame.transform.scale(enemy_image, (baddie_size, baddie_size)),
                    }

                baddies.append(new_baddie)

            # Move the player around.
            if move_left and player_rect.left > 0:
                player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
            if move_right and player_rect.right < WINDOW_WIDTH:
                player_rect.move_ip(PLAYER_MOVE_RATE, 0)
            if move_up and player_rect.top > 0:
                player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
            if move_down and player_rect.bottom < WINDOW_HEIGHT:
                player_rect.move_ip(0, PLAYER_MOVE_RATE)

            # Move the mouse cursor to match the player.
            pygame.mouse.set_pos(player_rect.centerx, player_rect.centery)

            # Move the baddies down.
            for b in baddies:
                if not reverse_cheat and not slow_cheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverse_cheat:
                    b['rect'].move_ip(0, -5)
                elif slow_cheat:
                    b['rect'].move_ip(0, 1)

            # Delete baddies that have fallen past the bottom.
            for b in baddies[:]:
                if b['rect'].top > WINDOW_HEIGHT:
                    baddies.remove(b)

            # Draw the game world on the window.
            window_surface.fill(BACKGROUND_COLOR)

            # Draw the score and top score.
            draw_text('Score: %s' % (score), font, window_surface, 10, 0)
            draw_text('Top Score: %s' % (top_score), font, window_surface, 10, 40)

            # Draw the player's rectangle
            window_surface.blit(player_image, player_rect)

            background_image = pygame.image.load("../drawable/backgrounds/background1.jpg")
            background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

            window_surface.blit(background_image, [0, 0])

            # Draw each baddie
            for b in baddies:
                window_surface.blit(b['surface'], b['rect'])

            pygame.display.update()

            # Check if any of the baddies have hit the player.
            if player_has_hit_baddie(player_rect, baddies):
                if score > top_score:
                    top_score = score  # set new top score
                break

            main_clock.tick(FPS)

        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()
        game_over_sound.play()

        draw_text('GAME OVER', font, window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        draw_text('Press a key to play again.', font, window_surface, (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 50)
        pygame.display.update()
        wait_for_player_to_press_key()

        game_over_sound.stop()


if __name__ == "__main__":
    # initiation
    # TODO: если инициализаций будет много, то их надо будет разбить на мелкие функции

    # set up pygame, the window, and the mouse cursor
    pygame.init()
    main_clock = pygame.time.Clock()
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    background_image = pygame.image.load("../drawable/backgrounds/main_menu.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    window_surface.blit(background_image, [0, 0])

    pygame.display.set_caption('Meow Hero')
    pygame.mouse.set_visible(False)

    # set up fonts
    font = pygame.font.SysFont(None, 48)

    # set up sounds
    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')
    pygame.mixer.music.load('../sound/main_theme.mp3')

    # set up images
    player_image = pygame.image.load('../drawable/cat_hero.png')
    # TODO: scale by window size
    player_image = pygame.transform.scale(player_image, (100, 100))

    player_rect = player_image.get_rect()
    enemy_image = pygame.image.load('../drawable/dog_enemy.png')

    # show the "Start" screen
    draw_text('Meow Hero', font, window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
    draw_text('Press any key to start ^_^', font, window_surface, (WINDOW_WIDTH / 3) - 30, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()

    # TODO: здесь отрисовать меню

    wait_for_player_to_press_key()
    game_loop()
