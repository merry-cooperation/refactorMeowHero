import json
import random
import re
import sys
from time import sleep

import pygame
import screeninfo
from modules import interface, objects, layouts, client
from pygame.locals import *

# taking screen W and H
for m in screeninfo.get_monitors():
    print(str(m))
    pattern = "\d*x\d*"
    WINDOW_WIDTH, WINDOW_HEIGHT = list(map(int, re.findall(pattern, str(m))[0].split('x')))

# constants, if need hardcoded
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

# constant BG
background_image_main = pygame.image.load("../drawable/backgrounds/main_menu4.jpg")
background_image_main = pygame.transform.scale(background_image_main, (WINDOW_WIDTH, WINDOW_HEIGHT))
background_image_levels = pygame.image.load("../drawable/backgrounds/main_menu4.jpg")
background_image_levels = pygame.transform.scale(background_image_levels, (WINDOW_WIDTH, WINDOW_HEIGHT))

# colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BRIGHT_GREY = (200, 200, 200)
COLOR_RED = (255, 0, 0)

# magic
FPS = 60
ENEMY_MAX_COUNT = 40


def terminate(player):
    # saving current state
    print("Levels:", player.levels)
    handler = open("../stats/last_player.txt", 'w')
    handler.write(player.name)
    handler.close()
    player.save_current_state()

    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key(player):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(player)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate(player)
                return


def story_loop(window_surface, level_number, prefix, player):
    pygame.mouse.set_visible(False)

    try:
        handler = open("../plot/" + prefix + "_story_" + str(level_number) + ".txt")
    except FileNotFoundError:
        print("No plot for level")
        pygame.mouse.set_visible(True)
        return

    pygame.mixer.music.load('../sound/short_tracks/typewriter.mp3')
    pygame.mixer.music.play(-1)

    text = handler.read()
    text = text.split('\n')
    handler.close()

    font = pygame.font.SysFont(None, 60)
    text_view = interface.TextView(font, COLOR_WHITE, WINDOW_WIDTH/5, 2*WINDOW_HEIGHT/5)

    window_surface.fill(COLOR_BLACK)

    meow_hero = objects.MeowHero(1, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 5)
    meow_hero.rect.move_ip(4*int(WINDOW_WIDTH/5), 6*int(WINDOW_HEIGHT/8))
    meow_hero.draw(window_surface)

    pygame.display.update()

    # try to skip buffered events
    for event in pygame.event.get():
        continue

    buf = ""
    skip = False
    for line in text:
        for elem in line:
            if skip:
                text_view.draw_this(window_surface, line)
                pygame.display.update()
                break
            buf += elem
            text_view.draw_this(window_surface, buf)
            pygame.display.update()
            sleep(0.1)
            # skip if escape
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        return
                    else:
                        skip = True
        buf = ""
        text_view.next_line(60)

    pygame.mixer.music.stop()
    wait_for_player_to_press_key(player)
    pygame.mouse.set_visible(True)


def game_loop(window_surface, level_number, player):
    print(player.name)
    pygame.mouse.set_visible(False)

    main_clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 500)

    # set up background
    try:
        background_image_in_game = pygame.image.load("../drawable/backgrounds/background" + str(level_number) + ".jpg")
    except Exception:
        background_image_in_game = pygame.image.load("../drawable/backgrounds/abstract_background.jpg")
    background_image_in_game = pygame.transform.scale(background_image_in_game, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # set up music
    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')
    damage_sound = pygame.mixer.Sound('../sound/short_tracks/damage.wav')
    victory_sound = pygame.mixer.Sound('../sound/short_tracks/victory.wav')
    coin_sound = pygame.mixer.Sound('../sound/short_tracks/coin.wav')
    health_sound = pygame.mixer.Sound('../sound/short_tracks/health.wav')
    new_top_sound = pygame.mixer.Sound('../sound/short_tracks/health.wav')
    attack_sound = pygame.mixer.Sound('../sound/short_tracks/attack_1' + ".wav")

    try:
        pygame.mixer.music.load('../sound/background_music/music' + str(level_number) + ".mp3")
    except Exception:
        pygame.mixer.music.load("../sound/main_theme.mp3")

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
    enemy_bullets = []

    main_timer = 50  # debugging
    # main_timer = 10*level_number + 40

    # set up bosses
    if level_number == 1:
        enemy = objects.ZloyMuzhic("Zloy muzhic", level_number, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 6)
        enemies.append(enemy)

    # setting score
    score = 0
    handler = open("../stats/high_score.json", 'r')
    data = json.load(handler)
    top_score = data[str(level_number)][1]
    handler.close()

    move_left = move_right = move_up = move_down = False
    pygame.mixer.music.play(-1, 0.0)

    running = True
    victory = True
    while running:  # the game loop runs while the game part is playing
        score += 1  # increase score

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(player)

            # TODO: spawn enemy
            if event.type == pygame.USEREVENT:
                main_timer -= 1
                # victory condition
                if main_timer <= 0:
                    running = False

                # attack time
                for enemy in enemies:
                    enemy_bullet = enemy.attack(meow_hero.rect.center)
                    if enemy_bullet is not None:
                        enemy_bullets.append(enemy_bullet)

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
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
                    quit_state = layouts.interruption_menu(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
                    if quit_state:
                        print("Goodbye")
                        terminate(player)
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

        # hitting enemy
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.life -= bullet.power
                    bullet.life -= 1
                    attack_sound.play()

        # hitting hero:
        for enemy in enemies:
            if meow_hero.rect.colliderect(enemy.rect):
                meow_hero.life -= 1
                enemies.remove(enemy)
                damage_sound.play()

        # hitting hero by bullets
        for bullet in enemy_bullets:
            if meow_hero.rect.colliderect(bullet.rect):
                meow_hero.life -= 1
                enemy_bullets.remove(bullet)
                damage_sound.play()

        # collecting bonuses:
        for bonus in bonuses:
            if meow_hero.rect.colliderect(bonus.rect):
                if bonus.bonus_type == "Life":
                    meow_hero.life += 1
                    health_sound.play()
                elif bonus.bonus_type == "Coin":
                    score += 1000
                    coin_sound.play()
                bonuses.remove(bonus)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw health points
        health_points.draw(window_surface, meow_hero.life)

        # draw text
        score_text.draw_this(window_surface, 'Score: %s' % (score), )
        top_score_text.draw_this(window_surface, 'Top Score: %s' % (top_score))
        timer_text.draw_this(window_surface, "Time " + str(main_timer).rjust(3) if main_timer > 0 else 'NICE, NIGGA')

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

        # move and draw enemy bullets
        for bullet in enemy_bullets:
            bullet.move()
            if bullet.rect.top > WINDOW_HEIGHT or bullet.life <= 0:
                enemy_bullets.remove(bullet)
            bullet.draw(window_surface)

        # check for ending:
        if meow_hero.life <= 0:
            running = False
            victory = False

        pygame.display.update()
        main_clock.tick(FPS)

    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

    if victory:
        # checking for new record
        victory_sound.play()
        layouts.victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
        victory_sound.stop()
        if level_number+1 not in player.levels:
            player.levels.append(int(level_number+1))
        if score > top_score:
            new_top_sound.play()
            handler = open("../stats/high_score.json", 'r')
            data = json.load(handler)
            handler.close()
            data[str(level_number)] = [player.name, score]
            handler = open("../stats/high_score.json", 'w')
            json.dump(data, handler)
            handler.close()
    else:
        game_over_sound.play()
        layouts.defeat_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_over_sound.stop()

    pygame.display.update()
    wait_for_player_to_press_key(player)

    return True if victory else False


def init_window(full_screen=False):  # set up pygame, the window, and the mouse cursor
    pygame.init()

    if full_screen:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    else:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    window_surface.blit(background_image_main, [0, 0])
    pygame.display.set_caption('Meow Hero')

    return window_surface


# TODO: отрисовать нормально :D
def levels_menu(window_surface, player):
    buttons = list()

    for i in range(12):
        if i+1 in player.levels:
            button = interface.Button(i*WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                      WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i+1))
        else:
            button = interface.Button(i * WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                      WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i + 1), True)

        buttons.append(button)

    button_back = interface.Button(20, 20, WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10, "Back")
    buttons.append(button_back)

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()  # gets mouse position
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate(player)

            for button in buttons:
                if button.is_over(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN and not button.is_off:
                        if button.text == "Back":
                            return
                        story_loop(window_surface, int(button.text), "pre", player)
                        victory = game_loop(window_surface, int(button.text), player)
                        if victory:
                            story_loop(window_surface, int(button.text), "post", player)
                            # TODO: do it in function
                            # TEST
                            buttons = list()
                            for i in range(12):
                                if i + 1 in player.levels:
                                    button = interface.Button(i * WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                                              WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i + 1))
                                else:
                                    button = interface.Button(i * WINDOW_WIDTH / 12, WINDOW_HEIGHT / 4,
                                                              WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, str(i + 1), True)

                                buttons.append(button)
                            button_back = interface.Button(20, 20, WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10, "Back")
                            buttons.append(button_back)
                            # TEST

            window_surface.blit(background_image_levels, [0, 0])

            for button in buttons:
                button.draw(window_surface)

            pygame.display.update()


# TODO: смена скина
def main_menu(window_surface):     # show the "Main menu" screen
    # preparing text
    font_0 = pygame.font.SysFont("rachana", 140)
    font_1 = pygame.font.SysFont(None, 78)
    font_2 = pygame.font.SysFont(None, 42)

    # loading last player
    handler = open("../stats/last_player.txt", 'r')
    player_name = handler.read().strip()
    handler.close()

    # loading player info
    try:
        player = interface.load_player_by_path("../stats/players/" + player_name + ".json")
    except FileNotFoundError:
        player = interface.load_player_by_path("../stats/players/" + "Test Player" + ".json")

    # creating text and buttons
    greeting_text = interface.TextView(font_1, COLOR_BLACK, 15, 15, "Hello, " + player_name + "!")
    game_title_text = interface.TextView(font_0, COLOR_BLACK, WINDOW_WIDTH/2, 50, "MEOW HERO")
    not_you_text_button = interface.TextView(font_2, COLOR_RED, WINDOW_WIDTH/5, 90, "Not you, dude?")

    button_single = interface.Button(WINDOW_WIDTH/2+100, WINDOW_HEIGHT/4,
                                   WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "1 Player")
    button_two = interface.Button(WINDOW_WIDTH/2+100, WINDOW_HEIGHT/2,
                                WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "2 Players")
    button_quit = interface.Button(WINDOW_WIDTH/2+100, 3*WINDOW_HEIGHT/4,
                                 WINDOW_WIDTH/3, WINDOW_HEIGHT/8, "Quit")

    # TODO: change text to images, if possible
    button_stats = interface.Button(50, 140, WINDOW_WIDTH/8, WINDOW_HEIGHT/7, "Stats")
    button_skins = interface.Button(260, 140, WINDOW_WIDTH/8, WINDOW_HEIGHT/7, "Skins")
    button_future = interface.Button(470, 140, WINDOW_WIDTH/8, WINDOW_HEIGHT/7, "KEK")

    drawable = list()
    drawable.append(greeting_text)
    drawable.append(game_title_text)
    drawable.append(not_you_text_button)
    drawable.append(button_quit)
    drawable.append(button_two)
    drawable.append(button_single)
    drawable.append(button_stats)
    drawable.append(button_skins)
    drawable.append(button_future)

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                print("Goodbye")
                terminate(player)

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate(player)

            if button_single.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    levels_menu(window_surface, player)
            elif button_two.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    client.two_players_mode(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
            elif button_quit.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    terminate(player)
            elif not_you_text_button.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player = layouts.create_profile_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT)
                    greeting_text.text = "Hello, " + player.name + "!"
            elif button_stats.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    layouts.stats_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
            elif button_skins.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    layouts.change_skin_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
            elif button_future.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # I don't know why I need this button
                    layouts.future_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)

        # drawing objects
        window_surface.blit(background_image_main, [0, 0])
        for elem in drawable:
            elem.draw(window_surface)

        pygame.display.update()


def main():
    while True:
        window = init_window(False)  # True if fullscreen
        main_menu(window)


if __name__ == "__main__":
    main()
