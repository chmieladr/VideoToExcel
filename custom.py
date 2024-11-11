import datetime

timestamp = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time(0, 0, 0))


def measures(text: str, verbose: bool = False) -> dict:
    global timestamp
    last_state_index = text.rfind("State:")  # extract only the text after the last "State:"
    if last_state_index == -1:
        return {}
    text = text[last_state_index + len("State:"):].strip()

    result_dict = {"Time": timestamp}
    timestamp += datetime.timedelta(seconds=1)

    lines = [line for line in text.splitlines() if line]  # remove empty lines
    lines[10] = lines[10] + ' ' + lines[11]  # merge lines 10 and 11
    del lines[11]

    for i in range(0, len(lines), 2):
        result_dict[f"{' '.join(lines[i].split()[1:])}"] = lines[i + 1].split()[0]

    if verbose:
        print(result_dict)

    return result_dict
