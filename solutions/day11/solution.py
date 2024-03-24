# puzzle prompt: https://adventofcode.com/2019/day/11

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *
from collections import defaultdict

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 11

    def build_robot(self, code, input_value):
        grid = defaultdict(int)

        grid[0] = input_value
        position = 0    #complex number to track position, real part is x direction, imag part is y
        direction = -1j 
        read_color = True

        computer = Computer(code)
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                # send in the color at the current spot
                computer.inputs.append(grid[position])
            except OutputEmmitted:
                value = computer.outputs[-1] # get the color to paint
                if read_color:
                    grid[position] = value   # and paint
                else:
                    direction = direction * -1j if value == 0 else direction * 1j # change direction
                    position += direction                                         # move forward 1 step
                read_color = not read_color

        return len(grid), grid

    def part_1(self):
        start_time = time.time()

        res = self.build_robot(self.input, 0)[0]

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        grid = self.build_robot(self.input, 1)[1]

        for j in range(6):
            line = ""
            for i in range(50):
                if complex(i,j) in grid:
                    line += "#" if grid[complex(i,j)] == 1 else " "
                else:
                    line += " "
            print(line)

        end_time = time.time()

          ##   ##   ##  #    ###   ##    ## ####          
        #  # #  # #  # #    #  # #  #    # #             
        #  # #    #  # #    #  # #       # ###           
        #### # ## #### #    ###  # ##    # #             
        #  # #  # #  # #    # #  #  # #  # #             
        #  #  ### #  # #### #  #  ###  ##  ####  

        self.solve("2", "AGALRGJE", (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()