from aoc2021 import aoc

from copy import deepcopy


@aoc.solver(day=18, part=1)
def part1(data: str):
    lines = data.splitlines()
    result = Pair.from_list(eval(lines[0]))
    for line in lines[1:]:
        pair = Pair.from_list(eval(line))
        result += pair
    return result.magnitude()


@aoc.solver(day=18, part=2)
def part2(data: str):
    numbers = [Pair.from_list(eval(line)) for line in data.splitlines()]
    highest = 0
    for x in numbers:
        for y in numbers:
            m = (x + y).magnitude()
            if m > highest:
                highest = m
    return highest


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, lst):
        if isinstance(lst[0], list):
            left = Pair.from_list(lst[0])
        else:
            left = int(lst[0])
        if isinstance(lst[1], list):
            right = Pair.from_list(lst[1])
        else:
            right = int(lst[1])
        return cls(left, right)

    def __add__(self, other):
        result = Pair(deepcopy(self), deepcopy(other))
        result.reduce()
        return result

    def __iadd__(self, other):
        result = Pair(self, other)
        result.reduce()
        return result

    def reduce(self):
        while True:
            if self.try_explode()[0]:
                continue
            if not self.try_split():
                break

    def try_explode(self, d=0):
        if d == 4:
            assert isinstance(self.left, int)
            assert isinstance(self.right, int)
            return True, self.left, self.right, 0

        if isinstance(self.left, Pair):
            s, a, b, c = self.left.try_explode(d+1)
            if s:
                self.left = c
                if b is not None:
                    if isinstance(self.right, int):
                        self.right += b
                    else:
                        self.right.add_to_leftmost(b)
                return True, a, None, self

        if isinstance(self.right, Pair):
            s, a, b, c = self.right.try_explode(d+1)
            if s:
                self.right = c
                if a is not None:
                    if isinstance(self.left, int):
                        self.left += a
                    else:
                        self.left.add_to_rightmost(a)
                return True, None, b, self

        return False, None, None, self

    def add_to_leftmost(self, n):
        if isinstance(self.left, Pair):
            self.left.add_to_leftmost(n)
        else:
            self.left += n

    def add_to_rightmost(self, n):
        if isinstance(self.right, Pair):
            self.right.add_to_rightmost(n)
        else:
            self.right += n

    def try_split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = Pair(self.left//2, (self.left+1)//2)
                return True
        elif self.left.try_split():
            return True
        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = Pair(self.right//2, (self.right+1)//2)
                return True
        elif self.right.try_split():
            return True
        return False

    def magnitude(self):
        mag = 0
        if isinstance(self.left, int):
            mag += 3*self.left
        else:
            mag += 3*self.left.magnitude()
        if isinstance(self.right, int):
            mag += 2*self.right
        else:
            mag += 2*self.right.magnitude()
        return mag

    def __deepcopy__(self, memo):
        return Pair(deepcopy(self.left, memo), deepcopy(self.right, memo))

    def __str__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

    def __repr__(self):
            return str(self)
