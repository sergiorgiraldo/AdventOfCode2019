# puzzle prompt: https://adventofcode.com/2019/day/24

import time
import sys
sys.path.insert(0,"..")

from base.advent import *

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 24

    def parse_grid(self, lines):
        grid = []
        
        grid = [
            [int(i == "#") for i in j]
            for j in lines
        ]

        return grid
    
    def parse_layers(self, lines):
        layers = []

        layers = [
            [[0 for i in range(5)] for i in range(5)],
            [
                [int(i == "#") for i in j]
                for j in lines
            ],
            [[0 for i in range(5)] for i in range(5)],
        ]

        return layers
    
    def get_surrounding_grid(self, grid, x, y):
            surrounding = []

            #grid is 5x5
            if y > 0:
                surrounding.append(grid[y - 1][x])
            if y < 4:
                surrounding.append(grid[y + 1][x])
            if x > 0:
                surrounding.append(grid[y][x - 1])
            if x < 4:
                surrounding.append(grid[y][x + 1])

            return surrounding    

    def get_biodiversity(self, lines):
        grid = self.parse_grid(lines)

        previous_grids = set()

        while True:
            rating = 0

            for y in range(5):
                for x in range(5):
                    rating += grid[y][x] * 2 ** (y * 5 + x)

            if rating in previous_grids:
                return rating

            previous_grids.add(rating)
            
            next_grid = [
                [
                    (1 if sum(self.get_surrounding_grid(grid, x, y)) == 1 else 0)
                    if grid[y][x] == 1
                    else (1 if sum(self.get_surrounding_grid(grid, x, y)) in {1, 2} else 0)
                    for x in range(5)
                ]
                for y in range(5)
            ]

            grid = next_grid
                    
    def get_surrounding_layers(self, layers, x, y, layer):
        surrounding = []

        #grid is 5x5
        if y > 0:
            surrounding.append(layers[layer][y - 1][x])
        else:
            if layer != 0:
                surrounding.append(layers[layer - 1][1][2])

        if y < 4:
            surrounding.append(layers[layer][y + 1][x])
        else:
            if layer != 0:
                surrounding.append(layers[layer - 1][3][2])

        if x > 0:
            surrounding.append(layers[layer][y][x - 1])
        else:
            if layer != 0:
                surrounding.append(layers[layer - 1][2][1])

        if x < 4:
            surrounding.append(layers[layer][y][x + 1])
        else:
            if layer != 0:
                surrounding.append(layers[layer - 1][2][3])

        if x == y == 2:
            return []

        if layer != len(layers) - 1:
            if (x, y) == (2, 1):
                surrounding.extend(layers[layer + 1][0])

            if (x, y) == (2, 3):
                surrounding.extend(layers[layer + 1][-1])

            if (x, y) == (1, 2):
                surrounding.extend(i[0] for i in layers[layer + 1])

            if (x, y) == (3, 2):
                surrounding.extend(i[-1] for i in layers[layer + 1])

        return surrounding

    def get_bugs_in_folded_space(self, lines):
        layers = self.parse_layers(lines)

        for i in range(200): #from puzzle, 200 minutes
            layers_len = len(layers)
            next_layers = [[[0 for _ in range(5)] for _ in range(5)]]

            for i in range(layers_len):
                layer = layers[i]

                next_grid = [
                    [
                        (1 if sum(self.get_surrounding_layers(layers, x, y, i)) == 1 else 0)
                        if layer[y][x] == 1
                        else (1 if sum(self.get_surrounding_layers(layers,x, y, i)) in {1, 2} else 0)
                        for x in range(5)
                    ]
                    for y in range(5)
                ]

                next_layers.append(next_grid)

            next_layers.append([[0 for _ in range(5)] for _ in range(5)])
            layers = next_layers

        return sum(sum(sum(row) for row in layer) for layer in layers)

    def part_1(self):
        start_time = time.time()

        res = self.get_biodiversity(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.get_bugs_in_folded_space(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()