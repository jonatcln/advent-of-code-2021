from aoc2021 import aoc

from collections import Counter, defaultdict


@aoc.solver(day=14, part=1)
def part1(data: str):
    return run(data, 10)


@aoc.solver(day=14, part=2)
def part2(data: str):
    return run(data, 40)


def run(data: str, n: int) -> int:
    polymer, rules = parse_input(data)
    rules = dict((s, (s[0] + c, c + s[1])) for s, c in rules.items())
    pair_counts = Counter(overlapping_pairs(polymer))
    last = polymer[-1]
    for _ in range(n):
        new_counts = Counter()
        for s in pair_counts:
            p1, p2 = rules[s]
            new_counts[p1] += pair_counts[s]
            new_counts[p2] += pair_counts[s]
        pair_counts = new_counts
    elem_counts = get_element_counts(pair_counts, last)
    return max(elem_counts) - min(elem_counts)


def parse_input(data: str):
    lines = data.splitlines()
    template = lines[0]
    insertion_rules = dict(x.split(" -> ") for x in lines[2:])
    return template, insertion_rules


def overlapping_pairs(polymer: str):
    for i in range(len(polymer) - 1):
        yield polymer[i:i+2]


def get_element_counts(pair_counts, last):
    counts = defaultdict(int)
    for s, k in pair_counts.items():
        counts[s[0]] += k
    counts[last] += 1
    return counts.values()
