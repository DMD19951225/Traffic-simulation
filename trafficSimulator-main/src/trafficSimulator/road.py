from scipy.spatial import distance
from collections import deque

class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.car_platoons = deque()

        self.init_properties()

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def update(self, dt):
        n = len(self.car_platoons)

        if n > 0:
            # Update first car_platoon
            self.car_platoons[0].update(None, dt)
            # Update other car_platoons
            for i in range(1, n):
                lead = self.car_platoons[i-1]
                self.car_platoons[i].update(lead, dt)
                if self.car_platoons[i].platoon_id == self.car_platoons[i-1].platoon_id:
                    self.car_platoons[i].v = self.car_platoons[i-1].v
                    self.car_platoons[i].a = self.car_platoons[i-1].a

             # Check for traffic signal
            if self.traffic_signal_state:
                # If traffic signal is green or doesn't exist
                # Then let vehicles pass
                self.car_platoons[0].unstop()
                for car_platoon in self.car_platoons:
                    car_platoon.unslow()
            else:
                # If traffic signal is red
                for i in range(n):
                    if self.car_platoons[0].x >= self.length - self.traffic_signal.slow_distance:
                        # Slow vehicles in slowing zone
                        self.car_platoons[0].slow(self.traffic_signal.slow_factor * self.car_platoons[0]._v_max)
                        if self.car_platoons[i].platoon_id == self.car_platoons[i-1].platoon_id:
                            self.car_platoons[i].v_max = self.car_platoons[i-1].v_max
                    if self.car_platoons[0].x >= self.length - self.traffic_signal.stop_distance and\
                       self.car_platoons[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                        # Stop vehicles in the stop zone
                        self.car_platoons[0].unslow()
