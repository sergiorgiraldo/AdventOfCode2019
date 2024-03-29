# puzzle prompt: https://adventofcode.com/2019/day/8

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from itertools import zip_longest
from collections import defaultdict

class Solution(InputAsStringSolution):
    _year = 2019
    _day = 8

    #from puzzle input, this is the image size
    width   = 25
    height  = 6
    
    def verify_image_is_good(self, data):
        
        def group(iterable, image_size):
            return zip_longest(*[iter(iterable)] * image_size, fillvalue="0")
        
        lowest, checksum = float("inf"), 0

        for layer in group(data, self.width * self.height):
            if layer.count("0") < lowest:
                lowest = layer.count("0")
                checksum = layer.count("1") * layer.count("2")

        return checksum

    def compute_layer_depth(self, data):
        raw = [int(pixel) for pixel in data]
        
        size = self.width * self.height

        layers = defaultdict(list)

        layer = -1

        for i in range(len(raw)):
            if not i % size:
                layer += 1
            layers[layer].append(raw[i])
        print (layers[0])
        print ()
        print (layers[1])

        return layers

    def print_image(self, data):
        layers = self.compute_layer_depth(data)

        for y in range(self.height):
            for x in range(self.width):
                pos = x + y * self.width

                for layer in range(self.width * self.height):
                    if layers[layer][pos] == 2:   #transparent
                        continue
                    if layers[layer][pos] == 1:   #black
                        print("#", end="")
                    else:                         #white
                        print(" ", end="")    
                    break    
            print()

    def part_1(self):
        start_time = time.time()

        res = self.verify_image_is_good(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        self.print_image(self.input)

        #### #    ###    ## #### 
           # #    #  #    # #    
          #  #    ###     # ###  
         #   #    #  #    # #    
        #    #    #  # #  # #    
        #### #### ###   ##  #  

        res = "ZLBJF"

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()

