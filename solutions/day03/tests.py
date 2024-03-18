import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        list = [
            ["R8","U5","L5","D3"],
            ["U7","R6","D4","L4"]
        ]
        self.assertEqual(solution.get_closest_intersection(list), 6, "Oops")

        list = [
            ["R75","D30","R83","U83","L12","D49","R71","U7","L72"],
            ["U62","R66","U55","R34","D71","R55","D58","R83"]
        ]
        self.assertEqual(solution.get_closest_intersection(list), 159, "Oops")

        list = [
            ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"],
            ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
        ]
        self.assertEqual(solution.get_closest_intersection(list), 135, "Oops")

    def test_part2(self):
        list = [
            ["R8","U5","L5","D3"],
            ["U7","R6","D4","L4"]
        ]
        self.assertEqual(solution.minimize_steps_taken(list), 30, "Oops")

        list = [
            ["R75","D30","R83","U83","L12","D49","R71","U7","L72"],
            ["U62","R66","U55","R34","D71","R55","D58","R83"]
        ]
        self.assertEqual(solution.minimize_steps_taken(list), 610, "Oops")

        list = [
            ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"],
            ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
        ]
        self.assertEqual(solution.minimize_steps_taken(list), 410, "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()