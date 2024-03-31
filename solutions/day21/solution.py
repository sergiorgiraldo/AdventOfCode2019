# puzzle prompt: https://adventofcode.com/2019/day/21

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 21

    def program_springdroid(self, code):
        #springdroid jumps 4 steps at a time
        # jump from anywhere if D is safe (AND D J)

        instruction =   "NOT C J\n" + \
                        "NOT A T\n" + \
                        "OR T J\n"  + \
                        "NOT B T\n" + \
                        "OR T J\n"  + \
                        "AND D J\n" + \
                        "WALK\n"
        
        computer = Computer(code)
        computer.inputs.extend([ord(char) for char in instruction])
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                computer.inputs.popleft()
            except OutputEmmitted:
                output = computer.outputs[-1]
                if output > 255:    # it will use an output instruction to indicate the damage
                    return output   # as a single giant integer outside the normal ASCII range

        return 0
    
    def enable_extended_mode(self, code):
        #springdroid jumps 4 steps at a time
        # jump from anywhere if D is safe (AND D J)(same as walk mode)
        # if we jump to D and E is not safe, we can jump if H is safe (H = 8 -> 4 + 4)(AND H T)
        # or go to E if safe (OR E T)
        # if no need to jump, then run

        instruction =   "NOT C J\n" + \
                        "NOT A T\n" + \
                        "OR T J\n"  + \
                        "NOT B T\n" + \
                        "OR T J\n"  + \
                        "AND D J\n" + \
                        "NOT E T\n" + \
                        "AND H T\n" + \
                        "OR E T\n"  + \
                        "AND T J\n" + \
                        "RUN\n"

        computer = Computer(code)
        computer.inputs.extend([ord(char) for char in instruction])
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                computer.inputs.popleft()
            except OutputEmmitted:
                output = computer.outputs[-1]
                if output > 255:    # it will use an output instruction to indicate the damage
                    return output   # as a single giant integer outside the normal ASCII range

        return 0

    def part_1(self):
        start_time = time.time()

        res = self.program_springdroid(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.enable_extended_mode(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()