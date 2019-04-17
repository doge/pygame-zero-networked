'''

	server.py
	pygame-zero-networked

    snake_case > all
    https://en.wikipedia.org/wiki/snake_case

'''

import socket, datetime, pickle
import config as cfg
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((cfg.ipv4, cfg.port))
s.listen(2) # max of 2 clients

users = []
positions = [[400.0, 275.0], [0, 0]]

def prefix(): print("<%s> " % datetime.datetime.now().strftime("%H:%M:%S"), end="")

def client_thread(conn, addr):
    while True:
        try:
            data = conn.recv(cfg.buffer_size)
            if not data:
                break
            else:
                for user in users: # send message to all of our users
                    from_client = pickle.loads(data)
                    positions[users.index(user)] = from_client
                    to_send = pickle.dumps(positions)
                    conn.sendall(to_send)
        except:
            break

    prefix()
    print("client disconnected: %s:%s" % (addr[0], addr[1]))
    conn.close()


def main():
    prefix()
    print("server listening on port: %s" % cfg.port)

    while True:
        conn, addr = s.accept()
        users.append(conn)
        prefix()
        print("client connected: %s:%s" % (addr[0], addr[1]))
        start_new_thread(client_thread, (conn, addr))


main()