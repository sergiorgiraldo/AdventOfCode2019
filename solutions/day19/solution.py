# puzzle prompt: https://adventofcode.com/2019/day/19

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 19

    def run_program(self, code, input):
        computer = Computer(code)
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                computer.inputs.append(input[0])
                computer.inputs.append(input[1])
            except OutputEmmitted:
                return computer.outputs[-1]
        
        return 0

    def get_beam_shape(self, code):
        affected = 0
        for y in range(50):
            for x in range(50):
                affected += self.run_program(code, [x,y])

        return affected

    # i made it simple, get each point from the boundaries (line 100 & column 100) 
    # and check if I can get a reading from it
    def get_closest_to_emmitter(self, code):
        x = y = 0
        while self.run_program(code, [x + 99, y]) == 0:
            y += 1
            while self.run_program(code, [x, y + 99]) == 0:
                x += 1

        return x * 10000 + y

    def part_1(self):
        start_time = time.time()

        res = self.get_beam_shape(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.get_closest_to_emmitter(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()