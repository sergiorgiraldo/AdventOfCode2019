# puzzle prompt: https://adventofcode.com/2019/day/4

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
import re

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 4

    LOWERBOUND_RANGE = 359_282 # from puzzle
    UPPERBOUND_RANGE = 820_401 # from puzzle

    def is_ascending(self, password):
        highest = 0
        for chr in password:
            if int(chr) >= highest:
                highest = int(chr)
            else:
                return False
        return True

    #what is not to love about regexes??

    def any_repeated_digits(self, password):
        pattern = r"^.*(\d)\1.*$"
        return re.match(pattern, password)
    
    def exactly_two_repeated_digits(self, password):        
        #          group captured  
        #            1st digit
        #               |              2nd digit
        #               v                 v
        pattern = r"^.*(\d)(?<!(?=\1)\1\1)\1(?!\1)"
        #                    ^                ^     
        #                    |                |
        #             not happen before       |
        #                               not happen after
        #
        # this part is tricky (<!(?=\1)\1\1)
        # i am saying that i go before the group and look ahead
        # there will be already one digit (the group itself, the part (?=\1))
        # and then cannot be 2 more of then after it, the \1\1 part, 
        #which then make three and it is not allowed
        
        return re.match(pattern, password)

    def is_valid_password(self, password, check_repeated_digits):
        if not self.is_ascending(password):
            return False

        if not check_repeated_digits(password):
            return False
            
        return True

    def count_valid_passwords(self, condition):
        valid_passwords = []
        password_range = range(self.LOWERBOUND_RANGE, self.UPPERBOUND_RANGE + 1)

        for password in password_range:
            if self.is_valid_password(str(password), condition):
                valid_passwords.append(password)
                            
        return len(valid_passwords)

    def part_1(self):
        start_time = time.time()

        res = self.count_valid_passwords(self.any_repeated_digits)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.count_valid_passwords(self.exactly_two_repeated_digits)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()