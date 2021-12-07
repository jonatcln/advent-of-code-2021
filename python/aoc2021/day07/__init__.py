from aoc2021 import aoc


@aoc.solver(day=7, part=1)
def part1(data: str):
    return min(fuels(data, lambda x: x))


@aoc.solver(day=7, part=2)
def part2(data: str):
    return min(fuels(data, lambda x: x*(x+1)//2))


def fuels(data: str, calc_fuel):
    positions = [int(x) for x in data.split(",")]
    for a in range(min(positions), max(positions) + 1):
        yield sum(calc_fuel(abs(x-a)) for x in positions)
