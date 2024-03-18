import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        code = [1,9,10,3,2,3,11,0,99,30,40,50]
        self.assertEqual(solution.run_program(code,False,0), 3_500, "Oops")

        code = [1,0,0,0,99]
        self.assertEqual(solution.run_program(code,False,0), 2, "Oops")

        code = [2,3,0,3,99]
        self.assertEqual(solution.run_program(code,False,3), 6, "Oops")

        code = [2,4,4,5,99,0]
        self.assertEqual(solution.run_program(code,False,5), 9_801, "Oops")

        code = [1,1,1,4,99,5,6,0,99]
        self.assertEqual(solution.run_program(code,False,0), 30, "Oops")

    #def test_part2(self):
    #    self.assertEqual(solution.part2(), "", "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()