

def delete_lines_that_contains_string_from_filepath(filepath, string) -> list:
    """
    Function goes through the file and deletes lines that contains string
    :
    :return: list of new lines
    """
    with open(filepath, 'r') as f:
        old_lines = f.readlines()

    new_lines = []
    for line in old_lines:
        if string not in line:
            new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

    return new_lines
