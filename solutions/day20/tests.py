import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        list = [
                "         A           ",
                "         A           ",
                "  #######.#########  ",
                "  #######.........#  ",
                "  #######.#######.#  ",
                "  #######.#######.#  ",
                "  #######.#######.#  ",
                "  #####  B    ###.#  ",
                "BC...##  C    ###.#  ",
                "  ##.##       ###.#  ",
                "  ##...DE  F  ###.#  ",
                "  #####    G  ###.#  ",
                "  #########.#####.#  ",
                "DE..#######...###.#  ",
                "  #.#########.###.#  ",
                "FG..#########.....#  ",
                "  ###########.#####  ",
                "             Z       ",
                "             Z       "
        ]
        self.assertEqual(solution.escape_maze(list), 23, "Oops")

        list = [
                "                   A               ",
                "                   A               ",
                "  #################.#############  ",
                "  #.#...#...................#.#.#  ",
                "  #.#.#.###.###.###.#########.#.#  ",
                "  #.#.#.......#...#.....#.#.#...#  ",
                "  #.#########.###.#####.#.#.###.#  ",
                "  #.............#.#.....#.......#  ",
                "  ###.###########.###.#####.#.#.#  ",
                "  #.....#        A   C    #.#.#.#  ",
                "  #######        S   P    #####.#  ",
                "  #.#...#                 #......VT",
                "  #.#.#.#                 #.#####  ",
                "  #...#.#               YN....#.#  ",
                "  #.###.#                 #####.#  ",
                "DI....#.#                 #.....#  ",
                "  #####.#                 #.###.#  ",
                "ZZ......#               QG....#..AS",
                "  ###.###                 #######  ",
                "JO..#.#.#                 #.....#  ",
                "  #.#.#.#                 ###.#.#  ",
                "  #...#..DI             BU....#..LF",
                "  #####.#                 #.#####  ",
                "YN......#               VT..#....QG",
                "  #.###.#                 #.###.#  ",
                "  #.#...#                 #.....#  ",
                "  ###.###    J L     J    #.#.###  ",
                "  #.....#    O F     P    #.#...#  ",
                "  #.###.#####.#.#####.#####.###.#  ",
                "  #...#.#.#...#.....#.....#.#...#  ",
                "  #.#####.###.###.#.#.#########.#  ",
                "  #...#.#.....#...#.#.#.#.....#.#  ",
                "  #.###.#####.###.###.#.#.#######  ",
                "  #.#.........#...#.............#  ",
                "  #########.###.###.#############  ",
                "           B   J   C               ",
                "           U   P   P               "]
        self.assertEqual(solution.escape_maze(list), 58, "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()