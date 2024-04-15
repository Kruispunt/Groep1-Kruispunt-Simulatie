import threading
from itertools import count
from random import randint

import pygame

from connection.client import Client
from simulation.intersection import Intersection
from simulation.lane import Lane
from simulation.light import Light
from simulation.enums.state import State
from pygame import *

from simulation.road import Road
from simulation.simulation import Simulation

init()
display.set_caption("Simulation")
light = Light()
running = True

simulation = Simulation(1400, 800)

# change screen size to 1400x800
screen = display.set_mode((simulation.get_width(), simulation.get_height()))

clock = time.Clock()


def button_presses():
    # get random lane
    road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]

    random_num = randint(0, len(road.get_lanes()) - 1)
    lane = road.get_lanes()[random_num]

    # if g is pressed, change light to green
    if key.get_pressed()[K_g]:
        for lane2 in road.get_lanes():
            lane2.change_light(State.green)

    # if r is pressed, change light to red
    if key.get_pressed()[K_r]:
        for lane2 in road.get_lanes():
            lane2.change_light(State.red)

    # if c is pressed, add a car
    if key.get_pressed()[K_c]:
        print(road.get_name())
        lane.add_car()
    if mouse.get_pressed()[0]:
        print("Vector2" + mouse.get_pos().__str__() + ",")


def draw_cars():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            for lane in road.get_lanes():
                lane.set_has_car_waiting(
                    sum([1 for car in lane.get_cars() if car.get_destination() == lane.get_light_position()]) >= 1)
                lane.set_has_car_waiting_far(
                    sum([1 for car in lane.get_cars() if car.get_destination() == lane.get_light_position()]) >= 5)

                for car in lane.get_cars():
                    is_moving = True
                    # car destination is at light
                    if car.get_destination() == lane.get_light_position():
                        if car.get_position().distance_to(lane.get_light_position()) < 5:
                            if lane.light_state() == State.red:
                                is_moving = False
                    # car destination is not at light
                    else:
                        next_car = None
                        if lane.get_connection() is not None:
                            next_car = None if len(lane.get_connection().get_cars()) == 0 else lane.get_connection().get_cars()[-1]
                        if next_car is not None:
                            distance = car.get_position().distance_to(next_car.get_position())
                            if distance < 40:
                                is_moving = False
                    index = lane.get_cars().index(car)

                    if index > 0 and lane.get_cars()[index - 1].get_position().distance_to(car.get_position()) < 40:
                        is_moving = False

                    if is_moving:
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
                                if lane.get_connection() is not None:
                                    lane.get_connection().add_car(car.get_original_sprite())
                                lane.remove_car(car)

                    scaled_width = int(car.get_original_sprite().get_width() * scale_factor)
                    scaled_height = int(car.get_original_sprite().get_height() * scale_factor)
                    scaled_car_image = pygame.transform.scale(car.get_original_sprite(), (scaled_width, scaled_height))
                    scaled_car_image = transform.rotate(scaled_car_image,
                                                        car.get_direction().angle_to(Vector2(1, 0)) - 90)
                    scaled_car_image.set_colorkey((255, 255, 255))

                    # adjust car position to the new scale
                    scaled_position = (
                        car.get_position()[0] * scale_factor + offset_x,
                        car.get_position()[1] * scale_factor + offset_y)

                    screen.blit(scaled_car_image, scaled_position)


def show_lights():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            for lane in road.get_lanes():
                if lane.light_state() == State.red:
                    draw.circle(screen, (255, 0, 0), lane.get_light_position(), 5)
                elif lane.light_state() == State.green:
                    draw.circle(screen, (0, 255, 0), lane.get_light_position(), 5)
                elif lane.light_state() == State.orange:
                    draw.circle(screen, (255, 255, 0), lane.get_light_position(), 5)

def listen_to_server():
    try:
        while running:
            message = client.receive()
            print('Received:', message)
            simulation.from_json(message)
    except Exception as e:
        print(e)


def send_to_server():
    try:
        while running:
            # every 0.5 seconds send the intersection to the server
            time.wait(5000)
            print('Sending:', simulation.to_json())
            # client.send(simulation.to_json())
    except Exception as e:
        print(e)


def spawn_random_car():
    while running:
        time.wait(200)
        road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]
        # length of roads
        random_num = randint(0, len(road.get_lanes()) - 1)
        lane = road.get_lanes()[random_num]
        if not lane.is_spawnable():
            continue
        lane.add_car()


client = Client()

# ip = input('Enter the ip: ')
# port = int(input('Enter the port: '))
ip = '127.0.0.1'
port = 12345
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
        scaled_background = transform.scale(simulation.get_background(), (scaled_width, scaled_height))
        screen.blit(scaled_background, (offset_x, offset_y))

        button_presses()
        draw_cars()
        show_lights()

        # Show screen
        display.flip()

        # 24 fps
        clock.tick(24)
    except Exception as e:
        print(e)

client.close()
quit()
