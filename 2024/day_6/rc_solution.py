import pathlib
import sys

# N, E, S, W
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def parse(puzzle_input):
    return [list(line) for line in puzzle_input.split("\n")]


def find_guard_with_heading(grid):
    h = len(grid)
    for x in range(h):
        row = grid[x]
        if row.count('^') > 0:
            return x, row.index('^'), len(grid), len(row), 0

def visited_cells(grid):
    visited = set()
    x, y, num_rows, num_cols, d = find_guard_with_heading(grid)
    while True:
        visited.add((x, y))
        dx, dy = dirs[d]
        xx = x + dx
        yy = y + dy
        if xx < 0 or xx >= num_rows or yy < 0 or yy >= num_cols:
            return visited
        if grid[xx][yy] == '#':
            d = (d+1) % 4
        else:
            x = xx
            y = yy

def has_cycle(grid):
    visited = set()
    x, y, num_rows, num_cols, d = find_guard_with_heading(grid)
    while True:
        if (x, y, d) in visited:
            return True
        visited.add((x, y, d))
        dx, dy = dirs[d]
        xx = x + dx
        yy = y + dy
        if xx < 0 or xx >= num_rows or yy < 0 or yy >= num_cols:
            return False
        if grid[xx][yy] == '#':
            d = (d+1)%4
        else:
            x = xx
            y = yy


"""
Solution Explanation:
1. Run through the entire visited locations of the guard. Mark them all into the visited column
2. Now for each visited cell, replace the visited cell with a barrier, then check if a cycle exists
    a. Cycle detection:
        Takes place by starting from the guard, traveling as normal (in the new grid with the extra barrier)
        Check for double visits (include direction in the set as overlapping is not enough solo).
"""

def part2(grid):
    visited = visited_cells(grid)
    z = 0
    for x, y in visited:
        if grid[x][y] == '.':
            grid[x][y] = '#'
            if has_cycle(grid):
                z += 1
            grid[x][y] = '.'
    return z

if __name__ == '__main__':
    puzzle_input = pathlib.Path("day_6/input").read_text().strip()
    print(part2(parse(puzzle_input)))
