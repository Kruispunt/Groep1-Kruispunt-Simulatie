from pygame import transform
from pygame.math import Vector2


class Car:
    def __init__(self, speed, position, direction, sprite):
        self._speed = speed
        self._position = position
        self._direction = direction.normalize()
        self._sprite = sprite
        self.__set_direction_of_sprite()

    def __set_direction_of_sprite(self):
        self._sprite = transform.rotate(self._sprite, self._direction.angle_to(Vector2(0, 1)))
        self._sprite.set_colorkey((255, 255, 255))

    def set_speed(self, speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position

    def set_direction(self, direction):
        self._direction = direction.normalize()
        self.__set_direction_of_sprite()

    def get_direction(self):
        return self._direction

    def set_sprite(self, sprite):
        self._sprite = sprite
        self.__set_direction_of_sprite()

    def get_sprite(self):
        return self._sprite

    def move(self):
        self._position += self._direction * self._speed

    def draw(self, screen):
        screen.blit(self._sprite, self._position)

    def stop(self):
        self._speed = 0

    # def is_out_of_screen(self, screen):
    #     return self._position.x < 0 or self._position.x > screen.get_width() or self._position.y < 0 or self._position.y > screen.get_height()
