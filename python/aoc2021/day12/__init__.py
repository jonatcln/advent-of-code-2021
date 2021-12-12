from aoc2021 import aoc

from collections import defaultdict


@aoc.solver(day=12)
def run(data: str):
    graph = defaultdict(set)
    for line in data.splitlines():
        p = line.split("-")
        graph[p[0]].add(p[1])
        graph[p[1]].add(p[0])
    return (
        find_paths1(graph, set(), "start"),
        find_paths2(graph, set(), "start"),
    )


def find_paths1(edges, lowers, node):
    count = 0
    for n in edges[node]:
        if n == "start":
            continue
        elif n == "end":
            count += 1
        elif n.isupper():
            count += find_paths1(edges, lowers, n)
        elif n not in lowers:
            count += find_paths1(edges, lowers | {n}, n)
    return count


def find_paths2(edges, lowers, node, twice=False):
    count = 0
    for n in edges[node]:
        if n == "start":
            continue
        elif n == "end":
            count += 1
        elif n.isupper():
            count += find_paths2(edges, lowers, n, twice)
        elif not twice:
            count += find_paths2(edges, lowers | {n}, n, n in lowers)
        elif n not in lowers:
            count += find_paths2(edges, lowers | {n}, n, twice)
    return count
