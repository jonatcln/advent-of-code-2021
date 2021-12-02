def part1(data: str):
    nums = [int(x) for x in data.splitlines()]
    prev = nums[0]
    increased = 0
    for crnt in nums[1:]:
        if crnt > prev:
            increased += 1
        prev = crnt
    print(increased)


def part2(data: str):
    nums = [int(x) for x in data.splitlines()]
    prev = sum(nums[:3])
    increased = 0
    for i in range(1, len(nums) - 2):
        crnt = sum(nums[i:i+3])
        if crnt > prev:
            increased += 1
        prev = crnt
    print(increased)
