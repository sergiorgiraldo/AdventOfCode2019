# puzzle prompt: https://adventofcode.com/2019/day/18

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from collections import deque
from functools import lru_cache
import string

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 18
    map = list()

    @lru_cache(maxsize=26) # 26 lowercase letters
    def key_to_bit(self, key):
        return 1 << (ord(key) - 97)

    @lru_cache(maxsize=26) # 26 uppercase letters
    def door_to_bit(self, key):
        return 1 << (ord(key) - 65)

    @lru_cache(maxsize=None)
    def get_reachable_keys(self, position, obtained):
        queue = deque([position])
        dists = {position: 0}
        keys = {}

        while queue:
            row, col = queue.popleft()
            for (x, y) in [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]:
                if x not in range(81) or y not in range(81): # my input is 81x81
                    continue

                tile = self.map[y][x]

                if tile == "#" or (x, y) in dists:
                    continue

                dists[x, y] = dists[row, col] + 1

                if tile in string.ascii_uppercase and not obtained & self.door_to_bit(tile):
                    continue

                if tile in string.ascii_lowercase and not obtained & self.key_to_bit(tile):
                    keys[tile] = dists[x, y], (x, y)
                else:
                    queue.append((x, y))

        return keys

    @lru_cache(maxsize=None)
    def find_shortest_path(self, positions, obtained):
        keys = {
            key: (distance, position, robot)
            for robot, start in enumerate(positions)
            for key, (distance, position) in self.get_reachable_keys(start, obtained).items()
        }

        if not keys:
            return 0

        distances = []

        for key, (distance, position, robot) in keys.items():
            robot_positions = tuple(
                [initial, position][i == robot] for i, initial in enumerate(positions)
            )
            distances.append(
                distance + self.find_shortest_path(robot_positions, obtained | self.key_to_bit(key))
            )

        return min(distances)

    def parse(self, lines):
        map = [[*line] for line in lines]
        self.map = map

    def find_entrance(self):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "@":
                    position = (x, y)
                    break
            else:
                continue
            break
        return position
    
    def collect_keys(self, lines):
        self.parse(lines)

        entrance = self.find_entrance()

        return self.find_shortest_path((entrance,), 0)

    def collect_keys_with_4robots(self, lines):
        self.parse(lines)

        #from the puzzle: update the map, @ is the entrance
        #  ...     @#@
        #  .@.  -> ### 
        #  ...     @#@

        (x,y) = self.find_entrance()

        self.map[y - 1][x - 1]  = "@"
        self.map[y - 1][x]      = "#"
        self.map[y - 1][x + 1]  = "@"
        self.map[y]    [x - 1]  = "#"
        self.map[y]    [x]      = "#"
        self.map[y]    [x + 1]  = "#"
        self.map[y + 1][x - 1]  = "@"
        self.map[y + 1][x]      = "#"
        self.map[y + 1][x + 1]  = "@"

        #reset cache
        self.find_shortest_path.cache_clear()
        self.get_reachable_keys.cache_clear()

        return self.find_shortest_path(((x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)), 0) 
    
    def part_1(self):
        start_time = time.time()

        res = self.collect_keys(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.collect_keys_with_4robots(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()