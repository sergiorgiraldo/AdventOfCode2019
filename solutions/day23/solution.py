# puzzle prompt: https://adventofcode.com/2019/day/23

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.networkcomputer import *

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 23

    def build_network(self, code):
        network, network_queue = [], []
        
        for network_address in range(50):
            computer = Computer(code)
            computer.inputs.append(network_address)
            network.append(computer)
            network_queue.append([])
    
        return network, network_queue

    def boot_network(self, code):
        network, network_queue = self.build_network(code)

        while True:
            for network_address in range(50):
                output = self.run_network_computer(network[network_address], network_address)
                if (output != None):
                    network_queue[network_address].append(output)
                    if len(network_queue[network_address]) == 3:
                        if network_queue[network_address][0] == 255:
                            return network_queue[network_address]
                        
                        network[network_queue[network_address][0]].inputs.extend(network_queue[network_address][1:])
                        network_queue[network_address] = []

    #network computers dont run until end, they just emit one value and die
    def run_network_computer(self, computer, index):
        try:
            computer.run()
        except InputInterrupted:
            computer.inputs.append(-1)
        except OutputEmmitted:
            output = computer.outputs[-1]
            return output
        return None

    def is_idle(self, network, network_queue):
        for network_address in range(50):
            if len(network_queue[network_address]) or not network[network_address].waiting:
                return False
        return True

    def get_NAT_value(self, code):
        network, network_queue = self.build_network(code)

        nat, last_nat = [], None

        while True:
            for network_address in range(50):
                output = self.run_network_computer(network[network_address], network_address)
                if (output != None):
                    network_queue[network_address].append(output)
                    if len(network_queue[network_address]) == 3:
                        if network_queue[network_address][0] == 255:
                            nat = network_queue[network_address][1:]
                        else:
                            network[network_queue[network_address][0]].inputs.extend(network_queue[network_address][1:])
                        network_queue[network_address] = []

            if self.is_idle(network, network_queue) and len(nat):
                if nat[1] == last_nat:
                    return last_nat
                network[0].inputs.extend(nat)
                last_nat, nat = nat[1], []

    def part_1(self):
        start_time = time.time()

        res = self.boot_network(self.input)[2]

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.get_NAT_value(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()