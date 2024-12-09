#!/usr/bin/env python3


def solve(data):
    idx = next_freespace(data, 0)

    while idx < len(data):
        item = data.pop(-1)

        if item != -1:
            data[idx] = item

        idx = next_freespace(data, idx)

    return get_checksum(data)


def next_freespace(data, idx):
    while idx < len(data) and data[idx] != -1:
        idx += 1

    return idx


def get_checksum(data):
    checksum = 0

    for idx, value in enumerate(data):
        checksum += idx * value

    return checksum


def parse(line):
    line = list(line.strip())
    parsed = []

    for data, idx in enumerate(range(0, len(line), 2)):
        parsed += [data] * int(line[idx])
        try:
            parsed += [-1] * int(line[idx + 1])
        except:
            pass

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 1928)
    main("input.txt")
