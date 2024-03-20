# puzzle prompt: https://adventofcode.com/2019/day/7

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *
from itertools import permutations

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 7

    def find_signal(self, code, phases):
        max_thruster_signal = 0

        all_phases = permutations(phases, 5)
        for phases in all_phases:
            next_input = 0
            for setting in phases:
                computer = Computer(code)
                computer.inputs.append(setting)
                computer.inputs.append(next_input)
                try:
                    computer.run()
                except OutputEmmitted:
                    next_input = computer.outputs[-1]
            if next_input > max_thruster_signal:
                max_thruster_signal = next_input
        return max_thruster_signal

    def find_signal_with_feedback(self,code, phase_sequence):
        all_phases = permutations(phase_sequence, 5)

        max_thruster_signal = max(self.run_computers(code, phases) for phases in all_phases)
        
        return max_thruster_signal
    
    def run_computers(self, code, phases):
        computers = []
        for setting in phases:
            computer = Computer(code)
            computer.inputs.append(setting)
            computers.append(computer)

        i = -1
        computers[0].inputs.append(0)
        while True:
            i = (i + 1) % 5
            while not computers[i].done:
                try:
                    computers[i].run()
                except OutputEmmitted:
                    next_input = computers[i].outputs[-1] #wire output to input
                    computers[(i + 1) % 5].inputs.append(next_input)
                    continue
                except InputInterrupted:
                    break

            if all(map(lambda computer: computer.done, computers)):
                break

        return computers[0].inputs[-1]

    def part_1(self):
        start_time = time.time()

        res = self.find_signal(self.input, [0, 1, 2, 3, 4])

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.find_signal_with_feedback(self.input, [5, 6, 7, 8, 9])

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()