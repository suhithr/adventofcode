import shared.constants
from dataclasses import dataclass

@dataclass
class Equation:
    test_result: int
    numbers: list[int]

def process_input() -> list[Equation]:
    # with open('day_7/' + shared.constants.INPUT_PATH + '_test', 'r') as f:
    with open('day_7/' + shared.constants.INPUT_PATH, 'r') as f:
        lines = f.read().splitlines() # doesn't read the \n in newlines
    equations: list[Equation] = []
    for l in lines:
        tr, rest = l.split(":")
        tr = int(tr)
        nums: list[int] = list(map(int, rest[1:].split(" ")))
        equations.append(Equation(test_result=tr, numbers=nums))
    return equations

def concatenation(left: int, right: int) -> int:
    return int(str(left) + str(right))

def backtrack(candidate_result: int, desired_result: int, current_num: int, remaining_num: list[int]) -> bool:
    # print(candidate_result, current_num, remaining_num)
    if candidate_result == desired_result and current_num == None:
        return True
    if candidate_result > desired_result or current_num == None:
        return False
    
    next_num = None if len(remaining_num) == 0 else remaining_num[0]
    return backtrack(candidate_result * current_num, desired_result, next_num, remaining_num[1:]) or \
        backtrack(candidate_result + current_num, desired_result, next_num, remaining_num[1:]) or \
        backtrack(concatenation(candidate_result ,current_num), desired_result, next_num, remaining_num[1:])


def is_valid(eqn: Equation) -> bool:

    goal = eqn.test_result
    assert len(eqn.numbers) >= 2
    candidate_result = eqn.numbers[0]
    current_num: int = eqn.numbers[1]

    remaining_num = [None] if len(eqn.numbers) < 3 else eqn.numbers[2:]

    return backtrack(candidate_result * current_num, goal, remaining_num[0], remaining_num[1:]) or \
        backtrack(candidate_result + current_num, goal, remaining_num[0], remaining_num[1:]) or \
        backtrack(concatenation(candidate_result, current_num), goal, remaining_num[0], remaining_num[1:])


def solve():
    equations = process_input()
    calibration_result = 0
    for eq in equations:
        if is_valid(eq):
            # print(eq.test_result)
            calibration_result += eq.test_result
    
    return calibration_result

if __name__ == '__main__':
    print(solve())