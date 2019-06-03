import random
import re
import pygame
import screeninfo
import sys

from modules import interface, client, objects
from time import sleep
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
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

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


def story_loop(window_surface, level_number, prefix):
    pygame.mouse.set_visible(False)

    try:
        handler = open("../plot/" + prefix + "_story_" + str(level_number) + ".txt")
    except FileNotFoundError:
        print("No plot for level")
        return

    text = handler.read()
    handler.close()

    font = pygame.font.SysFont(None, 60)
    text_view = interface.TextView(font, COLOR_WHITE, WINDOW_WIDTH/5, 2*WINDOW_HEIGHT/5)

    window_surface.fill(COLOR_BLACK)

    meow_hero = objects.MeowHero(1, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 5)
    meow_hero.rect.move_ip(4*int(WINDOW_WIDTH/5), 6*int(WINDOW_HEIGHT/8))
    meow_hero.draw(window_surface)

    pygame.display.update()

    # ебааать импровизированная анимация
    # TODO: add interruption
    buf = ""
    for elem in text:
        buf += elem
        text_view.draw(window_surface, buf)
        pygame.display.update()
        sleep(0.1)
        # skip if escape
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return
    # TODO: add pause after this
    wait_for_player_to_press_key()

    pygame.mouse.set_visible(True)


def game_loop(window_surface, level_number):
    pygame.mouse.set_visible(False)

    main_clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')

    # TODO; exception on 10, 11 and 12 levels
    pygame.mixer.music.load('../sound/background_music/music_' + str(level_number) + ".mp3")

    # set up text
    font = pygame.font.SysFont(None, 60)
    score_text = interface.TextView(font, COLOR_WHITE, 10, 0)
    top_score_text = interface.TextView(font, COLOR_WHITE, 10, 40)
    timer_text = interface.TextView(font, COLOR_WHITE, 10*WINDOW_WIDTH/12, 10)

    meow_hero = objects.MeowHero(1, WINDOW_WIDTH/12, WINDOW_HEIGHT/12)
    meow_hero.rect.move_ip(int(WINDOW_WIDTH/2), 7*int(WINDOW_HEIGHT/8))

    health_points = objects.Health(1, WINDOW_WIDTH/30, WINDOW_HEIGHT/30)

    bullets = []
    enemies = []
    bonuses = []

    main_timer = 10*level_number + 40
    top_score = 0
    score = 0

    move_left = move_right = move_up = move_down = False
    pygame.mixer.music.play(-1, 0.0)

    running = True
    victory = True
    while running:  # the game loop runs while the game part is playing
        score += 1  # increase score

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                # TODO: open quit menu
                terminate()

            if event.type == pygame.USEREVENT:
                main_timer -= 1
                # victory condition
                if main_timer <= 0:
                    running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # TODO: add sound
                    bullet = objects.Bullet(1, WINDOW_WIDTH/30, WINDOW_HEIGHT/30)
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

        # spawn bonuses by time
        if main_timer % 10 == 0 and len(bonuses) == 0:
            bonus = objects.Bonus("Life", WINDOW_WIDTH/24, WINDOW_HEIGHT/24)
            bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            bonuses.append(bonus)
            bonus = objects.Bonus("Coin", WINDOW_WIDTH / 24, WINDOW_HEIGHT / 24)
            bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            bonuses.append(bonus)

        # spawn enemy
        if len(enemies) < ENEMY_MAX_COUNT:
            dice = random.random()
            if dice < 0.1:
                # TODO: spawn randomly by level_number
                enemy = objects.DogEnemy(1, WINDOW_WIDTH/18, WINDOW_HEIGHT/18)
                enemy.rect.move_ip(random.randint(0, WINDOW_WIDTH), 0)
                enemies.append(enemy)

        # hitting enemy
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

        # collecting bonuses:
        for bonus in bonuses:
            if meow_hero.rect.colliderect(bonus.rect):
                if bonus.bonus_type == "Life":
                    meow_hero.life += 1
                elif bonus.bonus_type == "Coin":
                    score += 1000
                bonuses.remove(bonus)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw health points
        health_points.draw(window_surface, meow_hero.life)

        # draw text
        score_text.draw(window_surface, 'Score: %s' % (score), )
        top_score_text.draw(window_surface, 'Top Score: %s' % (top_score))
        timer_text.draw(window_surface, "Time "+ str(main_timer).rjust(3) if main_timer > 0 else 'NICE, NIGGA')

        # draw hero
        meow_hero.draw(window_surface)

        # draw bonuses
        for bonus in bonuses:
            bonus.draw(window_surface)

        # draw enemies
        for enemy in enemies:
            enemy.move()
            if enemy.rect.top > WINDOW_HEIGHT or enemy.life <= 0:
                enemies.remove(enemy)
                score += 100 * enemy.level
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
            victory = False

        pygame.display.update()

        main_clock.tick(FPS)

    if victory:
        # TODO: do something
        pass
    else:
        pygame.mixer.music.stop()
        game_over_sound.play()

    # TODO: check if game is over
    pygame.display.update()
    wait_for_player_to_press_key()

    game_over_sound.stop()
    pygame.mouse.set_visible(True)


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
        button = interface.Button(image, i*WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i+1))
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
                        story_loop(window_surface, int(button.text), "pre")
                        game_loop(window_surface, int(button.text))
                        story_loop(window_surface, int(button.text), "post")
                        return


# TODO: кнопка статистики
# TODO: смена имени игрока
# TODO: смена скина
def main_menu(window_surface):     # show the "Main menu" screen
    image = pygame.image.load('../drawable/buttons/red_button.png')
    image = pygame.transform.scale(image, (int(WINDOW_WIDTH/3), int(WINDOW_HEIGHT/8)))

    button_single = interface.Button(image, WINDOW_WIDTH/2, WINDOW_HEIGHT/4,
                                   WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "1 Player")
    button_two = interface.Button(image, WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                                WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "2 Players")
    button_quit = interface.Button(image, WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4,
                                 WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "Quit")

    button_single.draw(window_surface)
    button_two.draw(window_surface)
    button_quit.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if button_single.is_over(mouse_pos):
                    levels_menu(window_surface)
                    return
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
    while True:
        window = init_window(True)
        main_menu(window)


if __name__ == "__main__":
    main()
