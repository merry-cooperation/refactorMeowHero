"""
Our future server
"""

import logging
import socket
import time

HOST = '0.0.0.0'
PORT = 9027

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
sock.listen(2)

print("Hello from server")
logger.info('Start serving on %s' % (PORT))

while True:
    conn, address = sock.accept()
    data = conn.recv(1024)

    logger.info('Connection from %s on %s' % (address[0], address[1]))

    print('Connection:', address)
    print('------------------------------')
    print("Request Data")
    print('------------------------------')
    print(data.decode())

    conn.send(data)
    conn.close()

    # do not load the CPU
    time.sleep(0.1)
