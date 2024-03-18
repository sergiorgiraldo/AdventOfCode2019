# puzzle prompt: https://adventofcode.com/2019/day/2

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *
from copy import copy

# i've read several puzzles in 2019 need an intepreter for IntCode
# instead coding the functions here, i made a class that I can extend further

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 2

    def run_program(self, code_, restore_gravity=False, register_to_check=0):
        code = copy(code_) 
         
        if restore_gravity:
            code[1] = 12
            code[2] = 2

        computer = Computer(code)

        computer.run()

        return computer.code[register_to_check]

    def run_until_magic_number(self, code_):
        original = code_

        try:
            for noun in range(100):
                for verb in range(100):
                    code = copy(original)       
                    code[1] = noun
                    code[2] = verb

                    computer = Computer(code)
                    computer.run()

                    if computer.code[0] == 19_690_720: 
                        raise StopIteration
        except:
            pass
            
        return (100 * noun) + verb         

    def part_1(self):
        start_time = time.time()

        res = self.run_program(self.input, restore_gravity=True)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.run_until_magic_number(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    solution.part_2()
    
