import threading
from random import randint

import pygame

from connection.client import Client
from simulation.objects.car import Car
from simulation.light import Light
from simulation.enums.state import State
from pygame import *

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
    # get random car_lane
    road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]

    random_num = randint(0, len(road.get_car_lanes()) - 1)
    car_lane = road.get_car_lanes()[random_num]

    # if g is pressed, change light to green
    if key.get_pressed()[K_g]:
        for lane2 in road.get_car_lanes():
            lane2.change_light(State.green)

    # if r is pressed, change light to red
    if key.get_pressed()[K_r]:
        for lane2 in road.get_car_lanes():
            lane2.change_light(State.red)

    # if c is pressed, add a car
    if key.get_pressed()[K_c]:
        print(road.get_name())
        car_lane.add(Car(speed=3, sprite=None), sprite=image.load("simulation/images/car" + randint(0, 1).__str__() + ".png"))
    if mouse.get_pressed()[0]:
        print("Vector2" + mouse.get_pos().__str__() + ",")


def draw_cars():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            for car_lane in road.get_car_lanes():
                car_lane.set_has_waiting(
                    sum([1 for car in car_lane.get_all() if car.get_destination() == car_lane.get_light_position()]) >= 1)
                car_lane.set_has_waiting_far(
                    sum([1 for car in car_lane.get_all() if car.get_destination() == car_lane.get_light_position()]) >= 5)

                for car in car_lane.get_all():
                    is_moving = True
                    # car destination is at light
                    if car.get_destination() == car_lane.get_light_position():
                        if car.get_position().distance_to(car_lane.get_light_position()) < 5:
                            if car_lane.light_state() == State.red:
                                is_moving = False
                    # car destination is not at light
                    else:
                        next_car = None
                        if car_lane.get_connection() is not None:
                            next_car = None if len(car_lane.get_connection().get_all()) == 0 else car_lane.get_connection().get_all()[-1]
                        if next_car is not None:
                            distance = car.get_position().distance_to(next_car.get_position())
                            if distance < 40:
                                is_moving = False
                    index = car_lane.get_all().index(car)

                    if index > 0 and car_lane.get_all()[index - 1].get_position().distance_to(car.get_position()) < 40:
                        is_moving = False

                    if is_moving:
                        car.move()
                    if car.get_direction().dot(car.get_destination() - car.get_position()) < 0:
                        # move car to the next position
                        if car_lane.get_inbetween_positions():
                            # check for each position in the inbetween positions if the car destination is the same with lambda
                            next_position_index = next(
                                (i for i, x in enumerate(car_lane.get_inbetween_positions()) if x == car.get_destination()),
                                -1) + 1

                            if next_position_index < len(car_lane.get_inbetween_positions()):
                                car.move_to(car_lane.get_inbetween_positions()[next_position_index])
                            else:
                                if car_lane.get_connection() is not None:
                                    car_lane.get_connection().add_car(car.get_original_sprite())
                                car_lane.remove(car)

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

def draw_cyclists():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            cyclist_lane = road.get_cyclist_lanes()
            for cyclist_lane in road.get_cyclist_lanes():
                cyclist_lane.set_has_waiting(
                    any([1 for cyclist in cyclist_lane.get_all() if cyclist.get_destination() == cyclist_lane.get_light_position()]))

                for cyclist in cyclist_lane.get_all():
                    is_moving = True
                    # cyclist destination is at light
                    if cyclist.get_destination() == cyclist_lane.get_light_position():
                        if cyclist.get_position().distance_to(cyclist_lane.get_light_position()) < 5:
                            if cyclist_lane.light_state() == State.red:
                                is_moving = False
                    # cyclist destination is not at light
                    else:
                        next_cyclist = None
                        if cyclist_lane.get_connection() is not None:
                            next_cyclist = None if len(cyclist_lane.get_connection().get_all()) == 0 else cyclist_lane.get_connection().get_all()[-1]
                        if next_cyclist is not None:
                            distance = cyclist.get_position().distance_to(next_cyclist.get_position())
                            if distance < 40:
                                is_moving = False
                    index = cyclist_lane.get_all().index(cyclist)

                    if index > 0 and cyclist_lane.get_all()[index - 1].get_position().distance_to(cyclist.get_position()) < 40:
                        is_moving = False

                    if is_moving:
                        cyclist.move()
                    if cyclist.get_direction().dot(cyclist.get_destination() - cyclist.get_position()) < 0:
                        # move cyclist to the next position
                        if cyclist_lane.get_inbetween_positions():
                            # check for each position in the inbetween positions if the cyclist destination is the same with lambda
                            next_position_index = next(
                                (i for i, x in enumerate(cyclist_lane.get_inbetween_positions()) if x == cyclist.get_destination()),
                                -1) + 1

                            if next_position_index < len(cyclist_lane.get_inbetween_positions()):
                                cyclist.move_to(cyclist_lane.get_inbetween_positions()[next_position_index])
                            else:
                                if cyclist_lane.get_connection() is not None:
                                    cyclist_lane.get_connection().add_cyclist_lane(cyclist.get_original_sprite())
                                cyclist_lane.remove(cyclist)

                    scaled_width = int(cyclist.get_original_sprite().get_width() * scale_factor)
                    scaled_height = int(cyclist.get_original_sprite().get_height() * scale_factor)
                    scaled_cyclist_image = pygame.transform.scale(cyclist.get_original_sprite(), (scaled_width, scaled_height))
                    scaled_cyclist_image = transform.rotate(scaled_cyclist_image,
                                                        cyclist.get_direction().angle_to(Vector2(1, 0)) - 90)
                    scaled_cyclist_image.set_colorkey((255, 255, 255))

                    # adjust cyclist position to the new scale
                    scaled_position = (
                        cyclist.get_position()[0] * scale_factor + offset_x,
                        cyclist.get_position()[1] * scale_factor + offset_y)

                    screen.blit(scaled_cyclist_image, scaled_position)

def draw_pedestrians():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            for pedestrian_lane in road.get_pedestrian_lanes():
                pedestrian_lane.set_has_waiting(
                    any([1 for pedestrian in pedestrian_lane.get_all() if pedestrian.get_destination() == pedestrian_lane.get_light_position()]))

                for pedestrian in pedestrian_lane.get_all():
                    is_moving = True
                    # pedestrian destination is at light
                    if pedestrian.get_destination() == pedestrian_lane.get_light_position():
                        if pedestrian.get_position().distance_to(pedestrian_lane.get_light_position()) < 5:
                            if pedestrian_lane.light_state() == State.red:
                                is_moving = False
                    # pedestrian destination is not at light
                    else:
                        next_pedestrian = None
                        if pedestrian_lane.get_connection() is not None:
                            next_pedestrian = None if len(pedestrian_lane.get_connection().get_all()) == 0 else pedestrian_lane.get_connection().get_all()[-1]
                        if next_pedestrian is not None:
                            distance = pedestrian.get_position().distance_to(next_pedestrian.get_position())
                            if distance < 25:
                                is_moving = False
                    index = pedestrian_lane.get_all().index(pedestrian)

                    if index > 0 and pedestrian_lane.get_all()[index - 1].get_position().distance_to(pedestrian.get_position()) < 25:
                        is_moving = False

                    if is_moving:
                        pedestrian.move()
                    if pedestrian.get_direction().dot(pedestrian.get_destination() - pedestrian.get_position()) < 0:
                        # move pedestrian to the next position
                        if pedestrian_lane.get_inbetween_positions():
                            # check for each position in the inbetween positions if the pedestrian destination is the same with lambda
                            next_position_index = next(
                                (i for i, x in enumerate(pedestrian_lane.get_inbetween_positions()) if x == pedestrian.get_destination()),
                                -1) + 1

                            if next_position_index < len(pedestrian_lane.get_inbetween_positions()):
                                pedestrian.move_to(pedestrian_lane.get_inbetween_positions()[next_position_index])
                            else:
                                if pedestrian_lane.get_connection() is not None:
                                    pedestrian_lane.get_connection().add_pedestrian(pedestrian.get_original_sprite())
                                pedestrian_lane.remove(pedestrian)

                    scaled_width = int(pedestrian.get_original_sprite().get_width() * scale_factor)
                    scaled_height = int(pedestrian.get_original_sprite().get_height() * scale_factor)
                    scaled_pedestrian_image = pygame.transform.scale(pedestrian.get_original_sprite(), (scaled_width, scaled_height))
                    scaled_pedestrian_image = transform.rotate(scaled_pedestrian_image,
                                                        pedestrian.get_direction().angle_to(Vector2(1, 0)) - 90)
                    scaled_pedestrian_image.set_colorkey((255, 255, 255))

                    # adjust pedestrian position to the new scale
                    scaled_position = (
                        pedestrian.get_position()[0] * scale_factor + offset_x,
                        pedestrian.get_position()[1] * scale_factor + offset_y)

                    screen.blit(scaled_pedestrian_image, scaled_position)

def show_lights():
    for intersection in simulation.intersections:
        for road in intersection.get_roads():
            for thing_lane in road.get_car_lanes() + road.get_cyclist_lanes() + road.get_pedestrian_lanes():
                #move with zoom
                scaled_light_position = (
                    thing_lane.get_light_position()[0] * scale_factor + offset_x,
                    thing_lane.get_light_position()[1] * scale_factor + offset_y)
                #scale with zoom
                scaled_radius = 5 * scale_factor
                if thing_lane.light_state() == State.red:
                    draw.circle(screen, (255, 0, 0), scaled_light_position, scaled_radius)
                elif thing_lane.light_state() == State.green:
                    draw.circle(screen, (0, 255, 0), scaled_light_position, scaled_radius)
                elif thing_lane.light_state() == State.orange:
                    draw.circle(screen, (255, 255, 0), scaled_light_position, scaled_radius)


def listen_to_server():
    while running:
        try:
            message = client.receive()
            print('Received:', message)
            simulation.from_json(message)
        except Exception as e:
            print(e)


def send_to_server():
    while running:
        # every 0.5 seconds send the intersection to the server
        time.wait(500)
        try:
            print('Sending:', simulation.to_json())
            client.send(simulation.to_json())
        except Exception as e:
            print(e)


def spawn_random_car():
    while running:
        time.wait(400)
        road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]
        # length of roads
        random_num = randint(0, len(road.get_car_lanes()) - 1)
        car_lane = road.get_car_lanes()[random_num]
        random_num = randint(0, 1)
        if car_lane.is_spawnable():
            car_lane.add_car(image.load("simulation/images/car" + randint(0, 1).__str__() + ".png"))

def spawn_random_cyclist_pedestrian():
    while running:
        time.wait(700)
        road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]
        # length of roads
        length = len(road.get_cyclist_lanes())
        if length != 0:
            random_num = randint(0, len(road.get_cyclist_lanes()) - 1)
            cyclist_lane = road.get_cyclist_lanes()[random_num]
            if cyclist_lane.is_spawnable():
                cyclist_lane.add_cyclist(image.load("simulation/images/cyclist.png"))

        road = simulation.intersections[randint(0, 1)].get_roads()[randint(0, 2)]
        length = len(road.get_pedestrian_lanes())
        if length != 0:
            random_num = randint(0, len(road.get_pedestrian_lanes()) - 1)
            pedestrian_lane = road.get_pedestrian_lanes()[random_num]
            if pedestrian_lane.is_spawnable():
                pedestrian_lane.add_pedestrian(image.load("simulation/images/pedestrian.png"))

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
threading.Thread(target=spawn_random_cyclist_pedestrian).start()

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
        draw_cyclists()
        draw_pedestrians()
        show_lights()

        # Show screen
        display.flip()

        # 24 fps
        clock.tick(24)
    except Exception as e:
        print(e)

client.close()
quit()
