import re
import pygame
import screeninfo
import sys

from modules import objects, client, heroes
from pygame.locals import *

# taking screen W and H
for m in screeninfo.get_monitors():
    print(str(m))
    pattern = "\d*x\d*"
    WINDOW_WIDTH, WINDOW_HEIGHT = list(map(int, re.findall(pattern, str(m))[0].split('x')))

# constants, if need hardcoded
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600

# constant BG
background_image_in_game = pygame.image.load("../drawable/backgrounds/background1.jpg")
background_image_in_game = pygame.transform.scale(background_image_in_game, (WINDOW_WIDTH, WINDOW_HEIGHT))

# colors
COLOR_WHITE = (255, 255, 255)  # white

# magic
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 6
PLAYER_MOVE_RATE = 12
FPS = 40


def terminate():
    pygame.quit()
    sys.exit()


# TODO: it's pretty dumb
def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate()
                return


# TODO: remove this guy
def player_has_hit_baddie(player, baddies):
    for b in baddies:
        if player.colliderect(b['rect']):
            return True
    return False


def game_loop(window_surface):
    main_clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')
    pygame.mixer.music.load('../sound/main_theme.mp3')

    # set up images
    player_image = pygame.image.load('../drawable/sprites/cat_hero/cat_hero.png')

    # TODO: this guy
    meow_hero = heroes.MeowHero(player_image, WINDOW_WIDTH/12, WINDOW_HEIGHT/12)
    # TODO: init enemy

    wait_for_player_to_press_key()

    top_score = 0
    while True:
        score = 0

        move_left = move_right = move_up = move_down = False
        pygame.mixer.music.play(-1, 0.0)

        while True:  # the game loop runs while the game part is playing
            score += 1  # increase score

            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        # TODO: generate bullet here
                        pass
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

            # Move the player around.
            # if move_left and player_rect.left > 0:
            #     player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
            # if move_right and player_rect.right < WINDOW_WIDTH:
            #     player_rect.move_ip(PLAYER_MOVE_RATE, 0)
            # if move_up and player_rect.top > 0:
            #     player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
            # if move_down and player_rect.bottom < WINDOW_HEIGHT:
            #     player_rect.move_ip(0, PLAYER_MOVE_RATE)

            # Draw background
            window_surface.blit(background_image_in_game, [0, 0])

            # Draw the score and top score.
            draw_text('Score: %s' % (score), window_surface, 10, 0)
            draw_text('Top Score: %s' % (top_score), window_surface, 10, 40)

            # TODO: draw objects

            pygame.display.update()

            main_clock.tick(FPS)

        # TODO: return player to main menu
        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()
        game_over_sound.play()

        draw_text('GAME OVER', window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        draw_text('Press a key to play again.', window_surface, (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 50)
        pygame.display.update()
        wait_for_player_to_press_key()

        game_over_sound.stop()


def init_window(full_screen=False):  # set up pygame, the window, and the mouse cursor
    pygame.init()

    if full_screen:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    else:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    background_image_main = pygame.image.load("../drawable/backgrounds/main_menu4.jpg")
    background_image_main = pygame.transform.scale(background_image_main, (WINDOW_WIDTH, WINDOW_HEIGHT))

    window_surface.blit(background_image_main, [0, 0])

    pygame.display.set_caption('Meow Hero')

    return window_surface


def draw_text(text, surface, x, y):
    font = pygame.font.SysFont(None, 60)
    text_object = font.render(text, 1, COLOR_WHITE)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)


# TODO: отрисовать нормально :D
# TODO: кнопка "назад"
# TODO: lock levels
def levels_menu(window_surface):
    background_image_levels = pygame.transform.scale(pygame.image.load("../drawable/backgrounds/main_menu4.jpg"),
                                                     (WINDOW_WIDTH, WINDOW_HEIGHT))

    window_surface.blit(background_image_levels, [0, 0])

    image = pygame.image.load('../drawable/buttons/red_button.png')
    image = pygame.transform.scale(image, (int(WINDOW_WIDTH / 20), int(WINDOW_HEIGHT / 20)))

    buttons = list()

    for i in range(12):
        button = objects.Button(image, i*WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i))
        buttons.append(button)

    for button in buttons:
        button.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                for button in buttons:
                    if button.is_over(mouse_pos):
                        # TODO: draw story here
                        # TODO: send level as param
                        game_loop(window_surface)
                        # TODO: draw story here, if victory
                        # TODO: unlock new level


# TODO: кнопка статистики
# TODO: смена имени игрока
# TODO: смена скина
def main_menu(window_surface):     # show the "Main menu" screen
    image = pygame.image.load('../drawable/buttons/red_button.png')
    image = pygame.transform.scale(image, (int(WINDOW_WIDTH/3), int(WINDOW_HEIGHT/8)))

    button_single = objects.Button(image, WINDOW_WIDTH/2, WINDOW_HEIGHT/4,
                                   WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "1 Player")
    button_two = objects.Button(image, WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                                WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "2 Players")
    button_quit = objects.Button(image, WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4,
                                 WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "Quit")

    button_single.draw(window_surface)
    button_two.draw(window_surface)
    button_quit.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if button_single.is_over(mouse_pos):
                    levels_menu(window_surface)
                elif button_two.is_over(mouse_pos):
                    pass
                    # TODO: press F
                    # client.open_tcp_protocol("localhost", 9027, window_surface)
                    # init_window()
                    #
                    # button_single.draw(window_surface)
                    # button_two.draw(window_surface)
                    # button_quit.draw(window_surface)
                    #
                    # pygame.display.update()
                    # break
                elif button_quit.is_over(mouse_pos):
                    sys.exit(0)


def main():
    window = init_window(True)
    main_menu(window)


if __name__ == "__main__":
    main()
