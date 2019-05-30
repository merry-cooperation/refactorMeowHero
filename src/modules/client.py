import base64
import json
import logging
import pygame
import socket

from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def terminate_connection(sock):
    print("Connection closed")
    sock.send("Connection closed".encode())
    sock.close()


def open_tcp_protocol(host, port, window_surface):
    sock = socket.socket()

    logger = logging.getLogger("Fucking Client")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("client_info.log")

    # pretty formatting
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    sock.connect((host, port))

    # TODO: add logs
    # TODO: refactor this part
    # TODO: add normal protocol
    running = True
    while running:  # the game loop runs while the game part is playing
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                events.append((event.type, None))
                terminate_connection(sock)
                running = False

            if event.type == KEYDOWN:
                events.append((event.type, event.key))

            if event.type == KEYUP:
                events.append((event.type, event.key))

        print(events)
        json_string = json.dumps(events)
        try:
            sock.send(json_string.encode())
        except BrokenPipeError:
            print("Broken pipe")
            running = False
            return

        data = sock.recv(32000)

        if data:
            image_data = base64.b64decode(data)

            with open('temp_background.jpg', 'wb') as f:
                f.write(image_data)

            # try to draw background
            try:
                background_image1 = pygame.image.load('temp_background.jpg')
            except pygame.error:
                print("SOOQA")
                continue

            background_image1 = pygame.transform.scale(background_image1, (WINDOW_WIDTH, WINDOW_HEIGHT))

            window_surface.blit(background_image1, [0, 0])

        pygame.display.update()
