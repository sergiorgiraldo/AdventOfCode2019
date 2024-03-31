# puzzle prompt: https://adventofcode.com/2019/day/20

import time
import sys
sys.path.insert(0,"..")

from base.advent import *

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 20

    def part_1(self):
        start_time = time.time()

        arr = self.input
        res = ""

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        arr = self.input
        res = ""

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    # solution.part_2()