def file_lines(filepath: str) -> list[str]:
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return lines