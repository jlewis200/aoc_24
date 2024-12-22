#!/usr/bin/env python3


def solve(numbers):
    return sum(get_numbers(numbers))


def get_numbers(numbers):
    for _ in range(2000):
        next_numbers = []

        for number in numbers:
            number ^= number * 64
            number %= 16777216

            number ^= number // 32
            number %= 16777216

            number ^= number * 2048
            number %= 16777216

            next_numbers.append(number)

        numbers = next_numbers

    return numbers


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(int(line))

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 37327623)
    main("input.txt")
