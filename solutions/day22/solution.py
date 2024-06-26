# puzzle prompt: https://adventofcode.com/2019/day/22

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
import re

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 22

    regex_deal_inc = re.compile(r"deal with increment (\d+)")
    regex_deal_new = re.compile(r"deal into new stack")
    regex_cut = re.compile(r"cut (-?\d+)")

    def parse(self, lines):
        self.instructions = [
            [1, int(match.group(1))]
            if (match := self.regex_cut.match(instruction))
            else (
                [2, int(match.group(1))] if (match := self.regex_deal_inc.match(instruction)) else [3, 0]
            )
            for instruction in lines
        ]

    def shuffle_deck_once(self, lines, deck_size, which_card):
        self.parse(lines)

        deck = list(range(deck_size))
        
        for instruction in lines:
            if match := self.regex_deal_new.match(instruction):
                deck = deck[::-1]
            elif match := self.regex_deal_inc.match(instruction):
                step = int(match.group(1))

                new_deck = deck.copy()
                pos = 0
                while deck:
                    new_deck[pos] = deck.pop(0)
                    pos += step
                    pos %= len(new_deck)
                deck = new_deck
            elif match := self.regex_cut.match(instruction):
                value = int(match.group(1))
                deck = deck[value:] + deck[:value]
            else:
                raise Exception(f"Unrecognized instruction: {instruction}")
        return deck.index(which_card)

# deck[n] = increment*n + offset

# new stack:
# - increment = -increment (because we've just reversed the list direction)
# - offset += increment (so that the first number moves and the new second is first)

# cut a:
# when going back, a=-a
# - card a becomes card 0
# - to move a to beginning, offset = increment*a + offset
# - offset += increment * a

# deal inc a:
# - increment *= a
# aka card i -> i*a
# new card 1 = i*a
# where did it start?
# - i
# i = 1/a = a ** (-1)
# modular inverse 
# - increment *= modular inverse(a)
# modular inverse(a) = pow(a,base-2,base)
# base = deck_len = 119315717514047
# inverse(a) = pow(a, 119315717514045, 119315717514047)
# - increment *= pow(a, 119315717514045, 119315717514047)

# after one pass:
# increment *= a
# offset += b*increment at that step
#           some n of previous increment
# odiff = offset after one pass from =0 (summative identity)
# idiff = increment after one pass from =1 (multiplicative identity)
# one pass:
# - offset += increment * odiff
# - increment *= idiff
# increment being multiplied by a number repeatedly - exponentiation
# increment = idiff ** number % 119315717514047 (if we go more than one deck at once we could stay put)
#           = pow(idiff, number, 119315717514047)
# offset depends on increment
# offset = 0
#        = 0 + 1*odiff
#        = 0 + 1*odiff + idiff*odiff
#        = 0 + 1*odiff + idiff*odiff + (idiff**2)*odiff
#        = 0 + odiff*(idiff**0+idiff**1 + ... + idiff**(n-2) + idiff**(n-1))
# geometric series
# https://en.wikipedia.org/wiki/Geometric_series
# a+ar+ar**2+...+ar**n-1
#                       = a * (1-r**n)/(1-r) if r != 1
# r = idiff
# a = odiff
# offset = odiff * (1 - pow(idiff, number, 119315717514047) * pow(1-idiff, 119315717514045, 119315717514047))
# calculate diffs

    def shuffle_huge_deck_many(self, lines):
        deck_size  = 119_315_717_514_047 #120 trillion of cards :)
        which_card = 2020
        times      = 101_741_582_076_661 # shuffle 100 trillion times :)

        self.parse(lines)

        offset, increment = (0, 1)

        for instruction in lines:
            if match := self.regex_deal_new.match(instruction):
                increment *= -1
                increment %= deck_size
                offset += increment
                offset %= deck_size
            elif match := self.regex_deal_inc.match(instruction):
                increment *= pow(int(match.group(1)), deck_size - 2, deck_size)
                increment %= deck_size
            elif match := self.regex_cut.match(instruction):
                offset += increment * int(match.group(1))
                offset %= deck_size

        final_increment = pow(increment, times, deck_size)
        final_offset = offset * (
            (1 - pow(increment, times, deck_size)) * pow(1 - increment, deck_size - 2, deck_size)
        )

        return (which_card * final_increment + final_offset) % deck_size

    def part_1(self):
        start_time = time.time()

        res = self.shuffle_deck_once(self.input, 10_007, 2_019)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.shuffle_huge_deck_many(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()