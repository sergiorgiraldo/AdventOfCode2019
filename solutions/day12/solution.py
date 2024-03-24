# puzzle prompt: https://adventofcode.com/2019/day/12

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from math import gcd
import re

class Moon:
    def __init__(self, position, velocity=(0, 0, 0)):
        self.position = position
        self.velocity = velocity

    def get_next_velocity(self, moons):
        new_velocity = list(self.velocity)
        for moon in moons:
            for axis in range(3):
                if self.position[axis] < moon.position[axis]:
                    new_velocity[axis] += 1
                elif self.position[axis] > moon.position[axis]:
                    new_velocity[axis] -= 1
        self.velocity = tuple(new_velocity)

    def get_next_position(self):
        self.position = tuple([velocity + position for velocity, position in zip(self.position, self.velocity)])

    def get_total_energy(self):
        potential_energy = sum([abs(element) for element in self.position])
        kinetic_energy = sum([abs(element) for element in self.velocity])

        return potential_energy * kinetic_energy

    def get_position_hash(self):
        return hash(self.position)

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 12

    def parse(self, lines):
        pattern = re.compile(r"<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>")

        m = pattern.match(lines[0])
        io_initial_position = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.io = Moon(io_initial_position)
        
        m = pattern.match(lines[1])
        europa_initial_position = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.europa = Moon(europa_initial_position)
        
        m = pattern.match(lines[2])
        ganymede_initial_position = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.ganymede = Moon(ganymede_initial_position)
        
        m = pattern.match(lines[3])
        callisto_initial_position = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.callisto = Moon(callisto_initial_position)

        self.initial_positions  = [io_initial_position, europa_initial_position, ganymede_initial_position, callisto_initial_position]
        self.jupiter_moons      = [self.io, self.europa, self.ganymede, self.callisto]

        self.surrounding_moons = {
            self.io         : [self.europa, self.ganymede, self.callisto],
            self.europa     : [self.io, self.ganymede, self.callisto],
            self.ganymede   : [self.io, self.europa, self.callisto],
            self.callisto   : [self.io, self.europa, self.ganymede],
    }

    def simulate_moons_motion(self, steps):
        for _ in range(steps):
            for moon in self.jupiter_moons:
                moon.get_next_velocity(self.surrounding_moons[moon])
            for moon in self.jupiter_moons:
                moon.get_next_position()

    def get_total_energy(self, lines, range):
        self.parse(lines)

        self.simulate_moons_motion(range)

        total_system_energy = sum([moon.get_total_energy() for moon in self.jupiter_moons])
        
        return total_system_energy

    def update_positions_and_velocities(self, positions, velocities):
        moons_count = len(positions)

        for moon in range(moons_count):
            for other_moon in range(moons_count):
                if positions[moon] > positions[other_moon]:
                    velocities[moon] -= 1
                elif positions[moon] < positions[other_moon]:
                    velocities[moon] += 1

        for moon in range(moons_count):
            positions[moon] += velocities[moon]

        return positions, velocities

    def get_minimal_period(self, positions, velocities):
        past_positions = set()
        step = 0

        while True:
            self.update_positions_and_velocities(positions, velocities)
            position_hash = hash(tuple(zip(positions, velocities)))
            if position_hash in past_positions:
                return step
            else:
                past_positions.add(position_hash)
                step += 1

    def find_first_repeating_state(self, lines):
        def lcd(a, b):
            return abs(a * b) // gcd(a, b)
        
        self.parse(lines)

        x_positions = [moon[0] for moon in self.initial_positions]
        y_positions = [moon[1] for moon in self.initial_positions]
        z_positions = [moon[2] for moon in self.initial_positions]

        x_velocities = [0] * 4
        y_velocities = [0] * 4
        z_velocities = [0] * 4

        x_period = self.get_minimal_period(x_positions, x_velocities)
        y_period = self.get_minimal_period(y_positions, y_velocities)
        z_period = self.get_minimal_period(z_positions, z_velocities)

        common_period = lcd(lcd(x_period, y_period), z_period)

        return common_period
        
    def part_1(self):
        start_time = time.time()

        res = self.get_total_energy(self.input, 1000)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.find_first_repeating_state(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()