from aoc2021 import aoc


@aoc.solver(day=3, part=1)
def part1(data: str):
    lines = data.splitlines()
    width = len(lines[0])

    gamma = int(most_common_bits(lines), 2)
    epsilon = 2**(width) - 1 - gamma

    return gamma * epsilon


@aoc.solver(day=3, part=2)
def part2(data: str):
    lines = data.splitlines()

    # Binary search the numbers in the list (digits from left to right)
    # and choose each time:
    # - the most common bit for oxy ('1' on tie)
    # - the least common bit for co2 ('0' on tie)
    # to recursively search the next bits of all values starting with that bit.
    lines.sort(reverse=True)
    oxy_bin_str = binary_search(lines, flip=False)
    co2_bin_str = binary_search(lines, flip=True)

    return int(oxy_bin_str, 2) * int(co2_bin_str, 2)


def most_common_bits(lines):
    bit_at = [[k[i] for k in lines] for i in range(len(lines[0]))]
    return ''.join(max('0', '1', key=lambda x: bs.count(x)) for bs in bit_at)


def binary_search(lines, flip):
    if len(lines) == 0:
        return ''
    if len(lines) == 1:
        return lines[0]
    count = sum(x[0] == '1' for x in lines)
    c, f = ('0', '1') if flip else ('1', '0')
    b = c if count*2 >= len(lines) else f
    return b + binary_search([x[1:] for x in lines if x[0] == b], flip)
