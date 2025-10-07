import collections
import shared.constants
import enum
import operator

class Direction(enum.Enum):
    N = 0
    E = 1
    S = 2
    W = 3

class InArea(enum.Enum):
    INSIDE = 1
    OUTSIDE = 0
    STALLED = -1

SPACE = 0
VISITED = 1
BARRIER = -1

def rotate(heading: Direction) -> Direction:
    if heading == Direction.N: return Direction.E
    if heading == Direction.E: return Direction.S
    if heading == Direction.S: return Direction.W
    if heading == Direction.W: return Direction.N

def comparison_idx(heading: Direction, row, col) -> int:
    if heading == Direction.N or heading == Direction.S:
        return col, row, 0, 1
    else: return row, col, 1, 0

def comparison_fn_and_operation(heading: Direction) -> callable:
    if heading == Direction.N or heading == Direction.W:
        return min, operator.lt
    else:
        return max, operator.gt

def is_barrier(area: list[int, list[int]], pos: tuple[int, int]):
    return area[pos[0]][pos[1]] == BARRIER

def is_outside(area: list[int, list[int]], pos: tuple[int, int]):
    return not(0 <= pos[0] < len(area) and 0 <= pos[1] < len(area[0]))

def next_valid(area: list[int, list[int]], pos: tuple[int, int], heading: Direction) -> tuple[InArea, tuple[tuple[int, int], Direction]]:
    rotation = 0
    while rotation < 4:
        if heading == Direction.N:
            next_pos = (pos[0]-1, pos[1])
        elif heading == Direction.E:
            next_pos = (pos[0], pos[1]+1)
        elif heading == Direction.S:
            next_pos = (pos[0]+1, pos[1])
        elif heading == Direction.W:
            next_pos = (pos[0], pos[1]-1)

        if is_outside(area, next_pos):
            return (InArea.OUTSIDE, (next_pos, heading))
        elif is_barrier(area, next_pos):
            heading = rotate(heading)
            rotation += 1
        else:
            return (InArea.INSIDE, (next_pos, heading))
    
    if rotation == 4:
        return (InArea.STALLED, (next_pos, heading))




def solve():
    total = 0
    with open('day_6/' + shared.constants.INPUT_PATH + "_test", 'r') as f:
        lines = f.readlines()
    
    area = []
    direction_row: dict[Direction, set[int]] = {d: set() for d in Direction}
    direction_col: dict[Direction, set[int]] = {d: set() for d in Direction}
    guard = None
    for i, line in enumerate(lines):
        line = list(line)
        area_line = []
        for j, l in enumerate(line):
            if l == '^':
                guard = (i, j)
                area_line.append(SPACE)
            elif l == '.':
                area_line.append(SPACE)
            elif l == '#':
                area_line.append(BARRIER)
        area.append(area_line[::])
    
    print(f"Boundaries rows {len(area)}, cols {len(area[0])}")
    if guard is None:
        print("Invalid input")
        return
    
    heading = Direction.N
    status = InArea.INSIDE
    while status == InArea.INSIDE:

        area[guard[0]][guard[1]] = 1
        # check for possibility of loop
        # if we turn 90deg to the right + if we
        candidate_heading = rotate(heading)

        comp_fn, comp_op = comparison_fn_and_operation(candidate_heading)
        comparision_data, other_comp_data, comp_idx, fixed_idx = comparison_idx(candidate_heading, direction_row, direction_col)
        try:
            if (comp_op(comp_fn(comparision_data[candidate_heading]), guard[comp_idx])) and guard[fixed_idx] in other_comp_data[candidate_heading]:
                print(guard, heading, candidate_heading)
                total += 1
        except ValueError:
            pass

        direction_row[heading].add(guard[0])
        direction_col[heading].add(guard[1])
        print("row", direction_row)
        print("col", direction_col)


        status, (next_pos, heading) = next_valid(area, guard, heading)
        guard = next_pos
    
    # for row in area:
    #     print(row)
    #     for col in row:
    #         if col == VISITED:
    #             total += 1
    
    print(total)

# def solve_2():



if __name__ == '__main__':
    solve()
