import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    # def test_part1(self):
    #     self.assertEqual(solution.part1(), "", "Oops")

    #def test_part2(self):
    #    self.assertEqual(solution.part2(), "", "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()