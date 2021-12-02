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
