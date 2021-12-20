from aoc2021 import aoc


@aoc.solver(day=20, part=1)
def part1(data: str):
    return run_enhancer(data, 2)


@aoc.solver(day=20, part=2)
def part2(data: str):
    return run_enhancer(data, 50)


def run_enhancer(data: str, times: int):
    raw_algo, raw_grid = data.split("\n\n")
    assert len(raw_algo) == 2**9
    algorithm = [int(x == '#') for x in raw_algo]
    topleft = -1
    pixels = PixelCollection(0)
    right, bottom = pixels.parse(raw_grid, lambda x: int(x == '#'))
    for _ in range(times):
        enhanced_pixels = PixelCollection(algorithm[-pixels.get_default()])
        for y in range(topleft, bottom+1):
            for x in range(topleft, right+1):
                enhanced_pixels.set(x, y, enhance(algorithm, pixels, x, y))
        topleft -= 1
        right += 1
        bottom += 1
        pixels = enhanced_pixels
    return sum(p for p in pixels.values())


class PixelCollection:
    def __init__(self, default_pixel):
        self.default = default_pixel
        self.pixels = {}

    def get(self, x, y):
        return self.pixels.get((x, y), self.default)

    def set(self, x, y, pixel):
        self.pixels[(x, y)] = pixel

    def get_default(self):
        return self.default

    def values(self):
        return self.pixels.values()

    def parse(self, raw_pixel_grid, to_pixel):
        lines = raw_pixel_grid.splitlines()
        for y, row in enumerate(lines):
            for x, p in enumerate(row):
                self.pixels[(x, y)] = to_pixel(p)
        return len(lines[0]), len(lines)


def enhance(algorithm, pixels, pixel_x, pixel_y):
    index = 0
    for y in range(pixel_y-1, pixel_y+2):
        for x in range(pixel_x-1, pixel_x+2):
            index = (index << 1) | pixels.get(x, y)
    return algorithm[index]
