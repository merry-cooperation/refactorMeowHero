import logging
import random
import socket
import sys

import pygame
from pygame.locals import *

from . import objects, layouts

HOST = '0.0.0.0'
PORT = 9027


def terminate_connection(sock):
    print("Connection closed")
    sock.send("Connection closed".encode())
    sock.close()


def terminate():
    pygame.quit()
    sys.exit(0)


ENEMY_MAX_COUNT = 30


def two_players_mode(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    # setup socket and logger
    logger = logging.getLogger("Fucking Server")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("server_info.log")

    # pretty formatting
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    socket.setdefaulttimeout(60)
    sock = socket.socket()

    sock.bind((HOST, PORT))
    sock.listen(100)
    sock.settimeout(0.01)

    print("Serving on ", PORT)
    logger.info('Start serving on %s' % (PORT))

    # setup game
    pygame.mouse.set_visible(False)

    main_clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    background_image_in_game = pygame.image.load("../drawable/backgrounds/background1.jpg")
    background_image_in_game = pygame.transform.scale(background_image_in_game, (WINDOW_WIDTH, WINDOW_HEIGHT))

    meow_hero1 = objects.MeowHero(1, WINDOW_WIDTH / 12, WINDOW_HEIGHT / 12)
    meow_hero1.rect.move_ip(int(WINDOW_WIDTH / 2), 7 * int(WINDOW_HEIGHT / 8))

    meow_hero2 = objects.MeowHero(1, WINDOW_WIDTH / 12, WINDOW_HEIGHT / 12)
    meow_hero2.rect.move_ip(int(WINDOW_WIDTH / 2), 7 * int(WINDOW_HEIGHT / 8))

    move_left1 = move_right1 = move_up1 = move_down1 = False
    move_left2 = move_right2 = move_up2 = move_down2 = False

    # set up music
    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')
    damage_sound = pygame.mixer.Sound('../sound/short_tracks/damage.wav')
    victory_sound = pygame.mixer.Sound('../sound/short_tracks/victory.wav')
    coin_sound = pygame.mixer.Sound('../sound/short_tracks/coin.wav')
    health_sound = pygame.mixer.Sound('../sound/short_tracks/health.wav')
    new_top_sound = pygame.mixer.Sound('../sound/short_tracks/health.wav')
    attack_sound = pygame.mixer.Sound('../sound/short_tracks/attack_1' + ".wav")

    bullets = []
    enemies = []
    enemy_bullets = []
    bonuses = []

    main_timer = 0
    score = 0
    running = True
    while running:  # the game loop runs while the game part is playing
        score += 1  # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                print("Goodbye")
                terminate()

            if event.type == pygame.USEREVENT:
                main_timer += 1
                # victory condition
                if main_timer >= 200:
                    running = False

            # terminating by ESC
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit_state = layouts.interruption_menu(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
                    if quit_state:
                        print("Goodbye")
                        terminate()

        # handling socket
        # TODO: attack event
        data = []
        try:
            conn, address = sock.accept()
            logger.info('Connection from %s on %s' % (address[0], address[1]))
            data = conn.recv(1024).decode()
            print(data)
            logger.info("Income data: %s" % (data))
            data = data.split()

        except Exception:  # exception if timeout
            pass

        # handle data events
        if data:
            # handle first player
            if "1" in data:
                if "Attack" in data:
                    bullet = objects.Bullet(1, WINDOW_WIDTH / 30, WINDOW_HEIGHT / 30)
                    bullet.rect.move_ip(meow_hero1.rect.left, meow_hero1.rect.top)
                    bullets.append(bullet)
                if "R" in data:
                    move_left1 = False
                    move_right1 = True
                if "L" in data:
                    move_left1 = True
                    move_right1 = False
                if "U" in data:
                    move_down1 = False
                    move_up1 = True
                if "D" in data:
                    move_down1 = True
                    move_up1 = False
                if "SH" in data:
                    move_left1 = False
                    move_right1 = False
                if "SV" in data:
                    move_down1 = False
                    move_up1 = False

            # handle second player
            elif "2" in data:
                if "Attack" in data:
                    bullet = objects.Bullet(1, WINDOW_WIDTH / 30, WINDOW_HEIGHT / 30)
                    bullet.rect.move_ip(meow_hero2.rect.left, meow_hero2.rect.top)
                    bullets.append(bullet)
                if "R" in data:
                    move_left2 = False
                    move_right2 = True
                if "L" in data:
                    move_left2 = True
                    move_right2 = False
                if "U" in data:
                    move_down2 = False
                    move_up2 = True
                if "D" in data:
                    move_down2 = True
                    move_up2 = False
                if "SH" in data:
                    move_left2 = False
                    move_right2 = False
                if "SV" in data:
                    move_down2 = False
                    move_up2 = False

        # move the first player around
        if move_left1 and meow_hero1.rect.left > 0:
            meow_hero1.move(-1, 0)
        if move_right1 and meow_hero1.rect.right < WINDOW_WIDTH:
            meow_hero1.move(1, 0)
        if move_up1 and meow_hero1.rect.top > 0:
            meow_hero1.move(0, -1)
        if move_down1 and meow_hero1.rect.bottom < WINDOW_HEIGHT:
            meow_hero1.move(0, 1)

        # move the second player around
        if move_left2 and meow_hero2.rect.left > 0:
            meow_hero2.move(-1, 0)
        if move_right2 and meow_hero2.rect.right < WINDOW_WIDTH:
            meow_hero2.move(1, 0)
        if move_up2 and meow_hero2.rect.top > 0:
            meow_hero2.move(0, -1)
        if move_down2 and meow_hero2.rect.bottom < WINDOW_HEIGHT:
            meow_hero2.move(0, 1)

        # spawn bonuses by time
        if main_timer % 10 == 0 and len(bonuses) <= 1:
            bonus = objects.Bonus("Life", WINDOW_WIDTH / 24, WINDOW_HEIGHT / 24)
            bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            bonuses.append(bonus)
            bonus = objects.Bonus("Coin", WINDOW_WIDTH / 24, WINDOW_HEIGHT / 24)
            bonus.rect.move_ip(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            bonuses.append(bonus)

        # spawn enemy
        if len(enemies) < ENEMY_MAX_COUNT:
            dice = random.random()
            if dice < 0.1:
                # TODO: spawn randomly by time
                enemy = objects.AttackerEnemy(1, WINDOW_WIDTH / 18, WINDOW_HEIGHT / 18)
                enemy.rect.move_ip(random.randint(0, WINDOW_WIDTH), 0)
                enemies.append(enemy)

        # hitting enemy
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.life -= 1
                    bullet.life -= 1
                    attack_sound.play()

        # hitting second and first player
        for enemy in enemies:
            if meow_hero1.rect.colliderect(enemy.rect):
                meow_hero1.life -= 1
                enemies.remove(enemy)
                damage_sound.play()
            elif meow_hero2.rect.colliderect(enemy.rect):
                meow_hero2.life -= 1
                enemies.remove(enemy)
                damage_sound.play()

        # hitting players by bullets
        for bullet in enemy_bullets:
            if meow_hero1.rect.colliderect(bullet.rect):
                meow_hero1.life -= 1
                enemy_bullets.remove(bullet)
                damage_sound.play()
            elif meow_hero2.rect.colliderect(bullet.rect):
                meow_hero2.life -= 1
                enemy_bullets.remove(bullet)
                damage_sound.play()

        # collecting bonuses:
        for bonus in bonuses:
            if meow_hero1.rect.colliderect(bonus.rect):
                if bonus.bonus_type == "Life":
                    meow_hero1.life += 1
                    health_sound.play()
                elif bonus.bonus_type == "Coin":
                    score += 1000
                    coin_sound.play()
                bonuses.remove(bonus)
            elif meow_hero2.rect.colliderect(bonus.rect):
                if bonus.bonus_type == "Life":
                    meow_hero2.life += 1
                    health_sound.play()
                elif bonus.bonus_type == "Coin":
                    score += 1000
                    coin_sound.play()
                bonuses.remove(bonus)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw players
        meow_hero1.draw(window_surface)
        meow_hero2.draw(window_surface)

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
        if meow_hero1.life <= 0 or meow_hero2.life <= 0:
            running = False

        pygame.display.update()
        main_clock.tick(40)  # FPS

    pygame.mouse.set_visible(True)

    sock.close()
