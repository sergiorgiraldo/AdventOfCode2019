from pathlib import Path
from aocd import submit
from os import path
from abc import ABC, abstractmethod
from typing import final


class AoCException(Exception):
    pass

# Abstract Solution


class BaseSolution(ABC):
    _year: int
    _day: int

    def __init__(cls, lines=False, csv=False, two_dimensional=False):
        if lines:
            cls.input = cls.read_input().splitlines()
        else:
            if csv:
                lines = cls.read_input().splitlines()

                cls.input = [line.split(",") for line in lines]
            else:
                if two_dimensional:
                    lines = cls.read_input().splitlines()

                    cls.input = [list(line) for line in lines]
                else:  # if string:
                    cls.input = cls.read_input()

    @property
    def year(self):
        if not hasattr(self, "_year"):
            raise NotImplementedError("explicitly define Solution._year")
        return self._year

    @property
    def day(self):
        if not hasattr(self, "_day"):
            raise NotImplementedError("explicitly define Solution._day")
        return self._day

    @abstractmethod
    def dummy(self):  # prevent usage of BaseSolution
        pass

    @final
    def read_input(self) -> str:
        """
        handles locating, reading, and parsing input files
        """
        input_file = Path(
            Path(__file__).parent.parent.parent,
            f"input.txt",
        )
        if not input_file.exists():
            raise AoCException(
                f'Failed to find an input file at path "./{input_file.relative_to(Path.cwd())}". You can run `./start --year {self.year} {self.day}` to create it.'
            )

        data = input_file.read_text().strip("\n")

        if not data:
            raise AoCException(
                f'Found a file at path "./{input_file.relative_to(Path.cwd())}", but it was empty. Make sure to paste some input!'
            )
        return data

    @final
    def save(self, part, res, tm):
        answer_path = Path(
            Path(__file__).parent.parent.parent,
            f"ans{part}.txt",
        )

        if path.exists(answer_path):
            open(answer_path, 'w').close()  # always overwrite

        with (answer_path.open("a")) as f:
            f.write(res + "\n")
            f.write(int(tm * 1000).__str__() + " msecs")

    @final
    def submit(self, part, res):
        submit(res, part=part, day=self.day, year=self.year)

    def solve(self, part, res, tm, submit=True):
        self.save(part, str(res), tm)

        print(f"Part {part} :: {res}")

        if submit:
            self.submit(part="a" if part == "1" else "b", res=res)

# Concrete Solutions


class InputAsStringSolution(BaseSolution):
    def __init__(self):
        super().__init__(lines=False, csv=False, two_dimensional=False)

    def dummy(self):
        pass


class InputAsLinesSolution(BaseSolution):
    def __init__(self):
        super().__init__(lines=True, csv=False, two_dimensional=False)

    def dummy(self):
        pass


class InputAsCSVSolution(BaseSolution):
    def __init__(self):
        super().__init__(lines=False, csv=True, two_dimensional=False)

    def dummy(self):
        pass


class InputAs2DSolution(BaseSolution):
    def __init__(self):
        super().__init__(lines=False, csv=False, two_dimensional=True)

    def dummy(self):
        pass
