from aoc2021 import aoc

from collections import defaultdict


@aoc.solver(day=12)
def run(data: str):
    graph = defaultdict(set)
    for line in data.splitlines():
        n1, n2 = line.split("-")
        graph[n1].add(n2)
        graph[n2].add(n1)
    return (
        find_paths1(graph, "start", set()),
        find_paths2(graph, "start", set()),
    )


def find_paths1(edges, node, lowers):
    count = 0
    for n in edges[node]:
        if n == "start":
            continue
        elif n == "end":
            count += 1
        elif n.isupper():
            count += find_paths1(edges, n, lowers)
        elif n not in lowers:
            count += find_paths1(edges, n, lowers | {n})
    return count


def find_paths2(edges, node, lowers, twice=False):
    count = 0
    for n in edges[node]:
        if n == "start":
            continue
        elif n == "end":
            count += 1
        elif n.isupper():
            count += find_paths2(edges, n, lowers, twice)
        elif not twice:
            count += find_paths2(edges, n, lowers | {n}, n in lowers)
        elif n not in lowers:
            count += find_paths2(edges, n, lowers | {n}, twice)
    return count
