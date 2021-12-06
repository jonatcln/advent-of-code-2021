from aoc2021 import aoc

import re


@aoc.solver(day=5, part=1)
def part1(data: str):
    return run(data, check_diagonals=False)


@aoc.solver(day=5, part=2)
def part2(data: str):
    return run(data, check_diagonals=True)


def run(data: str, check_diagonals):
    points = set()
    overlap_points = set()
    for text_line in data.splitlines():
        g = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", text_line)
        x1, y1, x2, y2 = [int(n) for n in g.groups()]
        dy, dx = y2 - y1, x2 - x1
        sy, sx = sign(dy), sign(dx)
        xs = range(x1, x2 + sx, sx)
        ys = range(y1, y2 + sy, sy)
        if dx == 0:
            ps = ((x1, y) for y in ys)
        elif dy == 0:
            ps = ((x, y1) for x in xs)
        elif check_diagonals and abs(dy) == abs(dx):
            ps = zip(xs, ys)
        else:
            continue
        for p in ps:
            if p in points:
                overlap_points.add(p)
            else:
                points.add(p)
    return len(overlap_points)


def sign(x):
    return ((x >= 0) << 1) - 1
