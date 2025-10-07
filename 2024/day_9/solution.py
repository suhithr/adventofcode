import shared.file_helpers as file_helpers
from dataclasses import dataclass

@dataclass
class file:
    id: int
    size: int


@dataclass
class block:
    # (0, 1) f(2) -> (0, 1), (2, 2) f(0) = 0*0 + 1*0 + 2*2 + 3*2
    # (1, 3) f(4) -> (1, 3), (2, 3) f(1) = + 4*1 + 5*1 + 6*1 + 7*2 + 8*2 + 9*2
    # (2, 5) f(0) -> (0, 0) f(0)
    files: list[file]
    free_space: int

def generate_blocks(input: list[int]) -> list[block]:
    res = []
    if len(input) % 2: input.append(0) # edge case of odd nums
    file_id = 0
    for i in range(0, len(input), 2):
        res.append(
            block(files=[file(file_id, input[i])], free_space=input[i+1])
        )
        file_id  += 1
    return res

def compaction_process(blocks: list[block]) -> list[block]:
    i, j  = 0, len(blocks)-1
    while i < j:
        left, right = blocks[i], blocks[j]
        movement = min(left.free_space, right.files[0].size)
        if movement > 0:
            left.files.append(file(right.files[0].id, movement))
        left.free_space -= movement
        right.files[0].size -= movement

        if left.free_space == 0:
            i += 1
        if right.files[0].size == 0:
            j -= 1
    return blocks

def sum_natural_nums(n: int) -> int:
    return (n * (n+1))/2

def get_checksum(blocks: list[block]) -> int:
    loc = 0
    total = 0
    for block in blocks:
        for file in block.files:
            while file.size > 0:
                total += file.id * loc
                file.size -= 1
                loc += 1
        loc += block.free_space
    return total

def compaction_process_2(blocks: list[block]) -> list[block]:
    j = len(blocks)-1
    while j > 0:
        i = 0
        right = blocks[j]
        while blocks[i].free_space < right.files[0].size and i < j:
            i += 1
        if i < j and blocks[i].free_space >= right.files[0].size:
            # Our new
            blocks[i].files.append(right.files[0])
            # if len(right.files) == 1:
            #     right.free_space += right.files[0].size
            right.files[0] = file(id=0, size=right.files[0].size)
            
            blocks[i].free_space -= right.files[0].size
        j -= 1
    return blocks

def solution(input_path: str) -> int:
    lines: list[str] = file_helpers.file_lines(input_path)
    assert len(lines) == 1
    input = list(map(int, lines[0].strip()))

    blocks = generate_blocks(input)
    blocks = compaction_process(blocks)

    result: int = get_checksum(blocks)
    print(result)
    return result
    
def solution_part_2(input_path: str) -> int:
    lines: list[str] = file_helpers.file_lines(input_path)
    assert len(lines) == 1
    input = list(map(int, lines[0].strip()))

    blocks = generate_blocks(input)
    blocks = compaction_process_2(blocks)
    # for b in blocks:
    #     print(b)
    
    result: int = get_checksum(blocks)
    print(result)
    return result


if __name__ == '__main__':
    solution_part_2(input_path="day_9/input")