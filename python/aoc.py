#!/usr/bin/env python3

import argparse
from datetime import date

from aoc import YEAR, AOC


def default_input_file(day):
    return f"input/day{day:02d}.txt"


def main():
    advent_start = date(YEAR, 12, 1)
    delta_days = (date.today() - advent_start).days + 1

    if delta_days < 1:
        err_no_day_msg = f"Advent of Code {YEAR} starts within {-delta_days} days."
        today = None
    elif delta_days > 25:
        err_no_day_msg = f"Advent of Code {YEAR} ended {delta_days - 25} days ago."
        today = None
    else:
        today = delta_days

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", metavar="DAY", type=int, choices=range(1, 26), default=today,
                        help="day to run (default: today's day)")
    parser.add_argument("-p", metavar="PART", type=int, choices=[1, 2], default=None,
                        help="part to run (default: last implemented)")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", metavar="INPUT_STRING", type=str, default=None,
                        help="input string")
    input_group.add_argument("-f", metavar="INPUT_FILE", type=argparse.FileType('r'), default=None,
                        help="input filename")

    args = parser.parse_args()

    day = args.d

    if day is None:
        parser.error(err_no_day_msg)

    if day not in AOC.keys():
        parser.error(f"day {day} hasn't been implemented yet")

    part = args.p or len(AOC[day].keys())

    if part not in AOC[day].keys():
        parser.error(f"day {day} part {part} hasn't been implemented yet")

    if args.i:
        data = args.i
    elif args.f:
        data = args.f.read()
        args.f.close()
    else:
        file = open(default_input_file(day), 'r')
        data = file.read()
        file.close()

    AOC[day][part](data)


if __name__ == '__main__':
    main()
