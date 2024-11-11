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
    for i in range(len(lines)):
        try:
            if lines[i].startswith("246") and lines[i + 1].startswith("Nominal"):
                lines[i] = lines[i] + ' ' + lines[i + 1]  # merge lines i and i+1
                del lines[i + 1]
        except IndexError:
            break

    for i in range(0, len(lines), 2):
        result_dict[f"{' '.join(lines[i].split()[1:])}"] = lines[i + 1].split()[0]

    if verbose:
        print(result_dict)

    return result_dict
