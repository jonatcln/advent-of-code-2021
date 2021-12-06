from aoc2021 import aoc


@aoc.solver(day=6, part=1)
def part1(data: str):
    return simulate(data, 80)


@aoc.solver(day=6, part=2)
def part2(data: str):
    return simulate(data, 256)


def simulate(data: str, cycles: int) -> int:
    fish = [int(x) for x in data.split(',')]
    fish_counts = dict((x, fish.count(x)) for x in range(9))
    for _ in range(cycles):
        zeros = fish_counts[0]
        for age in range(8):
            fish_counts[age] = fish_counts[age+1]
        fish_counts[6] += zeros
        fish_counts[8] = zeros
    return sum(fish_counts.values())
