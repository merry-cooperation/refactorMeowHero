import logging
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

    meow_hero = objects.MeowHero(1, WINDOW_WIDTH / 12, WINDOW_HEIGHT / 12)
    meow_hero.rect.move_ip(int(WINDOW_WIDTH / 2), 7 * int(WINDOW_HEIGHT / 8))

    move_left = move_right = move_up = move_down = False

    bullets = []

    main_timer = 200
    score = 0
    running = True
    while running:  # the game loop runs while the game part is playing
        score += 1  # increase score

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == pygame.USEREVENT:
                main_timer -= 1
                # victory condition
                if main_timer <= 0:
                    running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullet = objects.Bullet(1, WINDOW_WIDTH / 30, WINDOW_HEIGHT / 30)
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
                        terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_right = False
                if event.key == K_UP or event.key == ord('w'):
                    move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    move_down = False

        # handling socket
        try:
            conn, address = sock.accept()
            logger.info('Connection from %s on %s' % (address[0], address[1]))
            data = conn.recv(1024).decode()
            print(data)
            logger.info("Income data: %s" % (data))

            # handle data events
            data = data.split()
            if "Attack" in data:
                pass
            if "R" in data:
                move_left = False
                move_right = True
            if "L" in data:
                move_left = True
                move_right = False
            if "U" in data:
                move_down = False
                move_up = True
            if "D" in data:
                move_down = True
                move_up = False
            if "SH" in data:
                move_left = False
                move_right = False
            if "SV" in data:
                move_down = False
                move_up = False

        except Exception:  # exception if timeout
            pass

        # move the player around
        if move_left and meow_hero.rect.left > 0:
            meow_hero.move(-1, 0)
        if move_right and meow_hero.rect.right < WINDOW_WIDTH:
            meow_hero.move(1, 0)
        if move_up and meow_hero.rect.top > 0:
            meow_hero.move(0, -1)
        if move_down and meow_hero.rect.bottom < WINDOW_HEIGHT:
            meow_hero.move(0, 1)

        # draw background
        window_surface.blit(background_image_in_game, [0, 0])

        # draw hero
        meow_hero.draw(window_surface)

        # check for ending:
        if meow_hero.life <= 0:
            running = False

        pygame.display.update()
        main_clock.tick(40) # FPS

    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

    sock.close()
