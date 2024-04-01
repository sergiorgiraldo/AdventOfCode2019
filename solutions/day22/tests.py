import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        list = [
                "deal with increment 7",
                "deal into new stack",
                "deal into new stack"]
        self.assertEqual(solution.shuffle_deck_once(list, 10, 0), 0, "Oops")

        list = [
                "cut 6",
                "deal with increment 7",
                "deal into new stack"]
        self.assertEqual(solution.shuffle_deck_once(list, 10, 0), 1, "Oops")

        list = [
                "deal with increment 7",
                "deal with increment 9",
                "cut -2"]
        self.assertEqual(solution.shuffle_deck_once(list, 10, 0), 2, "Oops")

        list = [
                "deal into new stack",
                "cut -2",
                "deal with increment 7",
                "cut 8",
                "cut -4",
                "deal with increment 7",
                "cut 3",
                "deal with increment 9",
                "deal with increment 3",
                "cut -1"]
        self.assertEqual(solution.shuffle_deck_once(list, 10, 0), 7, "Oops")

    #def test_part2(self):
    #    self.assertEqual(solution.part2(), "", "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()