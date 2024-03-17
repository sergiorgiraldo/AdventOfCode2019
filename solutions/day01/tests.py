import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solution.get_fuel_requirement([12]), 2, "Oops")
        self.assertEqual(solution.get_fuel_requirement([14]), 2, "Oops")
        self.assertEqual(solution.get_fuel_requirement([1_969]), 654, "Oops")
        self.assertEqual(solution.get_fuel_requirement([100_756]), 33_583, "Oops")

    def test_part2(self):
        self.assertEqual(solution.get_fuel_requirement_with_mass([14]), 2, "Oops")
        self.assertEqual(solution.get_fuel_requirement_with_mass([1_969]), 966, "Oops")
        self.assertEqual(solution.get_fuel_requirement_with_mass([100_756]), 50_346, "Oops")
    
    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()