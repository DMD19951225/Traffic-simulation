from .car_platoon import Car_platoon
from numpy.random import randint

class VehicleGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        """Set default configuration"""
        self.car_platoon_rate = 20
        self.num = -1
        self.car_platoons = [
            (1, {})
        ]
        self.last_added_time = 0

    def init_properties(self):
        self.upcoming_car_platoon = self.generate_car_platoon()

    def generate_car_platoon(self):
        """Returns a random vehicle from self.vehicles with random proportions"""
        total = sum(pair[0] for pair in self.car_platoons)
        r = randint(1, total+1)
        for (weight, config) in self.car_platoons:
            r -= weight
            if r <= 0:
                self.num += 1
                return Car_platoon(self.num, config)

    def update(self):
        """Add vehicles"""
        if self.sim.t - self.last_added_time >= 60 / self.car_platoon_rate:
            # If time elasped after last added vehicle is
            # greater than vehicle_period; generate a vehicle
            road = self.sim.roads[self.upcoming_car_platoon.path[0]]
            if len(road.car_platoons) == 0\
               or road.car_platoons[-1].x > self.upcoming_car_platoon.car_platoon[0].s0 + self.upcoming_car_platoon.l:
                # If there is space for the generated vehicle; add it
                self.upcoming_car_platoon.time_added = self.sim.t
                for i in range(self.upcoming_car_platoon.count):
                    road.car_platoons.append(self.upcoming_car_platoon.car_platoon[i])
                # Reset last_added_time and upcoming_vehicle
                self.last_added_time = self.sim.t
            self.upcoming_car_platoon = self.generate_car_platoon()

