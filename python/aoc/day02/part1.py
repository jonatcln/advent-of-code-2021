def part1(data: str):
    pos = depth = 0
    for line in data.splitlines():
        command, n = line.split()
        n = int(n)
        if command == "down":
            depth += n
        elif command == "up":
            depth -= n
        elif command == "forward":
            pos += n
    print(pos*depth)
