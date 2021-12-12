from aoc2021 import aoc

from collections import defaultdict


@aoc.solver(day=12)
def part1(data: str):
    graph = defaultdict(set)
    for line in data.splitlines():
        p = line.split("-")
        graph[p[0]].add(p[1])
        graph[p[1]].add(p[0])
    return (
        sum(1 for _ in find_paths1(graph, ["start"])),
        sum(1 for _ in find_paths2(graph, ["start"])),
    )


def find_paths1(edges, path):
    node = path[-1]
    for n in edges[node]:
        if n == "end":
            yield [*path, n]
        elif n.isupper() or n not in path:
            yield from find_paths1(edges, [*path, n])


def find_paths2(edges, path, twice=False):
    node = path[-1]
    for n in edges[node]:
        if n == "start":
            continue
        elif n == "end":
            yield [*path, n]
        elif n.isupper():
            yield from find_paths2(edges, [*path, n], twice)
        elif not twice:
            yield from find_paths2(edges, [*path, n], n in path)
        elif n not in path:
            yield from find_paths2(edges, [*path, n], twice)
