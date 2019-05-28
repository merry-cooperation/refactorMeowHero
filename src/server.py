import json
import logging
import pygame
import socket
import sys

from pygame.locals import *

HOST = '0.0.0.0'
PORT = 9027
sock = socket.socket()


def terminate():
    pygame.quit()
    sock.close()
    sys.exit()


logger = logging.getLogger("Fucking Server")
logger.setLevel(logging.INFO)

fh = logging.FileHandler("server_info.log")

# pretty formatting
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)


sock.bind((HOST, PORT))
sock.listen(100)

print("Hello from server")
logger.info('Start serving on %s' % (PORT))

conn1, address1 = sock.accept()
logger.info('Connection first from %s on %s' % (address1[0], address1[1]))

# conn2, address2 = sock.accept()
# logger.info('Connection second from %s on %s' % (address2[0], address2[1]))

while True:
    data = conn1.recv(1024).decode()

    if data:
        if data == "Connection closed":
            print(data)
            break

        print('Connection:', address1)
        print('------------------------------')
        print("Request Data")
        print('------------------------------')
        print(data)

        data = json.loads(data)

        for event_type, event_key in data:
            if event_type == QUIT:
                terminate()

            if event_type == KEYDOWN:
                if event_key == ord('z'):
                    reverse_cheat = True
                if event_key == ord('x'):
                    slow_cheat = True
                if event_key == K_LEFT or event_key == ord('a'):
                    move_right = False
                    move_left = True
                if event_key == K_RIGHT or event_key == ord('d'):
                    move_left = False
                    move_right = True
                if event_key == K_UP or event_key == ord('w'):
                    move_down = False
                    move_up = True
                if event_key == K_DOWN or event_key == ord('s'):
                    move_up = False
                    move_down = True

            if event_type == KEYUP:
                if event_key == ord('z'):
                    reverse_cheat = False
                    score = 0
                if event_key == ord('x'):
                    slow_cheat = False
                    score = 0
                if event_key == K_ESCAPE:
                    terminate()

                if event_key == K_LEFT or event_key == ord('a'):
                    move_left = False
                if event_key == K_RIGHT or event_key == ord('d'):
                    move_right = False
                if event_key == K_UP or event_key == ord('w'):
                    move_up = False
                if event_key == K_DOWN or event_key == ord('s'):
                    move_down = False

        data = json.dumps(data)
        conn1.send(data.encode())

logger.info('Connection from %s on %s closed' % (address1[0], address1[1]))
