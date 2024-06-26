# puzzle prompt: https://adventofcode.com/2019/day/15

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer import *
import pygame

NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
WALL, WALKABLE, DROID, ORIGIN, PATH, OXYGEN, BACKGROUND = 0, 1, 2, 3, 4, 5, 6
WALL_STATUS, EMPTY_STATUS, OXYGEN_STATUS = 0, 1, 2
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)
OFFSETS = tuple(zip(DX, DY))
TILE_SIZE = 10

class RepairSystem:
    def __init__(self, code):
        self.origin = (25, 25) #arbitrary, i dont have any knowledge of the map
        self.position = self.origin
        self.found_oxygen = False
        self.world = {self.position: WALKABLE}
        self.path = [self.position]
        self.walkable = set()
        self.droid = Computer(code)
        self.dir_i = 0
        self.fully_explored = False
        self.oxygen_pos = set()
        self.check_neighbors = set()
        self.oxygen_minutes = 0

        # set up the repair board
        pygame.init()
        self.display = pygame.display.set_mode((500, 500))
        self.colors = {
            WALL:       pygame.Color("grey10"),
            WALKABLE:   pygame.Color("white"),
            DROID:      pygame.Color("yellow"),
            ORIGIN:     pygame.Color("red"),
            PATH:       pygame.Color("lightgreen"),
            OXYGEN:     pygame.Color("deepskyblue"),
            BACKGROUND: pygame.Color("black")
        }
        self.display.fill(self.colors[BACKGROUND])

    def move_droid(self, to_fill = False):
        running = True

        while running:
            running = self.read_events()

            if self.fully_explored:
                running = self.fill_oxygen() if to_fill else False
            else:
                self.explore_new_paths()

            self.draw_screen()

        pygame.quit()

    def draw_screen(self):
        for pos, tile in self.world.items():
            pygame.draw.rect(self.display, self.colors[tile], (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        for pos in self.path:
            pygame.draw.rect(self.display, self.colors[PATH], (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        pygame.draw.rect(self.display, self.colors[DROID], (self.position[0] * TILE_SIZE, self.position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        for pos in self.oxygen_pos:
            pygame.draw.rect(self.display, self.colors[OXYGEN], (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        pygame.draw.rect(self.display, self.colors[ORIGIN], (self.origin[0] * TILE_SIZE, self.origin[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        pygame.display.flip()

    def explore_new_paths(self):
        new_position = (self.position[0] + DX[self.dir_i], self.position[1] + DY[self.dir_i])
        if new_position == self.origin:
            self.fully_explored = True
            self.walkable = {k for k, v in self.world.items() if v == WALKABLE}

        status = self.get_status(self.droid, DIRECTIONS[self.dir_i])

        if status == WALL_STATUS:
            self.dir_i = (self.dir_i + 1) % 4
            self.world[new_position] = WALL
        elif status == EMPTY_STATUS or status == OXYGEN_STATUS:
            if new_position in self.world:
                if not self.found_oxygen:
                    self.path.pop()
            else:
                self.world[new_position] = WALKABLE
                if status == OXYGEN_STATUS:
                    self.found_oxygen = True
                    self.oxygen_pos.add(new_position)
                    self.check_neighbors.add(new_position)
                if not self.found_oxygen:
                    self.path.append(new_position)
            self.dir_i = (self.dir_i - 1) % 4
            self.position = new_position

    def fill_oxygen(self):
        self.oxygen_minutes += 1
        new_check_neighbors = set()
        while self.check_neighbors:
            pos = self.check_neighbors.pop()
            for o in OFFSETS:
                neighbor = (pos[0] + o[0], pos[1] + o[1])
                if self.world.get(neighbor) == WALKABLE and neighbor not in self.oxygen_pos and neighbor not in new_check_neighbors:
                    self.oxygen_pos.add(neighbor)
                    new_check_neighbors.add(neighbor)
        self.check_neighbors = new_check_neighbors
        if self.oxygen_pos == self.walkable:
            return False
        return True

    def read_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def get_status(self, droid, command):
        try:
            droid.run()
        except InputInterrupted:
            droid.inputs.append(command)
        except OutputEmmitted:
            return droid.outputs[-1]
        
class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 15

    def part_1(self):
        start_time = time.time()

        repair = RepairSystem(self.input)
        repair.move_droid()
        res = len(repair.path)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        repair = RepairSystem(self.input)
        repair.move_droid(True)
        res = repair.oxygen_minutes

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == "__main__":
    solution = Solution()

    solution.part_1()
    
    solution.part_2()
