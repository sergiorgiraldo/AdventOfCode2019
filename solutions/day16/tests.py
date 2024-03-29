import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        signal = "80871224585914546619083218645595"
        self.assertEqual(solution.test_fft(signal), "24176176", "Oops")

        signal = "19617804207202209144916044189917"
        self.assertEqual(solution.test_fft(signal), "73745418", "Oops")
        
        signal = "69317163492948606335995924319873"
        self.assertEqual(solution.test_fft(signal), "52432133", "Oops")

    def test_part2(self):
        signal = "03036732577212944063491565474664"
        self.assertEqual(solution.apply_fft(signal), "84462026", "Oops")

        signal = "02935109699940807407585447034323"
        self.assertEqual(solution.apply_fft(signal), "78725270", "Oops")
        
        signal = "03081770884921959731165446850517"
        self.assertEqual(solution.apply_fft(signal), "53553731", "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()