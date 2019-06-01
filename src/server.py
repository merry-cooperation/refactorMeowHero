import base64
import json
import logging
import pygame
import socket
import sys

HOST = '0.0.0.0'
PORT = 9027


def terminate():
    pygame.quit()
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

    sock = socket.socket()

    sock.bind((HOST, PORT))
    sock.listen(100)

    print("Serving on ", PORT)
    logger.info('Start serving on %s' % (PORT))

    while True:
        conn, address = sock.accept()
        logger.info('Connection first from %s on %s' % (address[0], address[1]))
        data = conn.recv(1024).decode()
        conn.send(data.encode())
        print(data)
        logger.info("Income data: %s" % (data))

    # logger.info('Connection from %s on %s closed' % (address[0], address[1]))

    sock.close()


if __name__ == "__main__":
    test()
