from aoc2021 import aoc


@aoc.solver(day=8, part=1)
def part1(data: str):
    s = 0
    for line in data.splitlines():
        patterns, digits = [x.split() for x in line.split(" | ")]
        s += sum(len(x) in {2, 4, 3, 7} for x in digits)
    return s


@aoc.solver(day=8, part=2)
def part2(data: str):
    total = 0
    for line in data.splitlines():
        patterns, digits = [x.split() for x in line.split(" | ")]
        pat_to_num = resolve(patterns)
        total += int(''.join(str(pat_to_num[frozenset(x)]) for x in digits))
    return total


def resolve(patterns):
    len_to_num = {2: 1, 4: 4, 3: 7, 7: 8}
    pat_to_num = dict((frozenset(p), len_to_num[len(p)]) for p in patterns if len(p) in len_to_num)
    cf = set(next(x for x in pat_to_num if pat_to_num[x] == 1))
    bcdf = set(next(x for x in pat_to_num if pat_to_num[x] == 4))
    fives = set(frozenset(p) for p in patterns if len(p) == 5)
    sixes = set(frozenset(p) for p in patterns if len(p) == 6)
    pat_to_num2 = {
        next(x for x in fives if cf < set(x)): 3,
        next(x for x in fives if len(set(x) | bcdf) == 7): 2,
        next(x for x in sixes if len(set(x) - cf) == 5): 6,
        next(x for x in sixes if len(set(x) - bcdf) == 2): 9,
    }
    pat_to_num3 = {
        (fives - set(pat_to_num2.keys())).pop(): 5,
        (sixes - set(pat_to_num2.keys())).pop(): 0,
    }
    return {**pat_to_num, **pat_to_num2, **pat_to_num3}
