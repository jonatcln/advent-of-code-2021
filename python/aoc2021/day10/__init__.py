from aoc2021 import aoc

from functools import reduce


syntax_error_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

autocomplete_score = {
    0b010: 1,
    0b101: 2,
    0b111: 3,
    0b011: 4,
}


@aoc.solver(day=10)
def run(data: str):
    syntax_score = 0
    auto_scores = []
    for line in data.splitlines():
        stack = []
        for c in line:
            if is_opening(c):
                stack.append(pair_value(c))
            elif stack.pop() != pair_value(c):
                # this line is corrupt
                syntax_score += syntax_error_score[c]
                break
        else:
            # this line is incomplete
            score = calc_autocomplete_score(stack)
            if score != 0:
                auto_scores.append(score)

    return syntax_score, sorted(auto_scores)[len(auto_scores)//2]


def calc_autocomplete_score(stack):
    return reduce(lambda s, x: s*5 + autocomplete_score[x], reversed(stack), 0)


def pair_value(char):
    return ord(char) >> 4


def is_opening(char):
    return not bool((ord(char) + (ord(char) >> 1)) & 1)
