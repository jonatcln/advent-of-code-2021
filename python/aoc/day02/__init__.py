def part1(data: str):
    pos = depth = 0
    for line in data.splitlines():
        command, ns = line.split()
        n = int(ns)
        if command == "down":
            depth += n
        elif command == "up":
            depth -= n
        elif command == "forward":
            pos += n
    print(pos*depth)

def part2(data: str):
    pos = depth = aim = 0
    for line in data.splitlines():
        command, ns = line.split()
        n = int(ns)
        if command == "down":
            aim += n
        elif command == "up":
            aim -= n
        elif command == "forward":
            pos += n
            depth += aim*n
    print(pos*depth)
