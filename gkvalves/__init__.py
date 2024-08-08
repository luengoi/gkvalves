from typing import List, NamedTuple, Optional, Set, Tuple

__all__ = ['Valve', 'VALVES', 'solve']

class Valve(NamedTuple):
    id: int
    name: str
    connections: List[int]

    def __str__(self) -> str:
        return self.name


VALVES = [
    Valve(0, 'Armory', [3, 5, 1]),
    Valve(1, 'Dept. Store', [0, 4, 2]),
    Valve(2, 'Dragon Command', [3, 1, 4]),
    Valve(3, 'Supply Depot', [2, 0, 5]),
    Valve(4, 'Infirmary', [1, 5, 2]),
    Valve(5, 'Tank Factory', [4, 3, 0])
]

def solve(start: Valve, end: Valve) -> Optional[List[Tuple[Valve, int]]]:
    '''
    For this particular case, a Hamiltonian Path is guaranteed to exist. Since
    we know the start and end vertices, we can use a simple DFS algorithm and
    brute-force all the possible combinations until we find a good one.

    Finding Hamiltonian Paths is an NP-complete problem. Since our problem space
    is considerable small (only 6 valves), the brute-force solution finds a valid
    solution fairly quickly.

    There is improvement potential using Dynamic Programming. But, for this
    particular case, the added complexity is not worth the speed improvement.
    '''
    visited: Set[int] = set([start.id])

    def dfs(valve: Valve, count: int) -> Optional[List[Tuple[Valve, int]]]:
        if valve == end:
            return [(valve, -1)] if count == len(VALVES) else None

        for i, connection in ((i, c) for (i, c) in enumerate(valve.connections) if c not in visited):
            visited.add(connection)
            if path := dfs(VALVES[connection], count + 1):
                return [(valve, i)] + path
            visited.remove(connection)

        return []

    return dfs(start, 1)
