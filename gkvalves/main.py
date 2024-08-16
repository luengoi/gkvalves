import argparse
import sys

from gkvalves import Valves, VERSION


def make_parser(valves: Valves) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gorod Krovi valve step solver.")
    parser.add_argument(
        "--version",
        action="store_true",
        help="show version number and exit",
        dest="version"
    )

    subparsers = parser.add_subparsers()
    list_cmd = subparsers.add_parser("list", aliases=["l"], help=_list.__doc__)
    list_cmd.set_defaults(func=_list)

    solve_cmd = subparsers.add_parser("solve", aliases=["s"], help=_solve.__doc__)
    solve_cmd.add_argument(
        "green",
        type=int,
        help="the location of the green-lit valve",
        choices=list(range(len(valves)))
    )
    solve_cmd.add_argument(
        "cylinder",
        type=int,
        help="the location of the valve with the cylinder",
        choices=list(range(len(valves)))
    )
    solve_cmd.set_defaults(func=_solve)
    return parser


def _list(_: argparse.Namespace, valves: Valves) -> None:
    """
    list the available valve locations
    """
    for location in sorted(valves.locations, key=lambda l: l.id):
        print(f"({location.id}) {location.name}")


def _solve(args: argparse.Namespace, valves: Valves) -> None:
    """
    find the configuration to connect all the valves
    """
    if args.green == args.cylinder:
        print("[ERROR] green-lit valve and cylinder cannot be at the same location.")
        sys.exit(1)

    try:
        green = valves[args.green]
        cylinder = valves[args.cylinder]
    except KeyError as ex:
        print(f"[ERROR] {ex}, use the 'list' command to list available locations.")
        sys.exit(1)

    if path := valves.solve(green, cylinder):
        for valve, conf in sorted(path.items(), key=lambda x: x[0].location.id):
            print(f"{valve.location.name}: {conf if conf is not None else "This is the ending valve."}")
    else:
        print(f"[ERROR] No path found for {green} -> {cylinder}")


def main() -> None:
    valves = Valves()
    parser = make_parser(valves)
    args = parser.parse_args()

    if args.version:
        print(VERSION)
    elif func := getattr(args, "func", None):
        func(args, valves)
    else:
        parser.print_help()
