import json
import random
import sys
from time import sleep

import pygame
from pygame.locals import *

from . import interface, objects, layouts
from .game_config import ENEMY_CONFIG
from modules.display_config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLACK, COLOR_WHITE, CAT_IMG_RESIZE

"""
Всё отвечающее за игру
"""

FPS = 40
ENEMY_MAX_COUNT = 40

SKIN_LEVELS = [1, 6, 8, 9, 10, 12]


def save_player_state(player):
    print("Levels:", player.levels)
    handler = open("../stats/last_player.txt", 'w')
    handler.write(player.name)
    handler.close()
    player.save_current_state()


def save_and_exit(player):
    save_player_state(player)
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key(player):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                save_and_exit(player)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    return
                return


def story_loop(window_surface, level_number, prefix, player):
    pygame.mouse.set_visible(False)

    try:
        handler = open("../plot/eng/" + prefix + "_story_" + str(level_number) + ".txt", 'r', errors='ignore')
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
    text_view = interface.TextView(font, COLOR_WHITE, WINDOW_WIDTH / 6 + 50, WINDOW_HEIGHT / 10)

    window_surface.fill(COLOR_BLACK)

    image = pygame.image.load('../drawable/sprites/cat_hero/skins/cat' + str(player.current_skin) + '.png')

    image_surface = pygame.transform.scale(image, CAT_IMG_RESIZE)
    rect = image_surface.get_rect()

    rect.move_ip(0, 150)
    window_surface.blit(image_surface, rect)

    pygame.display.update()

    # try to skip buffered events
    for event in pygame.event.get():
        continue

    buf = ""
    skip = False
    for line in text:
        line = line.replace("(username)", player.name)
        for elem in line:
            if skip:
                text_view.draw_this(window_surface, line)
                pygame.display.update()
                break
            buf += elem
            text_view.draw_this(window_surface, buf)
            pygame.display.update()
            sleep(0.05)
            # skip if escape
            for event in pygame.event.get():
                if event.type == KEYUP:
                    skip = True
        buf = ""
        text_view.next_line(60)

    pygame.mixer.music.stop()
    wait_for_player_to_press_key(player)
    pygame.mouse.set_visible(True)


def enemy_switch_by_level(level_number):
    try:
        _, name, enemy_class = ENEMY_CONFIG[level_number]
        return enemy_class(name, level_number)
    except KeyError as e:
        return None


def game_loop(window_surface, level_number, player):
    print(player.name)
    print(level_number)
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
    attack_sound = pygame.mixer.Sound('../sound/short_tracks/attack_1' + ".wav")

    try:
        pygame.mixer.music.load('../sound/background_music/music' + str(level_number) + ".mp3")
    except Exception:
        pygame.mixer.music.load("../sound/main_theme.mp3")

    # set up text
    font = pygame.font.SysFont(None, 60)
    score_text = interface.TextView(font, COLOR_WHITE, 10, 0)
    top_score_text = interface.TextView(font, COLOR_WHITE, 10, 40)
    timer_text = interface.TextView(font, COLOR_WHITE, 10 * WINDOW_WIDTH / 12, 10)

    meow_hero = objects.MeowHero(player.current_skin)
    meow_hero.rect.move_ip(int(WINDOW_WIDTH / 2), 7 * int(WINDOW_HEIGHT / 8))

    health_points = objects.Health(1, WINDOW_WIDTH / 30, WINDOW_HEIGHT / 30)

    bullets = []
    enemies = []
    bonuses = []
    enemy_bullets = []

    # setting score
    score = 0
    handler = open("../stats/high_score.json", 'r')
    data = json.load(handler)
    top_score = data[str(level_number)][1]
    handler.close()

    # setting spawn probability and level time
    try:
        spawn_proba, _, _ = ENEMY_CONFIG[int(level_number)]
    except KeyError as e:
        spawn_proba = 0
    # main_timer = 50
    main_timer = 10 * level_number + 60

    move_left = move_right = move_up = move_down = False
    pygame.mixer.music.play(-1, 0.0)

    running = True
    victory = True
    while running:  # the game loop runs while the game part is playing
        score += 1  # increase score
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                save_and_exit(player)

            if event.type == pygame.USEREVENT:
                main_timer -= 1
                # victory condition
                if main_timer <= 0:
                    running = False

                # decrement invulnerability
                if meow_hero.invulnerability > 0:
                    meow_hero.invulnerability -= 1

                # spawn enemy
                dice = random.random()
                if dice < spawn_proba:
                    enemy = enemy_switch_by_level(level_number)
                    enemies.append(enemy)

                # attack time
                for enemy in enemies:
                    enemy_bullet = enemy.attack(meow_hero.rect.center)
                    if enemy_bullet is not None:
                        enemy_bullets.append(enemy_bullet)

                # bonus lifetime
                for bonus in bonuses:
                    bonus.take_damage()
                    if not bonus.is_alive():
                        bonuses.remove(bonus)

                # spawn bonuses by time
                if main_timer % 10 == 0:
                    bonus = objects.Bonus("Coin", level_number)
                    bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(200, WINDOW_HEIGHT))
                    bonuses.append(bonus)

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullet = objects.Bullet(level_number)
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
                        pygame.mixer.music.stop()
                        pygame.mouse.set_visible(True)
                        return False
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

        # hitting enemy
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.take_damage(bullet.power)
                    bullet.take_damage()
                    attack_sound.play()

        # hitting hero:
        for enemy in enemies:
            if meow_hero.rect.colliderect(enemy.rect) and not meow_hero.invulnerability:
                meow_hero.take_damage()
                meow_hero.invulnerability += 1
                enemies.remove(enemy)
                damage_sound.play()

        # hitting hero by bullets
        for bullet in enemy_bullets:
            if meow_hero.rect.colliderect(bullet.rect) and not meow_hero.invulnerability:
                meow_hero.take_damage()
                enemy_bullets.remove(bullet)
                meow_hero.invulnerability += 1
                damage_sound.play()

        # collecting bonuses:
        for bonus in bonuses:
            if meow_hero.rect.colliderect(bonus.rect):
                if bonus.name == "Coin":
                    score += 1000
                    coin_sound.play()
                bonuses.remove(bonus)

        # check if bullet is out of screen
        for bullet in bullets:
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw health points
        health_points.draw(window_surface, meow_hero.life)

        # draw text
        score_text.draw_this(window_surface, 'Score: %s' % (score), )
        top_score_text.draw_this(window_surface, 'Top Score: %s' % (top_score))
        timer_text.draw_this(window_surface, "Time " + str(main_timer).rjust(3) if main_timer > 0 else 'GG')

        # draw hero
        meow_hero.draw(window_surface)

        # draw bonuses
        for bonus in bonuses:
            bonus.draw(window_surface)

        # draw enemies
        for enemy in enemies:
            enemy.move()
            if enemy.rect.top > WINDOW_HEIGHT or enemy.rect.right < 0 or enemy.rect.left > WINDOW_WIDTH or not enemy.is_alive():
                enemies.remove(enemy)
                score += 100 * enemy.level
            enemy.draw(window_surface)

        # move and draw hero bullets
        for bullet in bullets:
            bullet.move()
            if bullet.rect.top > WINDOW_HEIGHT or not bullet.is_alive():
                bullets.remove(bullet)
            bullet.draw(window_surface)

        # move and draw enemy bullets
        for bullet in enemy_bullets:
            bullet.move()
            if bullet.rect.top > WINDOW_HEIGHT or not bullet.is_alive():
                enemy_bullets.remove(bullet)
            bullet.draw(window_surface)

        # check for ending:
        if not meow_hero.is_alive():
            running = False
            victory = False

        pygame.display.update()
        main_clock.tick(FPS)

    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

    if victory:
        score = score + meow_hero.life * 1000
        # checking for new record
        victory_sound.play()

        new_skin = False
        if level_number in SKIN_LEVELS and level_number not in player.skins:
            new_skin = True
            player.skins.append(level_number)

        if score > top_score:
            handler = open("../stats/high_score.json", 'r')
            data = json.load(handler)
            handler.close()
            data[str(level_number)] = [player.name, score]
            handler = open("../stats/high_score.json", 'w')
            json.dump(data, handler)
            handler.close()
            layouts.victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, False, score, True, new_skin)
        else:
            layouts.victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, False, score, False, new_skin)
        victory_sound.stop()
        if level_number + 1 not in player.levels:
            player.levels.append(int(level_number + 1))
    else:
        game_over_sound.play()
        layouts.defeat_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_over_sound.stop()

    pygame.display.update()

    return victory


def boss_game_loop(window_surface, level_number, player):
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
    timer_text = interface.TextView(font, COLOR_WHITE, 10 * WINDOW_WIDTH / 12, 10)

    meow_hero = objects.MeowHero(player.current_skin)
    meow_hero.rect.move_ip(int(WINDOW_WIDTH / 2), 7 * int(WINDOW_HEIGHT / 8))

    health_points = objects.Health(1, WINDOW_WIDTH / 30, WINDOW_HEIGHT / 30)

    bullets = []
    enemies = []
    bonuses = []
    enemy_bullets = []

    main_timer = 0

    # set up bosses
    if level_number == 1:
        enemy = objects.ZloyMuzhic("Zloy muzhic", level_number)
        enemies.append(enemy)
    elif level_number == 4:
        enemy = objects.EGE("EGE", level_number)
        enemies.append(enemy)
    elif level_number == 5:
        enemy = objects.Committee("Committee", level_number)
        enemies.append(enemy)
    elif level_number == 6:
        for i in range(4):
            enemy = objects.Teacher(str(i + 1), level_number)
            enemy.rect.move_ip(i * 300, 0)
            enemies.append(enemy)
    elif level_number == 7:
        enemy = objects.Ejudje("Ejudje", level_number)
        enemies.append(enemy)
    elif level_number == 9:
        enemy = objects.DedMoroz("Ded Moroz", level_number)
        enemy.rect.move_ip(WINDOW_WIDTH / 2, 0)
        enemies.append(enemy)
    elif level_number == 10:
        enemy = objects.DiplomCommittee("Diplom Committee", level_number)
        enemy.rect.move_ip(WINDOW_WIDTH / 2, 0)
        enemies.append(enemy)
    elif level_number == 12:
        enemy = objects.OlegAlexeevich("Oleg Alexeevich", level_number)
        enemies.append(enemy)

    # define healthbar
    health_bar = None
    if len(enemies) == 1:
        boss_life = enemies[0].life
        health_bar = interface.TextView(font, COLOR_WHITE, 0, 0)

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
                save_and_exit(player)

            if event.type == pygame.USEREVENT:
                main_timer += 1
                # victory condition
                if len(enemies) == 0:
                    running = False
                    victory = True
                    break

                # decrement invulnerability
                if meow_hero.invulnerability > 0:
                    meow_hero.invulnerability -= 1

                # attack time
                for enemy in enemies:
                    enemy_bullet = enemy.attack(meow_hero.rect.center)
                    if enemy_bullet is not None:
                        enemy_bullets.append(enemy_bullet)

                # bonus lifetime
                for bonus in bonuses:
                    bonus.take_damage()
                    if not bonus.is_alive():
                        bonuses.remove(bonus)

                # spawn bonuses by time
                if main_timer % 10 == 0:
                    bonus = objects.Bonus("Coin", level_number)
                    bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(200, WINDOW_HEIGHT))
                    bonuses.append(bonus)

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullet = objects.Bullet(level_number)
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
                        pygame.mixer.music.stop()
                        pygame.mouse.set_visible(True)
                        return False
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

        # hitting enemy
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.take_damage(bullet.power)
                    bullet.take_damage()
                    attack_sound.play()

        # hitting hero:
        for enemy in enemies:
            if meow_hero.rect.colliderect(enemy.rect) and not meow_hero.invulnerability:
                meow_hero.take_damage()
                meow_hero.invulnerability += 1
                damage_sound.play()

        # hitting hero by bullets
        for bullet in enemy_bullets:
            if meow_hero.rect.colliderect(bullet.rect) and not meow_hero.invulnerability:
                meow_hero.take_damage()
                enemy_bullets.remove(bullet)
                meow_hero.invulnerability += 1
                damage_sound.play()

        # collecting bonuses:
        for bonus in bonuses:
            if meow_hero.rect.colliderect(bonus.rect):
                if bonus.name == "Coin":
                    score += 1000
                    coin_sound.play()
                bonuses.remove(bonus)

        # check if bullet is out of screen
        for bullet in bullets:
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw health points
        health_points.draw(window_surface, meow_hero.life)

        # draw text
        score_text.draw_this(window_surface, 'Score: %s' % (score), )
        top_score_text.draw_this(window_surface, 'Top Score: %s' % (top_score))
        timer_text.draw_this(window_surface, "Time " + str(main_timer).rjust(3) if main_timer > 0 else 'GG')

        # draw hero
        meow_hero.draw(window_surface)

        # draw bonuses
        for bonus in bonuses:
            bonus.draw(window_surface)

        # draw enemies
        for enemy in enemies:
            enemy.move()
            if enemy.rect.top > WINDOW_HEIGHT or not enemy.is_alive():
                enemies.remove(enemy)
                score += 100 * enemy.level
            enemy.draw(window_surface)

        # draw healthbar
        if health_bar is not None:
            if len(enemies):
                health_bar.rect.topleft = enemies[0].rect.center
                health_bar.rect.move_ip(20, 80)
                health_bar.draw_this(window_surface, str(enemies[0].life) + '/' + str(boss_life))

        # move and draw hero bullets
        for bullet in bullets:
            bullet.move()
            if bullet.rect.top > WINDOW_HEIGHT or not bullet.is_alive():
                bullets.remove(bullet)
            bullet.draw(window_surface)

        # move and draw enemy bullets
        for bullet in enemy_bullets:
            bullet.move()
            if bullet.rect.top > WINDOW_HEIGHT or not bullet.is_alive():
                enemy_bullets.remove(bullet)
            bullet.draw(window_surface)

        # check for ending:
        if not meow_hero.is_alive():
            running = False
            victory = False

        pygame.display.update()
        main_clock.tick(FPS)

    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

    if victory:
        # checking for new record
        score = int((score + meow_hero.life * 1000) * 100 / main_timer)
        victory_sound.play()

        new_skin = False
        if level_number in SKIN_LEVELS and level_number not in player.skins:
            new_skin = True
            player.skins.append(level_number)

        if score > top_score:
            handler = open("../stats/high_score.json", 'r')
            data = json.load(handler)
            handler.close()
            data[str(level_number)] = [player.name, score]
            handler = open("../stats/high_score.json", 'w')
            json.dump(data, handler)
            handler.close()
            layouts.victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, True, score, True, new_skin)
        else:
            layouts.victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, True, score, False, new_skin)
        victory_sound.stop()
        if level_number + 1 not in player.levels:
            player.levels.append(int(level_number + 1))
    else:
        game_over_sound.play()
        layouts.defeat_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_over_sound.stop()

    pygame.display.update()

    return victory
