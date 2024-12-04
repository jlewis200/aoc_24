#!/usr/bin/env python3

import re
import math
import numpy as np
import networkx as nx


def solve(board):
    """
    Map M, A, S to 1, 10, 100.  Perform a 2-d convolution with every rotation
    of the mask.  Increment if the sum of pointwise multiplication matches the
    expected value.
    """
    count = 0
    board_ = np.zeros_like(board, dtype=int)

    board_[board == "M"] = 1
    board_[board == "A"] = 10
    board_[board == "S"] = 100
    board = board_

    for y in range(board.shape[0] - 2):

        for x in range(board.shape[1] - 2):

            for mask in mask_permuter():

                res = board[y : y + 3, x : x + 3] * mask
                if res.sum() == (mask**2).sum():
                    count += 1

    return count


def mask_permuter():
    mask = np.array(
        [
            [1, 0, 100],
            [0, 10, 0],
            [1, 0, 100],
        ]
    )

    for _ in range(4):
        mask = np.rot90(mask)
        yield mask


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
    main("test_0.txt", 9)
    main("input.txt")
