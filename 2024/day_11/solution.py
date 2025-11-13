import shared.constants

def process_input() -> list[int]:
    # with open("day_11/" + shared.constants.INPUT_PATH, 'r') as f:
    with open("day_11/" + shared.constants.INPUT_PATH + "_test", 'r') as f:
        line = f.read()

    return list(map(int, line.split(" ")))

def run_blinks_via_graph(stones: list[int], blink_count: int = 6) -> int:
    stone_count: int = 0 # at the finall number of blinks only
    for stone in stones:
        stack: list[tuple[int, int]] = [(stone, 0)]

        while stack:
            top_stone, depth = stack.pop()
            if depth == blink_count:
                stone_count += 1
            elif top_stone == 0:
                stack.append((1, depth+1))
            elif len(str(top_stone)) % 2 == 0:
                str_top_stone = str(top_stone)
                num_digits = len(str_top_stone)
                stack.append((int(str_top_stone[:num_digits//2]), depth+1))
                stack.append((int(str_top_stone[num_digits//2:]), depth+1))
            else:
                stack.append((top_stone * 2024, depth+1))
    
    return stone_count


def simulate_blinks(stones: list[int], blink_count: int = 6) -> int:
    # look
    for _ in range(blink_count):
        post_blink: list[int] = []
        for stone in stones:
            if stone == 0:
                post_blink.append(1)
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                num_digits = len(str_stone)
                post_blink.append(int(str_stone[:num_digits//2]))
                post_blink.append(int(str_stone[num_digits//2:]))
            else:
                post_blink.append(stone * 2024)
        stones = post_blink
    
    return len(stones)

if __name__ == '__main__':
    # print(simulate_blinks(stones=process_input(), blink_count=75))
    print(run_blinks_via_graph(stones=process_input(), blink_count=75))
