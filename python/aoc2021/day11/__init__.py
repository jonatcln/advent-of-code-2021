from aoc2021 import aoc

from aoc2021.utils import Grid


@aoc.solver(day=11, part=1)
def part1(data: str):
    grid = Grid.parse(data, int)
    flashes = 0
    for _ in range(100):
        grid.map(lambda _, x: x + 1)
        while (p := grid.find_first(lambda _, x: x is not None and x > 9)) is not None:
            grid.set(p, None)
            flashes += 1
            for a in p.adjacents_with_diagonals():
                if (v := grid.get(a)) is not None:
                    grid.set(a, v + 1)
        grid.replace(None, 0)
    return flashes


@aoc.solver(day=11, part=2)
def part2(data: str):
    grid = Grid.parse(data, int)
    step = 0
    while grid.find_any(lambda _, x: x != 0):
        grid.map(lambda _, x: x + 1)
        while (p := grid.find_first(lambda _, x: x is not None and x > 9)) is not None:
            grid.set(p, None)
            for a in p.adjacents_with_diagonals():
                if (v := grid.get(a)) is not None:
                    grid.set(a, v + 1)
        grid.replace(None, 0)
        step += 1
    return step
