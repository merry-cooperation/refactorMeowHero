import base64
import json
import logging
import pygame
import socket
import sys

HOST = '0.0.0.0'
PORT = 9027
sock = socket.socket()


def terminate():
    pygame.quit()
    sock.close()
    sys.exit(0)


def test():
    logger = logging.getLogger("Fucking Server")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("server_info.log")

    # pretty formatting
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    sock.bind((HOST, PORT))
    sock.listen(2)

    print("Serving on ", PORT)
    logger.info('Start serving on %s' % (PORT))

    conn1, address1 = sock.accept()
    logger.info('Connection first from %s on %s' % (address1[0], address1[1]))

    while True:
        try:
            data = conn1.recv(1024).decode()
        except Exception:
            break
        print(data)
        logger.info("Income data: ", data)

    conn1.close()
    logger.info('Connection from %s on %s closed' % (address1[0], address1[1]))


if __name__ == "__main__":
    test()
