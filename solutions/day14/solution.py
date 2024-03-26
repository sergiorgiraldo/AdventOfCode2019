# puzzle prompt: https://adventofcode.com/2019/day/14

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from collections import defaultdict
from math import ceil
from statistics import median
import re

class Solution(InputAsLinesSolution):
    _year = 2019
    _day = 14

    def parse(self, lines):
        reactions = {}

        for reaction in lines:
            sources, target = reaction.split("=>")
            elements = [self.parse_volume_and_name(element) for element in sources.split(",")]
            target = self.parse_volume_and_name(target)
            reactions[target] = elements

        return reactions

    def parse_volume_and_name(self, data):
        volume = int(re.findall(r"\d+", data)[0])
        name = re.findall("[A-Z]+", data)[0]
        return volume, name

    def make_recipe(self, name, volume, reactions_list):
        for target, components in reactions_list.items():
            target_volume, target_name = target
            if target_name == name:
                reactions_to_trigger = ceil(volume / target_volume)
                volume_created = target_volume * reactions_to_trigger
                components_required = [
                    (component[0] * reactions_to_trigger, component[1]) for component in components]
                return components_required, volume_created

    def get_required_ore(self, lines, elements):
        reactions = self.parse(lines)

        ore_required = 0
        inventory = defaultdict(int)

        while len(elements) > 0:
            next_elements = []

            for element in elements:
                el_volume, el_name = element
                if el_name == "ORE":
                    ore_required += el_volume
                elif el_name in inventory:
                    volume_to_create = el_volume - inventory[el_name]

                    if volume_to_create > 0:
                        inventory.pop(el_name)
                        next_elements.append((volume_to_create, el_name))
                    else:
                        inventory[el_name] -= el_volume
                else:
                    next_components, volume_created = self.make_recipe(el_name, el_volume, reactions)
                    
                    if volume_created > el_volume:
                        inventory[el_name] += volume_created - el_volume

                    next_elements.extend(next_components)

            elements = next_elements

        return ore_required

    def maximize_fuel(self, lines):
        ore_available = 1_000_000_000_000
        min_range = 0
        max_range = ore_available
        guess = int(median([min_range, max_range]))

        while max_range - min_range > 1:
            ore_consumed = self.get_required_ore(lines, [(guess, "FUEL")])
            if ore_available - ore_consumed < 0:
                max_range = guess
            else:
                min_range = guess
            guess = int(median([min_range, max_range]))

        return guess

    def part_1(self):
        start_time = time.time()

        res = self.get_required_ore(self.input, [(1, "FUEL")])

        end_time = time.time()

        self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        res = self.maximize_fuel(self.input)

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))


if __name__ == "__main__":
    solution = Solution()

    solution.part_1()

    solution.part_2()
