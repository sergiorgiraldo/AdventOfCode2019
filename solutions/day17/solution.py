# puzzle prompt: https://adventofcode.com/2019/day/17

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *
from functools import reduce

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 17

    def build_image(self, code):
        computer = Computer(code)
        image = ""
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                break
            except OutputEmmitted:
                ch = computer.outputs[-1]
                image += chr(ch)
        #print(image) # needed for part 2
        return image


    def get_intersections(self, code):
        image = self.build_image(code)
        grid = [line for line in image.strip().split(chr(10))]
        height, width = len(grid), len(grid[0])

        #    -1  X  +1
        # -1     # 
        #  Y  #  o  #
        # +1     #
        #  
        
        intersections = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if grid[y][x] == "#" and grid[y - 1][x] == "#" and grid[y + 1][x] == "#" and grid[y][x - 1] == "#" and grid[y][x + 1] == "#":
                    intersections.append((x, y))

        return reduce(lambda acc, curr: acc + curr[0] * curr[1], intersections, 0)

    def collect_dust(self, code):
        code[0] = 2
        computer = Computer(code)

        # solved the map by hand, see `map WALKED.txt`
        # R12 L10 L10 L6 L12 R12 L4 R12 L10 L10 L6 L12 R12 L4 L12 R12 L6 L6 L12 R12 L4 L12 R12 L6 R12 L10 L10 L12 R12 L6 L12 R12 L6
        main_routine   = "A,B,A,B,C,B,C,A,C,C\n"
        a_function     = "R,12,L,10,L,10\n"
        b_function     = "L,6,L,12,R,12,L,4\n"
        c_function     = "L,12,R,12,L,6\n"
        movement_rules = main_routine + a_function + b_function + c_function + "n\n"
        
        inputs = [ord(ch) for ch in movement_rules]

        i = 0
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                computer.inputs.append(inputs[i])
                i += 1
            except OutputEmmitted:
                dust = computer.outputs[-1]
                if dust > 10_000: #arbitrary, cleaning robot will report the amount 
                    return dust   #as a large, non-ASCII value, in a single output instruction

    def part_1(self):
        start_time = time.time()

        res = self.get_intersections(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.collect_dust(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == "__main__":
    solution = Solution()

    solution.part_1()
    
    solution.part_2()