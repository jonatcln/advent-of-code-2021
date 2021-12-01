def part1(data: str):
    nums = [int(x) for x in data.splitlines()]
    prev = nums[0]
    increased = 0
    for crnt in nums[1:]:
        if crnt > prev:
            increased += 1
        prev = crnt
    print(increased)
