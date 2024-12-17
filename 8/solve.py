#!/usr/bin/env python3

import numpy as np
from itertools import combinations


def solve(board):
    antennas = set(np.unique(board))
    antennas.remove(".")
    antinodes = set()

    for antenna in antennas:
        for src, dst in combinations(np.argwhere(board == antenna), r=2):
            antinodes |= get_harmonics(board, src, dst)

    return len(antinodes)


def get_harmonics(board, src, dst):
    delta = src - dst
    harmonics = set()

    next_coord = dst.copy() - delta
    if next_coord[0] in range(board.shape[0]) and next_coord[1] in range(
        board.shape[1]
    ):
        harmonics.add(tuple(next_coord))

    next_coord = src.copy() + delta
    if next_coord[0] in range(board.shape[0]) and next_coord[1] in range(
        board.shape[1]
    ):
        harmonics.add(tuple(next_coord))

    return harmonics


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(list(line.strip()))

    return np.array(parsed)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 14)
    main("input.txt")
