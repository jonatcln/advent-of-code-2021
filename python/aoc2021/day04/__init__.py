from aoc2021 import aoc


@aoc.solver(day=4, part=1)
def part1(data: str):
    numbers, boards = parse_input(data)
    for num in numbers:
        call_num(boards, num)
        if (w := next(find_winners(boards), None)) is not None:
            return num * sum_of_unmarked(w)


@aoc.solver(day=4, part=2)
def part2(data: str):
    numbers, boards = parse_input(data)
    for num in numbers:
        call_num(boards, num)
        for winner in find_winners(boards):
            if len(boards) == 1:
                return num * sum_of_unmarked(winner)
            boards.remove(winner)


def parse_input(data: str):
    objects = data.split("\n\n")
    numbers = [int(x) for x in objects[0].split(",")]
    boards = [parse_board(x) for x in objects[1:]]
    return numbers, boards


def parse_board(data: str):
    return [[int(x) for x in line.split()] for line in data.splitlines()]


def call_num(boards, num):
    for board in boards:
        for row in board:
            if num in row:
                row[row.index(num)] = None


def find_winners(boards):
    for board in boards:
        if check_rows(board) or check_cols(board):
            yield board


def check_rows(board):
    for row in board:
        if all(x is None for x in row):
            return True
    return False


def check_cols(board):
    for j in range(len(board[0])):
        if all(x[j] is None for x in board):
            return True
    return False


def sum_of_unmarked(board):
    return sum(sum(n for n in row if n is not None) for row in board)
