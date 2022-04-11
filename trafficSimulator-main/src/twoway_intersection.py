import numpy as np
from trafficSimulator import *

sim = Simulation()

# Play with these
n = 20
a = 2
b = 10
c = 100
l = 274.32

# Nodes
WEST_RIGHT_START = ((-2*b)-l-c, a)
WEST_LEFT_START = ((-2*b)-l-c, -a)

WEST_RIGHT_START_2 = (-c, a)
WEST_LEFT_START_2 = (-c, -a)

#SOUTH_RIGHT_START = (-c-b+a, b+l)
SOUTH_LEFT_START = (-c-b+a, b+l)

SOUTH_RIGHT_START_2 = (b+c+a, b+l)
#SOUTH_LEFT_START_2 = (c+b-a, b+l)

EAST_RIGHT_START = ((2*b)+l+c, -a)
EAST_LEFT_START = ((2*b)+l+c, a)

NORTH_RIGHT_START = (-b+a-c, -b-l)
#NORTH_LEFT_START = (-c-b+a, -b-l)

#NORTH_RIGHT_START_2 = (c+b-a, -b-l)
NORTH_LEFT_START_2 = (b+c+a, -b-l)


WEST_RIGHT = ((-2*b)-c+2*a, a)
WEST_LEFT =	((-2*b)-c+2*a, -a)

WEST_RIGHT_2 = (c+a, a)
WEST_LEFT_2 = (c+a, -a)

#SOUTH_RIGHT = (-c-b+a, b)
SOUTH_LEFT = (a-b-c, b)

SOUTH_RIGHT_2 = (b+c+a, b)
#SOUTH_LEFT_2 = (c+b-a, b)

EAST_RIGHT = ((2*b)+c, -a)
EAST_LEFT = ((2*b)+c, a)

NORTH_RIGHT = (-b-c+a, -b)
#NORTH_LEFT = (-c-b+a, -b)

#NORTH_RIGHT_2 = (c+b-a, -b)
NORTH_LEFT_2 = (b+c+a, -b)

# Roads
WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
#SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
SOUTH_INBOUND_2 = (SOUTH_RIGHT_START_2, SOUTH_RIGHT_2)
EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)
#NORTH_INBOUND_2 = (NORTH_RIGHT_START_2, NORTH_RIGHT_2)

WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
#SOUTH_OUTBOUND_2 = (SOUTH_LEFT_2, SOUTH_LEFT_START_2)
EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
#NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)
NORTH_OUTBOUND_2 = (NORTH_LEFT_2, NORTH_LEFT_START_2)

WEST_STRAIGHT = (WEST_RIGHT, WEST_RIGHT_START_2)
WEST_STRAIGHT_2 = (WEST_RIGHT_START_2, WEST_RIGHT_2)
WEST_STRAIGHT_3 = (WEST_RIGHT_2, EAST_LEFT)
SOUTH_STRAIGHT = (SOUTH_LEFT, NORTH_RIGHT)
SOUTH_STRAIGHT_2 = (SOUTH_RIGHT_2, NORTH_LEFT_2)
EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT_2)
EAST_STRAIGHT_2 = (WEST_LEFT_2, WEST_LEFT_START_2)
EAST_STRAIGHT_3 = (WEST_LEFT_START_2, WEST_LEFT)
NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)
NORTH_STRAIGHT_2 = (NORTH_LEFT_2, SOUTH_RIGHT_2)

WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
WEST_RIGHT_TURN_2 = turn_road(WEST_RIGHT_2, SOUTH_RIGHT_2, TURN_RIGHT, n)

SOUTH_RIGHT_TURN_2 = turn_road(SOUTH_RIGHT_2, EAST_LEFT, TURN_RIGHT, n)
SOUTH_LEFT_TURN_2 = turn_road(SOUTH_RIGHT_2, WEST_LEFT_2, TURN_LEFT, n)

EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT_2, TURN_RIGHT, n)
EAST_RIGHT_TURN_2 = turn_road(WEST_LEFT_START_2, NORTH_RIGHT, TURN_RIGHT, n)

NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, WEST_RIGHT_START_2, TURN_LEFT, n)

SOUTH_RIGHT_TURN = turn_road(SOUTH_LEFT, WEST_RIGHT_START_2, TURN_RIGHT, n)
NORTH_RIGHT_TURN_2 = turn_road(NORTH_LEFT_2, WEST_LEFT_2, TURN_RIGHT, n)

sim.create_roads([
    WEST_INBOUND,
    #SOUTH_INBOUND,
    SOUTH_INBOUND_2,
    EAST_INBOUND,
    NORTH_INBOUND,
    #NORTH_INBOUND_2,

    WEST_OUTBOUND,
    SOUTH_OUTBOUND,
    #SOUTH_OUTBOUND_2,
    EAST_OUTBOUND,
    #NORTH_OUTBOUND,
    NORTH_OUTBOUND_2,

    WEST_STRAIGHT,
    WEST_STRAIGHT_2,
    WEST_STRAIGHT_3,
    SOUTH_STRAIGHT,
    SOUTH_STRAIGHT_2,
    EAST_STRAIGHT,
    EAST_STRAIGHT_2,
    EAST_STRAIGHT_3,
    NORTH_STRAIGHT,
    NORTH_STRAIGHT_2,

    *WEST_RIGHT_TURN,
    *WEST_RIGHT_TURN_2,

    *SOUTH_RIGHT_TURN_2,
    *SOUTH_LEFT_TURN_2,

    *EAST_RIGHT_TURN,
    *EAST_RIGHT_TURN_2,

    *NORTH_RIGHT_TURN,
    *NORTH_LEFT_TURN,

    *SOUTH_RIGHT_TURN,
    *NORTH_RIGHT_TURN_2
])

def road(a): return range(a, a+n)

sim.create_gen({
'car_platoon_rate': 10,
'car_platoons': [
    [1, {'path': [0, 8, 9, 10, 6]}],
    #[1, {'path': [0, 12, 13, *road(22+n), 8]}],
    [1, {'path': [0, *road(18), 5]}],

    [1, {'path': [1, 12, 7]}],
    [1, {'path': [1, *road(18+2*n), 6]}],
    [1, {'path': [1, *road(18+3*n), 14, 15, 4]}],
    #[1, {'path': [2, *road(22+3*n), 18, 19, *road(22+5*n), 10]}],


    [1, {'path': [2, 13, 14, 15, 4]}],
    #[1, {'path': [3, 17, 18, *road(22+5*n), 10]}],
    [1, {'path': [2, *road(18+4*n), 7]}],

    [1, {'path': [3, 16, 5]}],
    [1, {'path': [3, *road(18+6*n), 4]}],
    [1, {'path': [3, *road(18+7*n), 9, 10, 6]}],
    #[1, {'path': [4, *road(22+7*n), 13, *road(22+n), 8]}]

]})

#sim.create_signal([[0, 2, 9, 14], [1, 3]])
#sim.create_signal([[2], [3, 13]])

# Start simulation
win = Window(sim)
win.zoom = 3
win.run(steps_per_update=6)


