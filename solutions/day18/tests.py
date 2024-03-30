import unittest

from solution import Solution

solution = Solution()

class Tests(unittest.TestCase):
    def test_part1(self):
        list = [
                "#########",
                "#b.A.@.a#",
                "#########"]
        self.assertEqual(solution.collect_keys(list), 8, "Oops")

        list = [
                "########################",
                "#f.D.E.e.C.b.A.@.a.B.c.#",
                "######################.#",
                "#d.....................#",
                "########################"]
        self.assertEqual(solution.collect_keys(list), 86, "Oops")

        list = [
                "########################",
                "#...............b.C.D.f#",
                "#.######################",
                "#.....@.a.B.c.d.A.e.F.g#",
                "########################"]
        self.assertEqual(solution.collect_keys(list), 132, "Oops")

        list = [
                "#################",
                "#i.G..c...e..H.p#",
                "########.########",
                "#j.A..b...f..D.o#",
                "########@########",
                "#k.E..a...g..B.n#",
                "########.########",
                "#l.F..d...h..C.m#",
                "#################"]
        self.assertEqual(solution.collect_keys(list), 136, "Oops")

        list = [
                "########################",
                "#@..............ac.GI.b#",
                "###d#e#f################",
                "###A#B#C################",
                "###g#h#i################",
                "########################"]
        self.assertEqual(solution.collect_keys(list), 81, "Oops")

    def test_part2(self):
        list = [
                "#######",
                "#a.#Cd#",
                "##...##",
                "##.@.##",
                "##...##",
                "#cB#Ab#",
                "#######"]
        self.assertEqual(solution.collect_keys_with_4robots(list), 8, "Oops")

        list = [
                "#############",
                "#DcBa.#.GhKl#",
                "#.###...#I###",
                "#e#d#.@.#j#k#",
                "###C#...###J#",
                "#fEbA.#.FgHi#",
                "#############"]
        self.assertEqual(solution.collect_keys_with_4robots(list), 32, "Oops")

        list = [
                "#############",
                "#g#f.D#..h#l#",
                "#F###e#E###.#",
                "#dCba...BcIJ#",
                "#####.@.#####",
                "#nK.L...G...#",
                "#M###N#H###.#",
                "#o#m..#i#jk.#",
                "#############"]
        self.assertEqual(solution.collect_keys_with_4robots(list), 72, "Oops")

    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2, "Oops")

if __name__ == "__main__":
    unittest.main()