# puzzle prompt: https://adventofcode.com/2019/day/16

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from collections import deque

class Solution(InputAsStringSolution):
    _year = 2019
    _day = 16

    def test_fft(self, signal, upper_bound=100):
        elements = [int(num) for num in signal]

        for _ in range(upper_bound):
            for pos in range(len(elements)):
                pattern = deque([pattern for pattern in [0, 1, 0, -1] for _ in range(pos+1)])
                pattern.rotate(-1)

                res = 0
                for i in range(len(elements)):
                    res += elements[i] * pattern[0]
                    pattern.rotate(-1)
                elements[pos] = abs(res) % 10

        return "".join(str(num) for num in elements[:8])

# Input signal: 12345678

# 1*1 + 2*0 + 3*-1 + 4*0 + 5*1 + 6*0 + 7*-1 + 8*0 = 4
# 1*0 + 2*1 + 3*1 + 4*0 + 5*0 + 6*-1 + 7*-1 + 8*0 = 8
# 1*0 + 2*0 + 3*1 + 4*1 + 5*1 + 6*0 + 7*0 + 8*0 = 2
# 1*0 + 2*0 + 3*0 + 4*1 + 5*1 + 6*1 + 7*1 + 8*0 = 2
# 1*0 + 2*0 + 3*0 + 4*0 + 5*1 + 6*1 + 7*1 + 8*1 = 6 => (5+1)%10= 6// 5 is from signal, 1 is next calculated
# 1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*1 + 7*1 + 8*1 = 1 => (6+5)%10= 1// 6 is from signal, 5 is next calculated
# 1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*0 + 7*1 + 8*1 = 5 => (7+8)%10= 5// 7 is from signal, 8 is next calculated
# 1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*0 + 7*0 + 8*1 = 8 => 8

# After 1 phase: 48226158

# 4*1 + 8*0 + 2*-1 + 2*0 + 6*1 + 1*0 + 5*-1 + 8*0 = 3
# 4*0 + 8*1 + 2*1 + 2*0 + 6*0 + 1*-1 + 5*-1 + 8*0 = 4
# 4*0 + 8*0 + 2*1 + 2*1 + 6*1 + 1*0 + 5*0 + 8*0 = 0
# 4*0 + 8*0 + 2*0 + 2*1 + 6*1 + 1*1 + 5*1 + 8*0 = 4
# 4*0 + 8*0 + 2*0 + 2*0 + 6*1 + 1*1 + 5*1 + 8*1 = 0 => (4+6)%10= 0// 4 is from signal, 6 is next calculated
# 4*0 + 8*0 + 2*0 + 2*0 + 6*0 + 1*1 + 5*1 + 8*1 = 4 => (1+3)%10= 4// 1 is from signal, 3 is next calculated
# 4*0 + 8*0 + 2*0 + 2*0 + 6*0 + 1*0 + 5*1 + 8*1 = 3 => (5+8)%10= 3// 5 is from signal, 8 is next calculated
# 4*0 + 8*0 + 2*0 + 2*0 + 6*0 + 1*0 + 5*0 + 8*1 = 8 => 8

# with this rule above, i can calculate the last half of the digits in 100 phases
# yeah, it does not work for the beginning of the string but we are only interested in the last 8 digits
# original signal len is 650 and i replicated it 10_000 times (final len is 6_500_000)
# half is the len 3_250_000 and my offset is 5_971_981
# so i can use the formula as I am past half    
    def apply_fft(self, signal):
        offset   = int(signal[:7])
        elements = [int(num) for num in (signal * 10_000)][offset:] #get numbers from offset to end
        
        for _ in range(100):
            for j in range(-2, -len(elements)-1, -1): # in reverse order starting from second-to-last till first
                elements[j] = (elements[j] + elements[j+1]) % 10

        
        return "".join([str(num) for num in elements[:8]])

    def part_1(self):
        start_time = time.time()

        res = self.test_fft(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.apply_fft(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()
