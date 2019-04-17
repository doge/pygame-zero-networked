'''

	client.py
	pygame-zero-networked

    snake_case > all
    https://en.wikipedia.org/wiki/snake_case

'''

import pgzrun as game, socket, pickle, time
import config as cfg

blue_square = Actor("blue_square.png", (400, 275))
red_square = Actor("red_square.png", (400, 275))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init_connection():
    while True:
        try:
            s.connect((cfg.ipv4, cfg.port))
            break
        except socket.error as e:
            #print(e)
            print("failed to connect...")
            time.sleep(2)


def update():
    if keyboard.UP:
        blue_square.y -= 5
    if keyboard.DOWN:
        blue_square.y += 5
    if keyboard.LEFT:
        blue_square.x -= 5
    if keyboard.RIGHT:
        blue_square.x += 5

    player_position = [blue_square.x, blue_square.y]
    to_send = pickle.dumps(player_position)
    s.send(to_send) # sends out our position to the server


    time.sleep(0.00001) # this small delay minimizes desynchronization between clients/server

    data = s.recv(cfg.buffer_size)
    array = pickle.loads(data)

    #print(array)

    # set the actors as coords from the server
    blue_square.x = array[0][0] # local player
    blue_square.y = array[0][1]

    red_square.x = array[1][0] # other player
    red_square.y = array[1][1]

    # note, each player shows up as the opposite object on the other screen. (i.e. if your character is blue, enemy is red)


def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    blue_square.draw()
    red_square.draw()


init_connection()
game.go()