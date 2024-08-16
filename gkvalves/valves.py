import dataclasses
import typing


class Location(typing.NamedTuple):
    """
    Location of a valve in the map.
    """
    id: int
    name: str

    def __repr__(self) -> str:
        return f"{self.name} (id: {self.id})"


@dataclasses.dataclass
class Valve:
    """
    Description of a valve.
    """
    location: Location
    connections: tuple["Valve", "Valve", "Valve"]

    def __hash__(self) -> int:
        return self.location.id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Valve):
            raise NotImplemented()
        return self.location == other.location


class Valves:
    """
    Collection of the valves.
    """
    _valves: tuple[Valve, ...]

    def __init__(self) -> None:
        self._valves = (
            Valve(Location(0, "Armory"), tuple()),
            Valve(Location(1, "Department Store"), tuple()),
            Valve(Location(2, "Dragon Command"), tuple()),
            Valve(Location(3, "Supply Depot"), tuple()),
            Valve(Location(4, "Infirmary"), tuple()),
            Valve(Location(5, "Tank Factory"), tuple())
        )

        self._valves[0].connections = (self._valves[3], self._valves[5], self._valves[1])
        self._valves[1].connections = (self._valves[0], self._valves[4], self._valves[2])
        self._valves[2].connections = (self._valves[3], self._valves[1], self._valves[4])
        self._valves[3].connections = (self._valves[2], self._valves[0], self._valves[5])
        self._valves[4].connections = (self._valves[1], self._valves[5], self._valves[2])
        self._valves[5].connections = (self._valves[4], self._valves[3], self._valves[0])

    @property
    def locations(self) -> list[Location]:
        return [valve.location for valve in self._valves]

    def solve(self, start: Valve, end: Valve) -> dict[Valve, int | None] | None:
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
        visited: set[Valve] = set([start])

        def dfs(valve: Valve, count: int) -> dict[Valve, int | None] | None:
            if valve == end:
                return {valve: None} if count == len(self._valves) else None

            for i, connection in ((i, c) for (i, c) in enumerate(valve.connections) if c not in visited):
                visited.add(connection)
                if partial := dfs(connection, count + 1):
                    # Connections are 1-indexed in the game.
                    return partial | {valve: i + 1}
                visited.remove(connection)

            return {}

        return dfs(start, 1)

    def __getitem__(self, key: Location | int | str) -> Valve:
        if isinstance(key, int):
            if valve := next((v for v in self._valves if v.location.id == key)):
                return valve
            else:
                raise KeyError(f"Invalid location id: {key}")

        if isinstance(key, str):
            if valve := next((v for v in self._valves if v.location.name == key)):
                return valve
            else:
                raise KeyError(f"Invalid location name: {key}")

        if isinstance(key, Location):
            if valve := next((v for v in self._valves if v.location == key)):
                return valve
            else:
                raise KeyError(f"Invalid location: {key}")

    def __iter__(self) -> typing.Generator[Valve, None, None]:
        for valve in self._valves:
            yield valve

    def __len__(self) -> int:
        return len(self._valves)

    def __del__(self) -> None:
        # Get rid of the reference cycles.
        for valve in self._valves:
            valve.connections = tuple()
