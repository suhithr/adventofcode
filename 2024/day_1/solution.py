import shared.constants as constants
import shared.file_helpers as file_helpers

def solve(as_test: bool = False):
    if not as_test:
        lines: list[str] = file_helpers.file_lines("day_1/" + constants.INPUT_PATH)
    else:
        lines = ["2991712887533295256"]
    total = 0
    print(f"Number of lines is {len(lines)}")
    for line in lines:
        clean_str = "".join(line.split())
        # for each index in the string, incl the last one
        for idx in range(len(clean_str)):
            if idx == len(clean_str)-1 and idx > 0: # last character
                total += int(clean_str[0]) if clean_str[0] == line[idx] else 0
            else:
                total += int(clean_str[idx]) if clean_str[idx] == clean_str[idx+1] else 0
    
    return total

def solve_2(as_test: bool = False):
    if not as_test:
        lines: list[str] = file_helpers.file_lines("day_1/" + constants.INPUT_PATH)
    else:
        lines = ["12131415"]
    total = 0
    print(f"Number of lines is {len(lines)}")
    for line in lines:
        clean_str = "".join(line.split())

        offset: int = int(len(clean_str)/2)

        # for each index in the string, incl the last one
        for idx in range(len(clean_str)):
            if idx >= offset: # last character
                # print(clean_str[idx], clean_str[offset - (len(clean_str)- 1 - idx)-1 ])
                total += int(clean_str[idx]) if clean_str[idx] == clean_str[offset - (len(clean_str)- 1 - idx)-1 ] else 0
            else:
                total += int(clean_str[idx]) if clean_str[idx] == clean_str[idx+offset] else 0
    
    return total


if __name__ == '__main__':
    print(solve_2(as_test=True))
    print(solve_2(as_test=False))