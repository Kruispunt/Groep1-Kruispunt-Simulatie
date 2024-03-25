import threading

from connection.client import Client
from simulation.car import Car
from simulation.enums.direction import Direction
from simulation.lane import Lane
from simulation.light import Light
from simulation.enums.state import State
from pygame import *

from simulation.road import Road

init()
display.set_caption("Simulation")
light = Light()
running = True

background = image.load("simulation/images/crossroad-birds-eye-view.png")
# change screen size based on image size
screen = display.set_mode(background.get_size())

roadA = Road("A")

roadA.add_lane(Lane(Direction.east, Vector2(18, 282), Vector2(194, 299)))
roadA.add_lane(Lane(Direction.east, Vector2(0, 0), Vector2(194, 299)))
roadA.add_lane(Lane(Direction.east, Vector2(18, 282), Vector2(194, 299)))
roadA.add_lane(Lane(Direction.east, Vector2(18, 282), Vector2(194, 299)))

clock = time.Clock()


def button_presses():
    lane = roadA.get_lanes()[0]
    # if g is pressed, change light to green
    if key.get_pressed()[K_g]:
        lane.get_light().change(State.green)

    # if r is pressed, change light to red
    if key.get_pressed()[K_r]:
        lane.get_light().change(State.red)

    # if c is pressed, add a car
    if key.get_pressed()[K_c]:
        if not lane.get_cars() or lane.get_cars()[-1].get_position().x > lane.get_start_position().x + \
                lane.get_cars()[
                    -1].get_sprite().get_width():
            lane.add_car()


def is_car_between_positions(self, start_position, end_position):
    return any([
        start_position.x < car.get_position().x < end_position.x and
        start_position.y < car.get_position().y < end_position.y
        for car in self.get_cars()])


def draw_cars():
    for lane in roadA.get_lanes():
        # if none of the cars are in between the light and the start position, set has_car_waiting to False
        if lane.has_car_waiting() and ((not is_car_between_positions(lane, lane.get_start_position(),
                                                                     lane.get_light_position())) or lane.get_light().get_state() == State.green):
            lane.set_has_car_waiting(False)

        for index in range(len(lane.get_cars())):
            car = lane.get_cars()[index]
            # check if the car is at the light, if so, stop the car if the light is red
            # check if there is a car in front and stop the car if there is
            if lane.is_car_at_light(car) and lane.get_light().get_state() == State.red:
                car.stop()
                if not lane.has_car_waiting():
                    client.send(roadA.to_json())
                lane.set_has_car_waiting(True)
            elif index > 0 and lane.get_cars()[index - 1].get_position().distance_to(
                    car.get_position()) < car.get_sprite().get_width():
                car.stop()
            else:
                car.set_speed(1)

            car.move()
            car.draw(screen)
        lane.get_cars()[:] = [car for car in lane.get_cars() if
                              car.get_position().x < screen.get_width() and car.get_position().y < screen.get_height()]


def listen_to_server():
    while True:
        message = client.receive()
        # roadA_get = Road.from_json(message)
        print('Received:', message)
        # roadA.get_lanes[0].get_light().change(roadA_get["A"][0]["state"])


client = Client()

ip = input('Enter the ip: ')
port = int(input('Enter the port: '))
client.connect(ip, port)
print('Connected')

threading.Thread(target=listen_to_server).start()

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    # show background
    screen.blit(background, (0, 0))

    button_presses()
    draw_cars()

    # show screen
    display.flip()

    # 60 fps
    clock.tick(60)

client.close()
quit()
