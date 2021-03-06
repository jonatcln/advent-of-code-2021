from typing import Callable, Generic, Iterator, TypeVar, Optional, List
import enum

T = TypeVar('T')


class GeometricPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, p: 'GeometricPoint') -> float:
        return ((p.x - self.x)**2 + (p.y - self.y)**2) ** 0.5

    def distance_to_origin(self) -> float:
        return self.distance_to(GeometricPoint(0.0, 0.0))


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, p: 'Point') -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def distance_to_origin(self) -> int:
        return self.distance_to(Point(0, 0))

    def as_geometric_point(self) -> GeometricPoint:
        return GeometricPoint(float(self.x), float(self.y))

    def diagonally_adjacents(self) -> Iterator['Point']:
        for dy in (-1, 1):
            for dx in (-1, 1):
                yield Point(self.x + dx, self.y + dy)

    def adjacents(self) -> Iterator['Point']:
        return (
            Point(self.x, self.y - 1),
            Point(self.x - 1, self.y),
            Point(self.x + 1, self.y),
            Point(self.x, self.y + 1),
        ).iter()

    def adjacents_with_diagonals(self) -> Iterator['Point']:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx != 0 or dy != 0:
                    yield Point(self.x + dx, self.y + dy)

    def __repr__(self):
        return str((self.x, self.y))


class Grid(Generic[T]):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = [[]]

    @classmethod
    def new_empty(cls, width: int, height: int, init_value: T) -> 'Grid':
        grid = cls()
        grid.width = width
        grid.height = height
        grid.grid = [[init_value for _ in range(width)] for _ in range(height)]
        return grid

    @classmethod
    def from_matrix(cls, matrix: List[List[T]]) -> 'Grid':
        grid = cls()
        grid.height = len(matrix)
        grid.width = len(matrix[0])
        grid.grid = matrix
        return grid

    @classmethod
    def parse(cls, raw: str, char_to_symbol: Callable[[str], T]) -> 'Grid':
        data = [[char_to_symbol(c) for c in line] for line in raw.splitlines()]
        return cls.from_matrix(data)

    def has_pos(self, p: Point) -> bool:
        """Return if the point `p` is in this within the grid boundaries."""
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def get(self, p: Point) -> Optional[T]:
        if not self.has_pos(p):
            return None
        return self.grid[p.y][p.x]

    def set(self, p: Point, value: T) -> bool:
        """Set the cell at point `p` to `value` and return success?"""
        if not self.has_pos(p):
            return False
        self.grid[p.y][p.x] = value
        return True

    def find(self, f: Callable[[Point, T], bool]) -> Iterator[Point]:
        """Return an iterator over all points for which `f` returns True."""
        return (p for p in self.points() if f(p, self.grid[p.y][p.x]))

    def find_item(self, item: T) -> Iterator[Point]:
        """Return an iterator over all points at which an item equal to `item` is stored."""
        return (p for p in self.points() if item == self.grid[p.y][p.x])

    def find_any(self, f: Callable[[Point, T], bool]) -> bool:
        """Return whether there's an item for which `f` returns True."""
        return any(f(p, self.grid[p.y][p.x]) for p in self.points())

    def find_first(self, f: Callable[[Point, T], bool]) -> Optional[Point]:
        """Return the position of the first item for which `f` returns True (None if nothing matched)."""
        return next((p for p in self.points() if f(p, self.grid[p.y][p.x])), None)

    def row(self, y: int) -> Iterator[T]:
        """Return an iterator over all elements in the row with the given index `y`."""
        return iter(self.grid[y])

    def col(self, x: int) -> Iterator[T]:
        """Return an iterator over all elements in the column with the given index `x`."""
        return (self.grid[y][x] for y in range(self.height))

    def reset(self, reset_value: T):
        """Reset all cells to the given `reset_value`."""
        for p in self.points():
            self.grid[p.y][p.x] = reset_value

    def map(self, f: Callable[[Point, T], T]):
        """Apply `f` to each element. `f` is a function `Point, val -> new_val`"""
        for p in self.points():
            self.grid[p.y][p.x] = f(p, self.grid[p.y][p.x])

    def replace(self, old_item: T, new_item: T):
        """Replace every item equal to `old_item` by `new_item`."""
        for p in self.find_item(old_item):
            self.grid[p.y][p.x] = new_item

    def find_replace(self, find_item: Callable[[Point, T], bool], new_item: T):
        """Replace every item for which `find_item` returns True by `new_item`."""
        for p in self.find(find_item):
            self.grid[p.y][p.x] = new_item

    def replace_with_init(self, old_item: T, init_new_item: Callable[[Point], T]):
        """Replace every item equal to `old_item` by a new item initialized by `init_new_item`."""
        for p in self.find_item(old_item):
            self.grid[p.y][p.x] = init_new_item(p)

    def find_replace_with_init(self, find_item: Callable[[Point, T], bool], init_new_item: Callable[[Point, T], T]):
        """Replace every item for which `find_item` returns True by a new item initialized by `init_new_item`."""
        for p in self.find(find_item):
            self.grid[p.y][p.x] = init_new_item(p)

    def points(self) -> Iterator[Point]:
        """
        Return an iterator over all valid points in the following order:
            top left -> top right
            ...
            bottom left -> bottom right
        """
        for y in range(self.height):
            for x in range(self.width):
                yield Point(x, y)



class Direction(enum.Enum):
    U = N = UP = NORTH = 0
    R = E = RIGHT = EAST = 1
    D = S = DOWN = SOUTH = 2
    L = W = LEFT = WEST = 3

    def opposite(self) -> 'Direction':
        return self.rotate(2)

    def rotate_cw(self) -> 'Direction':
        return self.rotate(1)

    def rotate_ccw(self) -> 'Direction':
        return self.rotate(-1)

    def rotate(self, n: int) -> 'Direction':
        """Rotate n times 90 degrees. (to left if n < 0, to right if n > 0)"""
        return Direction((self.value + n) % 4)

    # Aliases

    def rotate_right(self) -> 'Direction':
        return self.rotate_cw()

    def rotate_left(self) -> 'Direction':
        return self.rotate_ccw()

    def mirror(self) -> 'Direction':
        return self.opposite()
