# puzzle prompt: https://adventofcode.com/2019/day/5

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 5

    def run_program(self, code, input_value):
        computer = Computer(code)
        
        computer.inputs.append(input_value)

        while True:
            try:
                computer.run()
            except OutputEmmitted:
                output = computer.outputs[-1]
                if output != 0:
                    return output

    def part_1(self):
        start_time = time.time()

        res = self.run_program(self.input, 1)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.run_program(self.input, 5)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()