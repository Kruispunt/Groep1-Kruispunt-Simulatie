import threading
from itertools import count
from random import randint

import pygame

from connection.client import Client
from simulation.enums.direction import Direction
from simulation.intersection import Intersection
from simulation.lane import Lane
from simulation.light import Light
from simulation.enums.state import State
from pygame import *

from simulation.road import Road

init()
display.set_caption("Simulation")
light = Light()
running = True

intersection = Intersection(1400, 800, "1")

# change screen size to 1400x800
screen = display.set_mode((1400, 800))

roadA = Road("A")
roadA.add_lane(Lane(Direction.east, Vector2(0, 418), [Vector2(977, 469)], Vector2(80, 427)))
roadA.add_lane(Lane(Direction.east, Vector2(0, 451), [Vector2(0, 0)], Vector2(80, 455)))
roadA.add_lane(Lane(Direction.east, Vector2(0, 475), [Vector2(185, 517), Vector2(227, 561), Vector2(246, 612), Vector2(245, 774)],Vector2(80, 485)))
roadA.add_lane(Lane(Direction.east, Vector2(0, 500), [Vector2(155, 533), Vector2(220, 572), Vector2(220, 748), ],Vector2(75, 516)))

roadB = Road("B")
roadB.add_lane(Lane(Direction.west, Vector2(293, 797),[Vector2(289, 575), Vector2(260, 466), Vector2(180, 342), Vector2(107, 314), Vector2(-100, 317)],Vector2(293, 650)))
roadB.add_lane(Lane(Direction.west, Vector2(1400, 451), [Vector2(0, 0)], Vector2(1288, 455)))
roadB.add_lane(Lane(Direction.west, Vector2(1400, 475), [Vector2(0, 0)], Vector2(1294, 485)))
roadB.add_lane(Lane(Direction.west, Vector2(360, 798), [Vector2(372, 520), Vector2(455, 410), Vector2(975, 420)],Vector2(358, 650)))

roadC = Road("C")
roadC.add_lane(Lane(Direction.south, Vector2(667, 362), [Vector2(335, 375), Vector2(285, 434), Vector2(222, 579), Vector2(218, 800)], Vector2(435, 363)))
roadC.add_lane(Lane(Direction.south, Vector2(0, 0), [Vector2(0, 0)], Vector2(0, 0)))
roadC.add_lane(Lane(Direction.south, Vector2(0, 0), [Vector2(0, 0)], Vector2(0, 0)))
roadC.add_lane(Lane(Direction.south, Vector2(667, 286), [Vector2(-50, 281)], Vector2(435, 286)))

intersection.add_road(roadA)
intersection.add_road(roadB)
intersection.add_road(roadC)

clock = time.Clock()


def button_presses():
    # get random lane
    random_num = 0 if randint(0, 1) == 0 else 3
    road = intersection.get_roads()[randint(0, 2)]
    lane = road.get_lanes()[random_num]

    # if g is pressed, change light to green
    if key.get_pressed()[K_g]:
        for lane2 in road.get_lanes():
            lane2.get_light().change(State.green)

    # if r is pressed, change light to red
    if key.get_pressed()[K_r]:
        for lane2 in road.get_lanes():
            lane2.get_light().change(State.red)

    # if c is pressed, add a car
    if key.get_pressed()[K_c]:
        print(road.get_name())
        lane.add_car()
    if mouse.get_pressed()[0]:
        print("Vector2" + mouse.get_pos().__str__() + ",")


def draw_cars():
    for road in intersection.get_roads():
        for lane in road.get_lanes():
            lane.set_has_car_waiting(sum([1 for car in lane.get_cars() if car.get_destination() == lane.get_light_position()]) >= 1)
            lane.set_has_car_waiting_far(sum([1 for car in lane.get_cars() if car.get_destination() == lane.get_light_position()]) >= 5)

            for car in lane.get_cars():
                if car.get_destination() == lane.get_light_position():
                    if car.get_position().distance_to(lane.get_light_position()) < 5:
                        if lane.get_light().get_state() != State.red:
                            car.move()
                    else:
                        index = lane.get_cars().index(car)
                        if index > 0:
                            if not lane.get_cars()[index - 1].get_position().distance_to(car.get_position()) < 40:
                                car.move()
                        else:
                            car.move()
                else:
                    car.move()
                if car.get_direction().dot(car.get_destination() - car.get_position()) < 0:
                    # move car to the next position
                    if lane.get_inbetween_positions():
                        # check for each position in the inbetween positions if the car destination is the same with lambda
                        next_position_index = next(
                            (i for i, x in enumerate(lane.get_inbetween_positions()) if x == car.get_destination()),
                            -1) + 1

                        if next_position_index < len(lane.get_inbetween_positions()):
                            car.move_to(lane.get_inbetween_positions()[next_position_index])
                        else:
                            car.move_to(lane.get_light_position())
                            lane.remove_car(car)

                scaled_width = int(car.get_original_sprite().get_width() * scale_factor)
                scaled_height = int(car.get_original_sprite().get_height() * scale_factor)
                scaled_car_image = pygame.transform.scale(car.get_original_sprite(), (scaled_width, scaled_height))
                scaled_car_image = transform.rotate(scaled_car_image, car.get_direction().angle_to(Vector2(1, 0)) - 90)
                scaled_car_image.set_colorkey((255, 255, 255))

                # adjust car position to the new scale
                scaled_position = (
                car.get_position()[0] * scale_factor + offset_x, car.get_position()[1] * scale_factor + offset_y)

                screen.blit(scaled_car_image, scaled_position)



def listen_to_server():
    try:
        while running:
            message = client.receive()
            print('Received:', message)
            intersection.from_json(message)
    except Exception as e:
        print(e)


def send_to_server():
    try:
        while running:
            # every 0.5 seconds send the intersection to the server
            time.wait(5000)
            print('Sending:', intersection.to_json())
            client.send(intersection.to_json())
    except Exception as e:
        print(e)


def spawn_random_car():
    while running:
        time.wait(400)
        random_num = 0 if randint(0, 1) == 0 else 3
        road = intersection.get_roads()[randint(0, 2)]
        lane = road.get_lanes()[random_num]
        lane.add_car()


client = Client()

ip = input('Enter the ip: ')
port = int(input('Enter the port: '))
# ip = '127.0.0.1'
# port = 12345
client.connect(ip, port)
print('Connected')

threading.Thread(target=listen_to_server).start()
threading.Thread(target=send_to_server).start()
threading.Thread(target=spawn_random_car).start()

MAX_WIDTH = 1400
MAX_HEIGHT = 800
scale_factor = 1.0
mouse_position = (0, 0)


def event_loop():
    global scale_factor, running, mouse_position
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 4 and scale_factor * MAX_WIDTH < 3 * MAX_WIDTH:
                scale_factor *= 1.1
                mouse_position = e.pos
            elif e.button == 5 and scale_factor * MAX_WIDTH > MAX_WIDTH:
                scale_factor /= 1.1
                mouse_position = e.pos
        if e.type == MOUSEMOTION:
            mouse_position = e.pos

def zoom(width, height):
    global scale_factor, mouse_position
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)

    scaled_mouse_x = (mouse_position[0] / width) * scaled_width
    scaled_mouse_y = (mouse_position[1] / height) * scaled_height

    offset_x = mouse_position[0] - scaled_mouse_x
    offset_y = mouse_position[1] - scaled_mouse_y
    return scaled_width, scaled_height, offset_x, offset_y


while running:
    try:
        event_loop()

        scaled_width, scaled_height, offset_x, offset_y = zoom(MAX_WIDTH, MAX_HEIGHT)
        scaled_background = transform.scale(intersection.get_background(), (scaled_width, scaled_height))
        screen.blit(scaled_background, (offset_x, offset_y))

        button_presses()
        draw_cars()

        # Show screen
        display.flip()

        # 24 fps
        clock.tick(24)
    except Exception as e:
        print(e)

client.close()
quit()
