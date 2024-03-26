# puzzle prompt: https://adventofcode.com/2019/day/13

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 13

    def play_the_game(self, code):
        tiles = {}

        computer = Computer(code)
        output_values = []
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                computer.inputs.append(0)
            except OutputEmmitted:
                output_values.append(computer.outputs[-1])
                # wait for 3 consecutive outputs
                if len(output_values) == 3:
                    x, y, tile = output_values
                    tiles[(x, y)] = tile
                    output_values.clear()

        self.render(tiles)

        blocks = sum(1 for i in range(30) for j in range(100) if (j, i) in tiles and tiles[(j, i)] == 2)

        return blocks
    
    def render(self, tiles):
        for i in range(30):
            game_line = ""
            for j in range(100):
                if (j, i) in tiles:
                    tile = tiles[(j, i)]
                    if tile == 0:
                        game_line += "  "
                    elif tile == 1:
                        game_line += "##"
                    elif tile == 2:
                        game_line += "██"
                    elif tile == 3:
                        game_line += "=="
                    elif tile == 4:
                        game_line += "@@"
            print(game_line)

    def beat_the_game(self, code):
        #outputs
        PADDLE = 3
        BALL   = 4

        #joystick moves
        LEFT    = -1
        NEUTRAL = 0
        RIGHT   = 1

        computer = Computer(code)

        # enter 2 coins
        computer.code[0] = 2

        # set up x positions for ball and paddle
        ball_x = 0
        paddle_x = 0

        # set up initial score
        score = 0

        output_values = []
        while not computer.done:
            try:
                computer.run()
            except InputInterrupted:
                if ball_x < paddle_x:
                    computer.inputs.append(LEFT)
                elif ball_x > paddle_x:
                    computer.inputs.append(RIGHT)
                else:
                    computer.inputs.append(NEUTRAL)
            except OutputEmmitted:
                output_values.append(computer.outputs[-1])
                if len(output_values) == 3:
                    x, y, tile = output_values
                    if x == -1 and y == 0:
                        score = tile
                    if tile == BALL:
                        ball_x = x
                    elif tile == PADDLE:
                        paddle_x = x
                    output_values.clear()

        return score

    def part_1(self):
        start_time = time.time()

        #see day13.png for the output

        res = self.play_the_game(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.beat_the_game(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()