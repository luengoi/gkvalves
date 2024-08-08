import argparse

from . import VALVES, solve

def main() -> int:
    parser = argparse.ArgumentParser(
        prog='gksolver',
        description='Gorod Krovi valve step solver',
        epilog=f'{' '.join(map(lambda v: f'({v.id}) {v.name}', VALVES))}'
    )
    parser.add_argument('green', type=int, help='the location of the green valve')
    parser.add_argument('cylinder', type=int, help='the location of the valve with the cylinder')
    args = parser.parse_args()

    if not 0 <= args.green < len(VALVES) or not 0 <= args.cylinder < len(VALVES):
        print('ERROR: Invalid valve location, use -h argument to see valid locations')
        return -1

    green = VALVES[args.green]
    cylinder = VALVES[args.cylinder]
    path = solve(green, cylinder)

    if green == cylinder:
        print('ERROR: green valve and cylinder cannot be at the same location.')
        return -2

    if not path:
        print(f'No path found for {green.name} -> {cylinder.name}')
        return -3

    for valve, connection in path[:-1]:
        print(f'{valve.name}: {connection + 1}')

    return 0


if __name__ == '__main__':
    exit(main())
