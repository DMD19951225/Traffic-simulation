import numpy as np
from .vehicle import Vehicle
import random


class Car_platoon:
    def __init__(self, platoon_id, config={}):
        self.ss = 3
        self.l = 4
        self.platoon_id = platoon_id
        self.count = random.randint(2, 5)
        self.L = self.count * self.l + (self.count - 1) * self.ss

        self.car_platoon = []
        self.path = []
        self.add_vehicle()

        self.current_road_index = 0

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        for i in range(self.count):
            self.car_platoon[i].path = self.path
        self.v_max =self.car_platoon[0].v_max
        self.sqrt_ab = 2 * np.sqrt(self.car_platoon[0].a_max * self.car_platoon[0].b_max)
        self._v_max = self.v_max

    def add_vehicle(self):
        for i in range(self.count):
            self.car_platoon.append(Vehicle())
            self.car_platoon[i].x = self.L - i * (self.l + self.ss)
            self.car_platoon[i].path = self.path
            self.car_platoon[i].platoon_id = self.platoon_id

    def update(self, lead, dt):
        # Update position and velocity
        if self.car_platoon[0].v + self.car_platoon[0].a * dt < 0:
            for i in range(self.count):
                self.car_platoon[i].x -= 1 / 2 * self.car_platoon[i].v * self.car_platoon[i].v / self.car_platoon[i].a
                self.car_platoon[i].v = 0
        else:
            self.car_platoon[0].v += self.car_platoon[0].a * dt
            self.car_platoon[0].x += self.car_platoon[0].v * dt + self.car_platoon[0].a * dt * dt / 2
            for i in range(1, self.count):
                self.car_platoon[i].v = self.car_platoon[0].v
                self.car_platoon[i].x = self.car_platoon[0].x - (i-1) * self.ss

        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.car_platoon[0].x - self.car_platoon[0].x - lead.L
            delta_v = self.car_platoon[0].v - lead.car_platoon[0].v

            alpha = (self.car_platoon[0].s0 + max(0, self.car_platoon[0].T * self.car_platoon[0].v + delta_v * self.car_platoon[0].v / self.car_platoon[0].sqrt_ab)) / delta_x

        self.car_platoon[0].a = self.car_platoon[0].a_max * (1 - (self.car_platoon[0].v / self.car_platoon[0].v_max) ** 4 - alpha ** 2)
        for i in range(1, self.count):
            self.car_platoon[i].a = self.car_platoon[0].a

        if self.stopped:
            self.car_platoon[0].a = -self.car_platoon[0].b_max * self.car_platoon[0].v / self.car_platoon[0].v_max
            for i in range(1, self.count):
                self.car_platoon[i].a = self.car_platoon[0].a
         # for i in range(1, self.count):
        #     self.car_platoon[i].x = self.car_platoon[0].x - i * self.ss
        #     self.car_platoon[i].v = self.car_platoon[0].v
        #     self.car_platoon[i].a = self.car_platoon[0].a

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max
