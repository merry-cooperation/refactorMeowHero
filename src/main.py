import random
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
FPS = 60
ENEMY_MAX_COUNT = 40


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


def game_loop(window_surface):
    main_clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')
    pygame.mixer.music.load('../sound/main_theme.mp3')

    # set up images
    player_image = pygame.image.load('../drawable/sprites/cat_hero/cat_hero.png')
    enemy_image = pygame.image.load('../drawable/sprites/enemy/dog_enemy.png')
    health_image = pygame.image.load('../drawable/other/health.png')
    bullet_image = pygame.image.load('../drawable/weapons/bullet1.png')

    # set up text
    font = pygame.font.SysFont(None, 60)
    score_text = objects.TextView(font, COLOR_WHITE, 10, 0)
    top_score_text = objects.TextView(font, COLOR_WHITE, 10, 40)
    timer_text = objects.TextView(font, COLOR_WHITE, 10*WINDOW_WIDTH/12, 10)

    meow_hero = heroes.MeowHero(player_image, WINDOW_WIDTH/12, WINDOW_HEIGHT/12)
    meow_hero.rect.move_ip(int(WINDOW_WIDTH/2), 7*int(WINDOW_HEIGHT/8))

    health_points = heroes.Health(health_image, WINDOW_WIDTH/30, WINDOW_HEIGHT/30)

    bullets = []
    enemies = []

    wait_for_player_to_press_key()

    main_timer = 100
    top_score = 0
    while True:
        score = 0

        move_left = move_right = move_up = move_down = False
        pygame.mixer.music.play(-1, 0.0)

        running = True
        while running:  # the game loop runs while the game part is playing
            score += 1  # increase score

            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    # TODO: open quit menu
                    terminate()

                if event.type == pygame.USEREVENT:
                    main_timer -= 1

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        # TODO: add sound
                        bullet = heroes.Bullet(bullet_image, WINDOW_WIDTH/30, WINDOW_HEIGHT/30)
                        bullet.rect.move_ip(meow_hero.rect.left, meow_hero.rect.top)
                        bullets.append(bullet)
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

            # move the player around
            if move_left and meow_hero.rect.left > 0:
                meow_hero.move(-1, 0)
            if move_right and meow_hero.rect.right < WINDOW_WIDTH:
                meow_hero.move(1, 0)
            if move_up and meow_hero.rect.top > 0:
                meow_hero.move(0, -1)
            if move_down and meow_hero.rect.bottom < WINDOW_HEIGHT:
                meow_hero.move(0, 1)

            # spawn dogs
            if len(enemies) < ENEMY_MAX_COUNT:
                dice = random.random()
                if dice < 0.1:
                    enemy = heroes.DogEnemy(enemy_image, WINDOW_WIDTH/24, WINDOW_HEIGHT/24)
                    enemy.rect.move_ip(random.randint(0, WINDOW_WIDTH), 0)
                    enemies.append(enemy)

            # hitting dogs
            for enemy in enemies:
                for bullet in bullets:
                    if enemy.rect.colliderect(bullet.rect):
                        enemy.life -= 1
                        bullet.life -= 1

            # hitting hero:
            for enemy in enemies:
                if meow_hero.rect.colliderect(enemy.rect):
                    meow_hero.life -= 1
                    enemies.remove(enemy)

            # draw background
            window_surface.blit(background_image_in_game, [0, 0])

            # draw health points
            health_points.draw(window_surface, meow_hero.life)

            # draw text
            score_text.draw(window_surface, 'Score: %s' % (score), )
            top_score_text.draw(window_surface, 'Top Score: %s' % (top_score))
            timer_text.draw(window_surface, "Time "+ str(main_timer).rjust(3) if main_timer > 0 else 'boom!')

            # draw hero
            meow_hero.draw(window_surface)

            # draw enemies
            for enemy in enemies:
                enemy.move()
                if enemy.rect.top > WINDOW_HEIGHT or enemy.life <= 0:
                    enemies.remove(enemy)
                enemy.draw(window_surface)

            # move and draw hero bullets
            for bullet in bullets:
                bullet.move()
                if bullet.rect.top > WINDOW_HEIGHT or bullet.life <= 0:
                    bullets.remove(bullet)
                bullet.draw(window_surface)

            # check for ending:
            if meow_hero.life <= 0:
                running = False

            pygame.display.update()

            main_clock.tick(FPS)

        # TODO: return player to main menu
        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()
        game_over_sound.play()

        # TODO: check if game is over
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
