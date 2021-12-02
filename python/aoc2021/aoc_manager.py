from typing import Callable, Set, Dict, Any


class AocManager:
    def __init__(self, year: int):
        self.year = year
        self._solvers: Dict[int, Dict[int, Callable[[str], None]]] = {}

    def days(self) -> Set[int]:
        """Return a set of all days who have at least one part for which a solver is registered."""
        return set(self._solvers.keys())

    def parts(self, day: int) -> Set[int]:
        """Return a set of all part numbers of the given `day` for which a solver is registered."""
        return set(self._solvers[day].keys())

    def solver(self, day: int, part: int) -> Callable[[Callable[[str], Any]], Callable[[str], None]]:
        def decorate_solver(solve: Callable[[str], Any]) -> Callable[[str], None]:
            """Add the `solve` function as a solver for the given `day` and `part`."""
            def decorated_solve(data: str):
                result = solve(data)
                if result is not None:
                    print(result)

            if day in self._solvers:
                if part in self._solvers[day]:
                    print(f"WARNING: Solver for day {day} part {part} implemented multiple times!")
                self._solvers[day][part] = decorated_solve
            else:
                self._solvers[day] = { part: decorated_solve }

            return decorated_solve

        return decorate_solver
   
    def solve(self, day: int, part: int, data: str) -> bool:
        """Solve the given `day` and `part` using `data` as input.
        Return whether that combination was implemented."""
        if day not in self.days() or part not in self.parts(day):
            return False
        self._solvers[day][part](data)
        return True
