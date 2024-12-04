#!/usr/bin/env python3

import re
import math
import numpy as np
import networkx as nx


def solve(board):
    count = 0
    board_ = np.zeros_like(board, dtype=int)

    board_[board == "M"] = 1
    board_[board == "A"] = 10
    board_[board == "S"] = 100
    board = board_

    mask = np.array(
        [
            [1,  0, 100],
            [0, 10,   0],
            [1,  0, 100],
        ]
    )

    for y in range(board.shape[0] - 2):
        for x in range(board.shape[1] - 2):
            print(y, x)
            for mask in mask_permuter():
                res = board[y:y+3, x:x+3] * mask
                if res.sum() == 20102:
                    count += 1
        
    return count


def mask_permuter():
    yield np.array(
        [
            [1,  0, 100],
            [0, 10,   0],
            [1,  0, 100],
        ]
    )

    yield np.array(
        [
            [100,  0, 100],
            [0, 10,   0],
            [1,  0, 1],
        ]
    )

    yield np.array(
        [
            [1,  0, 1],
            [0, 10,   0],
            [100,  0, 100],
        ]
    )

    yield np.array(
        [
            [100,  0, 1],
            [0, 10,   0],
            [100,  0, 1],
        ]
    )

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
    main("test_0.txt", 9)
    main("input.txt")
