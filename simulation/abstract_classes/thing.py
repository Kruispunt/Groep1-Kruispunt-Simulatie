from abc import abstractmethod, ABC

from pygame import transform, Vector2


class Thing(ABC):
    # speed, position, sprite, destination

    def _init(self, speed, position, sprite, destination, size):
        self._speed = speed
        self._position = position
        self._direction = (destination - position).normalize()
        self._original_sprite = sprite
        self._sprite = sprite
        self._size = size
        self._destination = destination
        self._current_rotation = 90
        self._set_direction_of_sprite()

    def _set_direction_of_sprite(self):
        # Rotate the sprite to face the direction of the car, take into account the current rotation of the sprite
        # and the angle between the current direction and the new direction
        angle = self._direction.angle_to(Vector2(1, 0)) - self._current_rotation
        self._current_rotation += angle
        self._sprite = transform.rotate(self._sprite, angle)

        self._sprite.set_colorkey((255, 255, 255))

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

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
        self._set_direction_of_sprite()

    def get_direction(self):
        return self._direction

    def set_sprite(self, sprite):
        self._sprite = sprite
        self._set_direction_of_sprite()

    def get_sprite(self):
        return self._sprite

    def get_original_sprite(self):
        return self._original_sprite

    def get_current_rotation(self):
        return self._current_rotation

    def get_destination(self):
        return self._destination

    def set_destination(self, destination):
        self._destination = destination

    def move(self):
        self._position += self._direction * self._speed

    def draw(self, screen):
        screen.blit(self._sprite, self._position)

    def stop(self):
        self._speed = 0

    def move_to(self, position):
        self._destination = position
        self._direction = (position - self._position).normalize()
        self._set_direction_of_sprite()
