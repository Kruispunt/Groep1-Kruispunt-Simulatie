from enum import Enum


class Direction(Enum):
    none = 0
    north = 1
    south = 2
    east = 4
    west = 8

    ns = 3
    ne = 5
    nw = 9

    se = 6
    sw = 10

    ew = 12

    nse = 7
    nsw = 11
    new = 13
    sew = 14

    vertical = 3
    horizontal = 12
    all = 15
