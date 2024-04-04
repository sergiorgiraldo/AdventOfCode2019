# puzzle prompt: https://adventofcode.com/2019/day/25

import time
import sys
sys.path.insert(0,"..")

from base.advent import *
from base.computer2 import *
from itertools import combinations
from collections import deque

class Solution(InputAsIntCSVLineSolution):
    _year = 2019
    _day = 25

    def play(self, code):
        def oppositeDoor(direction):
            opp = {"north": "south", "south": "north", "east": "west", "west": "east"}
            return opp[direction]

        ignoredItems = set(["infinite loop", "molten lava", "giant electromagnet", "photons", "escape pod"])

        computer_ = Computer(code)
        computer_.run()
        print(computer_.outputs)
        print("****************END*************")

        # Store the command list that reaches the final room with the maximum amount of items
        finalState = None
        maxItemsFound = 0

        # traverse through all rooms, storing (room, inventory) visited states
        visited = set()
        queue = deque([(set(), [], computer_)])
        while queue:
            inventory, path, computer = queue.popleft()

            # Save output and clear it
            text = "".join(chr(c) for c in computer.outputs)
            print(text)
            computer.outputs = []

            # Get room name
            room = text.split("==")[1].strip()
            # print(sum(p.split()[0] != "take" for p in path), room, "-->", sorted(inventory))

            # Ignore if already visited, also marks (room, inventory) as visited
            visKey = (room, tuple(sorted(inventory)))
            if visKey in visited: continue
            visited.add(visKey)

            # Parse room's doors and items
            doors, items = [], []
            doorsStart = text.find("Doors here lead:")
            itemsStart = text.find("Items here:")
            if doorsStart != -1:
                doors = [line[2:] for line in text[doorsStart:itemsStart].split("\n") if line.startswith("-")]
            if itemsStart != -1:
                items = [line[2:] for line in text[itemsStart:].split("\n") if line.startswith("-")]

            # Pick up all items in the room
            for item in items:
                if item in ignoredItems: continue # But ignore the game-ending ones
                path.append("take " + item)
                computer.inputs.extend([ord(c) for c in "take " + item + "\n"])
                computer.run()
                inventory.add(item)

            # After picking items, mark new (room, inventory) as visited also
            visKey = (room, tuple(sorted(inventory)))
            visited.add(visKey)

            # Update maximum amount of items found
            maxItemsFound = max(maxItemsFound, len(inventory))
            # If less than that, then as this is a BFS, this pathing missed an item, so ignore it
            if len(inventory) < maxItemsFound: continue

            # If at final room before floor, save as possible answer and ignore this pathing
            if room == "Security Checkpoint":
                # Get step to reach floor
                floorDirection = doors[0] if doors[0] != oppositeDoor(path[-1]) else doors[1]
                finalState = (computer, list(inventory), floorDirection)
                continue

            # Queue all next steps, copying the current VM for each one
            for door in doors:
                newComputer = computer.copy()
                print("%%%%%%%%%%%%%%% NEW VM ", newComputer.ip)

                newComputer.inputs.extend([ord(c) for c in (door + "\n")])
                newComputer.run()
                print(door, newComputer.outputs)

                queue.append((set(inventory), path+[door], newComputer))

        # Get computer at the checkpoint, list of all safe items and direction of pressure-sensitive floor
        computer, allItems, floorDirection = finalState
        computer.inputs.extend([ord(c) for c in ("\n".join("drop "+item for item in allItems) + "\n")])
        computer.run() # Drop all items

        # Generate all possible item combinations by increasing length
        itemCombinations = []
        for n in range(len(allItems)):
            itemCombinations += list(combinations(allItems, n))

        # Bruteforce the pressure floor by trying all of the combinations 
        inventory = set()
        tooHeavy = []
        for attemptItems in itemCombinations:
            # print("Trying items: {}".format(list(attemptItems)))

            # If inventory is a superset of any of tooHeavy, then it's also going to be too heavy
            if any(set(s).issubset(set(attemptItems)) for s in tooHeavy): continue

            # Drop all items that aren't in attemptItems
            toDrop = [item for item in inventory if item not in attemptItems]
            computer.inputs.extend([ord(c) for c in ("\n".join("drop "+item for item in toDrop) + "\n")])
            computer.run()
            inventory = inventory.difference(set(toDrop))

            # Pick up all from attemptItems that aren't yet in inventory
            toPick = [item for item in attemptItems if item not in inventory]
            computer.inputs.extend([ord(c) for c in ("\n".join("take "+item for item in toPick) + "\n")])
            computer.run()
            inventory = inventory.union(set(toPick))

            # Activate floor
            computer.inputs.extend([ord(c) for c in (floorDirection+"\n")])
            computer.run()

            text = "".join(chr(c) for c in computer.outputs)
            computer.outputs = []

            # Verify result
            if text.find("Alert!") == -1:
                print(path, "\n") 
                print("Part 1: {}".format(text.split()[-8]))
                break
            elif text.find("lighter") != -1: # Too heavy, add as invalid subset
                tooHeavy.append(attemptItems)

    def part_1(self):
        start_time = time.time()

        self.play(self.input)

        end_time = time.time()

        # self.solve("1", res, (end_time - start_time))

    def part_2(self):
        start_time = time.time()

        arr = self.input
        res = ""

        end_time = time.time()

        self.solve("2", res, (end_time - start_time))

if __name__ == '__main__':
    solution = Solution()

    solution.part_1()
    
    # solution.part_2()