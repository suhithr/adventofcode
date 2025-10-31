import shared.constants
from dataclasses import  dataclass
import collections

"""
graph repr: 
bound: m, n
dict {symbol: list[locations]}


"""

EMPTY_SPACE = '.'

@dataclass(frozen=True)
class Location:
    x: int
    y: int

def process_input() -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    # with open('day_8/' + shared.constants.INPUT_PATH + '_test', 'r') as f:
    with open('day_8/' + shared.constants.INPUT_PATH, 'r') as f:
        lines = f.read().splitlines()
    
    assert len(lines) > 0
    assert len(lines[0]) > 0
    row_bound = len(lines)
    col_bound = len(lines[0])

    symbol_location: dict[str, list[tuple[int, int]]] = collections.defaultdict(list)
    
    for row, line in enumerate(lines):
        for col, element in enumerate(line):
            if element != EMPTY_SPACE:
                symbol_location[element].append(Location(row, col))
    
    return symbol_location, row_bound, col_bound

def generate_antinodes(first_loc: Location, second_loc: Location) -> tuple[Location, Location]:
    delta_x, delta_y = second_loc.x - first_loc.x, second_loc.y - first_loc.y
    
    # antinode must be delta_[x,y] distance from second_loc and -delta_[x,y] distance from first_loc
    return Location(second_loc.x+delta_x, second_loc.y+delta_y), Location(first_loc.x-delta_x, first_loc.y-delta_y)

def gcd(smaller, larger) -> int:
    # factorize delta_x and delta_y
    for f in range(smaller, 1, -1):
        if smaller % f == 0 and larger % f == 0:
            return f
    return 1

def generate_filtered_expanded_antinodes(first_loc: Location, second_loc: Location, row_bound, col_bound) -> list[Location]:
    delta_x, delta_y = second_loc.x - first_loc.x, second_loc.y - first_loc.y
    factor = gcd(min(delta_x, delta_y), max(delta_x, delta_y))
    reduced_x, reduced_y = delta_x / factor, delta_y / factor
    valid_antinodes = {(first_loc.x, first_loc.y), (second_loc.x, second_loc.y)}

    # moving from the first node in both directions we test candidate coordinates cx, cy
    for multiplier in [1, -1]:
        reduced_x *= multiplier
        reduced_y *= multiplier
        cx, cy = first_loc.x + reduced_x, first_loc.y + reduced_y
        while 0 <= cx < row_bound and 0 <= cy < col_bound:
            valid_antinodes.add((cx, cy))
            cx += reduced_x
            cy += reduced_y
    
    return valid_antinodes


def filter_valid_antinodes(antinodes: list[Location], max_row_bound: int, max_col_bound: int) -> list[Location]:
    result = []
    for an in antinodes:
        if 0 <= an.x < max_row_bound and 0 <= an.y < max_col_bound:
            result.append(an)
    return result

def solve_part_two() -> int:
    symbol_location, row_bound, col_bound = process_input()
    all_antinodes = set()

    for symbol, locations in symbol_location.items():
        # Computing antinodes for every unique symbol pair in locations
        # print(f"Symbol: {symbol}")
        for i in range(len(locations)):
            first_loc = locations[i]
            for j in range(i+1, len(locations)):
                second_loc = locations[j]
                for antinode in generate_filtered_expanded_antinodes(first_loc, second_loc, row_bound, col_bound):
                    # print(antinode)
                    all_antinodes.add(antinode)
    
    # print(all_antinodes)
    return len(all_antinodes)

def solve() -> int:
    symbol_location, row_bound, col_bound = process_input()
    all_antinodes = set()

    for symbol, locations in symbol_location.items():
        # Computing antinodes for every unique symbol pair in locations
        # print(f"Symbol: {symbol}")
        for i in range(len(locations)):
            first_loc = locations[i]
            for j in range(i+1, len(locations)):
                second_loc = locations[j]
                for antinode in filter_valid_antinodes(generate_antinodes(first_loc, second_loc), row_bound, col_bound):
                    # print(antinode)
                    all_antinodes.add(antinode)
    
    # print(all_antinodes)
    return len(all_antinodes)

        


if __name__ == '__main__':
    print(solve_part_two())