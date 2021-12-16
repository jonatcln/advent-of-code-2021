from aoc2021 import aoc

from math import prod


@aoc.solver(day=16)
def part1(data: str):
    bitstring = ''.join(f"{int(c, 16):04b}" for c in data)
    _, total_version, total_value = parse_packet(bitstring, 0)
    return total_version, total_value


def parse_packet(bitstring, i):
    if len(bitstring) < 4:
        return

    version_total = int(bitstring[i:i+3], 2)
    type_id = int(bitstring[i+3:i+6], 2)
    i += 6

    if type_id == 4:
        # literal value
        valuestring = ""
        while bitstring[i] == '1':
            valuestring += bitstring[i+1:i+5]
            i += 5
        valuestring += bitstring[i+1:i+5]
        i += 5
        value = int(valuestring, 2)
        return i, version_total, value

    # operator

    length_type_id = bitstring[i]
    i += 1
    values = []
    if length_type_id == '0':
        total_subpacket_length = int(bitstring[i:i+15], 2)
        i += 15
        end_i = i + total_subpacket_length
        while i != end_i:
            i, subtotal, subvalue = parse_packet(bitstring, i)
            values.append(subvalue)
            version_total += subtotal
    else:
        subpacket_count = int(bitstring[i:i+11], 2)
        i += 11
        for _ in range(subpacket_count):
            i, subtotal, subvalue = parse_packet(bitstring, i)
            values.append(subvalue)
            version_total += subtotal
    if type_id == 0:
        value = sum(values)
    elif type_id == 1:
        value = prod(values)
    elif type_id == 2:
        value = min(values)
    elif type_id == 3:
        value = max(values)
    elif type_id == 5:
        value = int(values[0] > values[1])
    elif type_id == 6:
        value = int(values[0] < values[1])
    elif type_id == 7:
        value = int(values[0] == values[1])
    return i, version_total, value
