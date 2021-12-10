from aoc2021 import aoc

from aoc2021.utils import Grid, Point

from math import prod
from copy import deepcopy


@aoc.solver(day=9, part=1)
def part1(data: str):
    grid = Grid.parse(data, lambda x: int(x))
    total = 0
    for point in grid.points():
        m = min(grid.get(p) for p in adjacent_points(point) if grid.has_pos(p))
        if grid.get(point) < m:
            risk = grid.get(point) + 1
            total += risk
    return total


@aoc.solver(day=9, part=2)
def part2(data: str):
    grid = Grid.parse(data, lambda x: int(x))
    basin_sizes = []
    minima = []
    for point in grid.points():
        m = min(grid.get(p) for p in adjacent_points(point) if grid.has_pos(p))
        if grid.get(point) < m:
            minima.append(point)
    old_grid = deepcopy(grid)
    grid.map(lambda p, _: to_hor_range(old_grid, p))
    for m in minima:
        ranges = set()
        find_basin_ranges(grid, m, ranges)
        basin_sizes.append(sum(x[2] for x in ranges))
    return prod(list(sorted(basin_sizes))[-3:])


def adjacent_points(p: Point):
    return Point(p.x - 1, p.y), Point(p.x + 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1)


def find_basin_ranges(grid, p: Point, ranges):
    if not grid.has_pos(p):
        return
    r = grid.get(p)
    if r[2] == 0 or r in ranges:
        return
    ranges.add(r)
    for y in (p.y + 1, p.y - 1):
        if not grid.has_pos(Point(p.x, y)):
            continue
        for x in range(r[0], r[0] + r[2]):
            find_basin_ranges(grid, Point(x, y), ranges)


def to_hor_range(grid, p: Point):
    if grid.get(p) == 9:
        return (p.x, p.y, 0)
    min_x = 0
    max_x = grid.width - 1
    for x in range(p.x - 1, -1, -1):
        if grid.get(Point(x, p.y)) == 9:
            min_x = x + 1
            break
    for x in range(p.x + 1, grid.width):
        if grid.get(Point(x, p.y)) == 9:
            max_x = x - 1
            break
    return (min_x, p.y, max_x - min_x + 1)
