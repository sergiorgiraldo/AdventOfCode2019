# puzzle prompt: https://adventofcode.com/2019/day/10

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from math import atan2, degrees
from collections import defaultdict

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 10

    def parse(self, lines):
        asteroids_map = []

        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == '#':
                    asteroids_map.append((x, y))
        
        return asteroids_map
    
    #If we are looking at two asteroids by same angle then they are on the same line. 
    #Thus number of unique angles is the number of visible asteroids for a given asteroid
    #A,B,C are on the same line, so A cant see C, A can see B and D, 2 different angles   
    #     |         C
    #     |      B  D
    #     |   A
    #     _______________   
    #     |  
    #

    def angle_between(self, a1, a2):
        x_diff = a2[0] - a1[0]
        y_diff = a2[1] - a1[1]

        return degrees(atan2(y_diff, x_diff))

    def get_best_location(self, lines):
        asteroids_map = self.parse(lines)

        max_seen = 0
        best_asteroid = (0, 0)

        for a1 in asteroids_map:
            seen = set(self.angle_between(a1, a2) for a2 in asteroids_map if a1 != a2)
            if len(seen) > max_seen:
                max_seen = len(seen)
                best_asteroid = a1

        return max_seen, best_asteroid

    def get_manhattan_distance(self, a1, a2):
        return abs(a1[0] - a2[0]) + abs(a1[1] - a2[1]) 

    def vaporize(self, lines):
        angles = defaultdict(lambda: [])
        
        asteroids_map = self.parse(lines)
        
        station = self.get_best_location(lines)[1]

        # get all asteroids - grouped by angle we see them at, need to account for the fact
        # each time rotate clockwise by 90 degrees (the -90).
        # i then add 360 to make sure it is always 0<x<360 and mod by 360
        # 30  -> -60 -> 300 -> 300
        # 110 ->  20 -> 380 -> 20
        for asteroid in asteroids_map:
            if asteroid != station:
                angles[(self.angle_between(asteroid, station) - 90 + 360) % 360].append(asteroid)

        # sort the asteroids for each angle based on how far they are from the station
        for angle in angles:
            angles[angle] = list(sorted(angles[angle], key=lambda a: self.get_manhattan_distance(a, station)))

        # get the possible angles we rotate between
        possible_angles = list(sorted(angles.keys()))
        num_possible = len(possible_angles)

        angle_index = 0
        gone = 0
        while gone < 200: #magic number from the puzzle
            # find the next angle with asteroids left
            while not angles[possible_angles[angle_index]]:
                angle_index = (angle_index + 1) % num_possible

            # vaporize the closest asteroid
            vaporized = angles[possible_angles[angle_index]].pop(0)

            # move to the next angle
            angle_index = (angle_index + 1) % num_possible

            gone += 1

        return vaporized[0] * 100 + vaporized[1]

    def part_1(self):
        start_time = time.time()

        res = self.get_best_location(self.input)[0]

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.vaporize(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()