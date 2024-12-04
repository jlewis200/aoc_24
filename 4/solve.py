#!/usr/bin/env python3

import re
import math
import numpy as np
import networkx as nx


def solve(board):
    count = 0

    for permutation in permuter(board):
        print(permutation)
        count += len(re.findall("XMAS", permutation))
        count += len(re.findall("SAMX", permutation))

    return count

def permuter(board):
    for row in board:
        yield "".join(element for element in row)

    for idx in range(board.shape[1]):
        yield "".join(element for element in board[:, idx])
        
    for idx in range(-board.shape[1], board.shape[1]):
        yield "".join(element for element in np.diagonal(board, idx))

    for idx in range(-board.shape[1], board.shape[1]):
        yield "".join(element for element in np.diagonal(np.rot90(board), idx))


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
    main("test_0.txt", 18)
    main("input.txt")
