# puzzle prompt: https://adventofcode.com/2019/day/20

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from collections import defaultdict
from copy import copy

class Dungeon:
    def __init__(self, layout, recursive = False):
        self.area         = defaultdict(str)
        self.size_x       = len(layout[2])+4
        self.size_y       = len(layout)
        self.portals      = defaultdict(list)
        self.portal_names = defaultdict(str)
        self.paths        = defaultdict(list)
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                if x < len(layout[y]):
                    self.area[(x, y)] = layout[y][x]
        
        self.reduce_dungeon()
        self.find_portals() if not recursive else self.find_portals_recursive()
        self.find_paths()

    def is_dead_end(self, pos, keys_allowed = False):
        tile = self.area[pos]
        if tile == "#" or tile == "@" or (not keys_allowed and tile.islower()):
            return False
        
        count = sum(self.area[(pos[0] + side[0], pos[1] + side[1])] != "#" for side in [(-1,0), (0,-1), (1,0), (0,1)])
        
        if count <= 1:
            return True
        return False
    
    def reduce_dungeon(self):
        reduced = True
        while reduced:
            reduced = False
            for y in range(1, self.size_y):
                for x in range(1, self.size_x):
                    if self.is_dead_end((x, y)):
                        self.area[(x, y)] = "#"
                        reduced = True

    def find_portals(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.area[(x, y)].isupper():
                    if self.area[(x+1, y)].isupper():
                        name = self.area[(x, y)] + self.area[(x+1, y)]
                        if not name in [p[0] for p in self.portals]:
                            id = 0
                        else:
                            id = 1
                        if self.area[(x+2, y)] == ".":
                            self.portals[(name, id)].append((x+2, y))
                            self.portal_names[(x+1, y)] = (name, id)
                        elif self.area[(x-1, y)] == ".":
                            self.portals[(name, id)].append((x-1, y))
                            self.portal_names[(x, y)] = (name, id)
                            
                    elif self.area[(x, y+1)].isupper():
                        name = self.area[(x, y)] + self.area[(x, y+1)]
                        if not name in [p[0] for p in self.portals]:
                            id = 0
                        else:
                            id = 1
                        if self.area[(x, y+2)] == ".":
                            self.portals[(name, id)].append((x, y+2))
                            self.portal_names[(x, y+1)] = (name, id)
                        elif self.area[(x, y-1)] == ".":
                            self.portals[(name, id)].append((x, y-1))
                            self.portal_names[(x, y)] = (name, id)
                        
    def find_portals_recursive(self):
            for y in range(self.size_y):
                for x in range(self.size_x):
                    if self.area[(x, y)].isupper():
                        if x > 10 and y > 10    and \
                           x < self.size_x - 10 and \
                           y < self.size_y - 10:
                            id = 1
                        else:
                            id = -1
                            
                        if self.area[(x+1, y)].isupper():
                            name = self.area[(x, y)] + self.area[(x+1, y)]
                            if self.area[(x+2, y)] == ".":
                                self.portals[(name, id)].append((x+2, y))
                                self.portal_names[(x+1, y)] = (name, id)
                            elif self.area[(x-1, y)] == ".":
                                self.portals[(name, id)].append((x-1, y))
                                self.portal_names[(x, y)] = (name, id)
                                
                        elif self.area[(x, y+1)].isupper():
                            name = self.area[(x, y)] + self.area[(x, y+1)]
                            if self.area[(x, y+2)] == ".":
                                self.portals[(name, id)].append((x, y+2))
                                self.portal_names[(x, y+1)] = (name, id)
                            elif self.area[(x, y-1)] == ".":
                                self.portals[(name, id)].append((x, y-1))
                                self.portal_names[(x, y)] = (name, id)

    def find_paths(self):
        for name, positions in self.portals.items():
            for pos in positions:
                next_search = defaultdict(int)
                next_search[pos] = 1

                changes = True
                steps   = 0
        
                while changes or not steps:
                    changes = False
                    steps  += 1
                    search = copy(next_search)
            
                    for position, state in search.items():
                        if state == -1:
                            del next_search[position]
                        if state == 1:
                            next_search[position] = -1
                            for side in [(-1,0), (0,-1), (1,0), (0,1)]:
                                side_pos = (position[0] + side[0], position[1] + side[1])
                                if self.area[side_pos] != "#" and \
                                 not search[side_pos]:
                                    del search[side_pos]
                                    changes = True
                                    next_search[side_pos] = 1
                                    if self.area[side_pos].isupper():
                                        next_search[side_pos] = -1
                                        if steps > 1:
                                            target_name = self.portal_names[(side_pos)]
                                            self.paths[name].append((target_name, steps-1))

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 20

    def find_shortest_way(self, dungeon, path = [("AA", 0)], best_steps = 1e8, steps = 0):
        if path[-1] == ("ZZ", 1):
            return steps

        for next_portal in dungeon.paths[path[-1]]:
            if next_portal[0] in path:
                continue
            
            next_steps = steps + next_portal[1] + 1
            if next_steps >= best_steps:
                continue

            if next_portal[0][1] == 0:
                id = 1
            else:
                id = 0
                
            next_path = path + [next_portal] + [(next_portal[0][0], id)]
            this_steps = self.find_shortest_way(dungeon, next_path, best_steps, next_steps)

            if this_steps < best_steps:
                best_steps = this_steps
        
        return best_steps
    
    def find_shortest_way_recursive(self, dungeon, path = [("AA", -1, 0)], best_steps = 1e8, steps = 0):
        # print("\n", path)
        depth = path[-1][2]
        if depth > 25:
            # print("out 1")
            return 1e8
        if depth == -1:
            # print("out 2")
            return steps
        best_path = None
        for next_portal in sorted(dungeon.paths[(path[-1][0], path[-1][1])], key = lambda x: x[1], reverse = True):
            situation = (next_portal[0][0], next_portal[0][1], depth)

            if situation in path:
                continue
            if (situation[0] == "AA" or situation[0] == "ZZ") and situation[2] > 0:
                continue
            if (situation[0] != "AA" and situation[0] != "ZZ") and situation[1] == -1 and situation[2] == 0:
                continue
            
            next_steps = steps + next_portal[1] + 1
            if next_steps >= best_steps:
                continue

            if next_portal[0][1] == -1:
                id = 1
            else:
                id = -1
                
            next_path = path + [situation] + [(next_portal[0][0], id, depth + next_portal[0][1])]
            this_steps = self.find_shortest_way_recursive(dungeon, next_path, best_steps, next_steps)

            if this_steps < best_steps:
                best_steps = this_steps
                best_path = path

        return best_steps   

    def escape_maze(self, lines):
        dungeon = Dungeon(lines)
        return self.find_shortest_way(dungeon) - 1

    def escape_recursive_maze(self, lines):
        dungeon = Dungeon(lines, True)
        return self.find_shortest_way_recursive(dungeon) - 1
    
    def part_1(self):
        start_time = time.time()

        res = self.escape_maze(self.input)

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.escape_recursive_maze(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    solution.part_2()