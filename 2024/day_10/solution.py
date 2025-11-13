import shared.constants
import collections
from dataclasses import dataclass

TRAIL_START = 0
TRAIL_END = 9

def neighbors(cur_row: int, cur_col: int, max_row: int, max_col: int) -> list[tuple[int, int]]:
    nbrs = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = cur_row + dx, cur_col+dy
        if 0 <= new_row <= max_row and 0 <= new_col <= max_col:
            nbrs.append((new_row, new_col))
    return nbrs

def process_input() -> list[list[int]]:
    # with open('day_10/' + shared.constants.INPUT_PATH + '_test', 'r') as f:
    with open('day_10/' + shared.constants.INPUT_PATH, 'r') as f:
        lines = f.read().splitlines()
    parsed_graph: list[list[int]] = []
    for l in lines:
        parsed_graph.append(list(map(int, l)))
    return parsed_graph

def compute_score(start_row: int, start_col: int, graph: list[list[int]]) -> int:
    assert 0 <= start_row < len(graph)
    assert len(graph) > 0
    assert 0 <= start_col < len(graph[0])
    max_row, max_col = len(graph)-1, len(graph[0])-1

    trail_count = 0 # how many 9's do we see

    # BFS along trail ensuring uphill
    qu = collections.deque()
    qu.append((start_row, start_col, graph[start_row][start_col]))
    visited: set[tuple[int, int]] = set()
    while qu:
        row, col, height = qu.popleft()

        # never visit same spot twice, if it's a new 9, incr trail_count
        if (row, col) not in visited:
            visited.add((row, col))
            if height == TRAIL_END:
                trail_count += 1
            else:
                # add valid neighbors to qu
                for new_row, new_col in neighbors(row, col, max_row, max_col):
                    if graph[new_row][new_col] == height+1:
                        qu.append((new_row, new_col, height+1))
    
    return trail_count

def compute_score_distinct_trails(start_row: int, start_col: int, graph: list[list[int]]) -> int:
    assert 0 <= start_row < len(graph)
    assert len(graph) > 0
    assert 0 <= start_col < len(graph[0])
    max_row, max_col = len(graph)-1, len(graph[0])-1
    
    distinct_trail_count = [0]
    def depth_first_traversal(row: int, col: int, visited_path: set, distinct_trail_count: list[int]):
        curr_height = graph[row][col]
        if curr_height == 9:
            distinct_trail_count[0] += 1
        else:
            for new_row, new_col in neighbors(row, col, max_row, max_col):
                if graph[new_row][new_col] == curr_height+1:
                    visited_path.add((new_row, new_col))
                    depth_first_traversal(new_row, new_col, visited_path, distinct_trail_count)
                    visited_path.remove((new_row, new_col))
    
    depth_first_traversal(start_row, start_col, set([(start_row, start_col)]), distinct_trail_count)
    return distinct_trail_count[0]

def solve_part_2() -> int:
    graph: list[list[int]] = process_input()
    score = 0
    for row, values in enumerate(graph):
        for col, height in enumerate(values):
            if height == TRAIL_START:
                score += compute_score_distinct_trails(row, col, graph)
    
    return score

        

def solve() -> int:
    graph: list[list[int]] = process_input()

    score = 0
    for row, values in enumerate(graph):
        for col, height in enumerate(values):
            if height == TRAIL_START:
                score += compute_score(row, col, graph)
    
    return score

if __name__ == '__main__':
    print(solve_part_2())