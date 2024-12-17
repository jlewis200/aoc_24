#!/usr/bin/env python3


def solve(data):
    breakpoint()


def parse(lines):
    parsed = []

    for line in line:
        # do something more useful here
        parsed.append(line)

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
    main("test_0.txt", None)
    main("input.txt")
