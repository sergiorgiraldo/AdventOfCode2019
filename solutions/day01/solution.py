# puzzle prompt: https://adventofcode.com/2019/day/1

import time
import sys
sys.path.insert(0,"..")

from base.advent import *

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 1

    def get_fuel_requirement(self, lines):
        fuel_requirement = 0
        
        for line in lines:
            mass = int(line)
            computed_fuel = int(mass / 3) - 2
            fuel_requirement += max(0, computed_fuel)
        
        return fuel_requirement

    def get_fuel_requirement_with_mass(self, lines):
        fuel_requirement = 0
        
        for line in lines:
            mass = int(line)
            fuel_requirement += self.get_total_fuel_requirement(mass)
        
        return fuel_requirement

    def get_total_fuel_requirement(self, mass):
        total_fuel_required = self.get_fuel_requirement([mass])
        if total_fuel_required == 0:
            return 0
        else:
            additional_fuel_for_fuel = self.get_total_fuel_requirement(total_fuel_required)
            return total_fuel_required + additional_fuel_for_fuel

    def part_1(self):
        start_time = time.time()

        res = self.get_fuel_requirement(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.get_fuel_requirement_with_mass(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()