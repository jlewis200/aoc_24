#!/usr/bin/env python3

import numpy as np
from collections import defaultdict


def solve(numbers):
    """
    Return max sale price across all sequence tuples.
    """
    numbers = get_numbers(numbers) % 10
    return max(get_sequence_sums(get_sequence_values(numbers)))


def get_sequence_sums(sequence_values):
    """
    Sum the monkey sale prices across all sequence tuples.
    """
    sequence_sums = []

    for counts in sequence_values.values():
        sequence_sums.append(sum(counts.values()))

    return sequence_sums


def get_sequence_values(numbers):
    """
    Construct a dict mapping 4-tuple sequences to per-monkey sale prices.

    schema:
        {
            (0, 1, 2, 3): {
                monkey_0: sale_price_0,
                monkey_1: sale_price_1,
                ...
            },
            (1, 2, 3, 4): {
                monkey_0: sale_price_0,
                monkey_1: sale_price_1,
                ...
            },
            ...
        }

    Only the first sale price per sequenc-tuple/monkey combination is recorded.
    """
    deltas = numbers[1:] - numbers[:-1]
    sequence_values = defaultdict(lambda: {})

    for idx, chunk in enumerate(
        np.lib.stride_tricks.sliding_window_view(deltas, 4, axis=0),
        start=4,
    ):
        for jdx, row in enumerate(chunk):
            sequence = tuple(row)

            if jdx not in sequence_values[sequence]:
                sequence_values[sequence][jdx] = numbers[idx, jdx]

    return sequence_values


def get_numbers(numbers):
    for _ in range(2000):
        next_numbers = []

        for number in numbers[-1]:
            number ^= number * 64
            number %= 16777216

            number ^= number // 32
            number %= 16777216

            number ^= number * 2048
            number %= 16777216

            next_numbers.append(number)

        numbers.append(next_numbers)

    return np.array(numbers)


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(map(str, row)) for row in board)


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(int(line))

    return [parsed]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_1.txt", 23)
    main("input.txt")
