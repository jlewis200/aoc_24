#!/usr/bin/env python3

import numpy as np
from collections import deque, defaultdict
from dataclasses import dataclass
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str, parse


@dataclass
class Step:
    src: VectorTuple
    dst: VectorTuple
    cost: int
    step: int


def solve(board):
    start = VectorTuple(*np.argwhere(board == "S"))
    end = VectorTuple(*np.argwhere(board == "E"))
    steps = get_steps(board, start)
    coord_set = get_coord_set(steps, end)
    print_board(board, coord_set)
    return len(coord_set)


def get_steps(board, src):
    steps = defaultdict(lambda: [])
    costs = defaultdict(lambda: 2**32, {(src, VectorTuple(0, 1)): 0})
    queue = deque([(src, VectorTuple(0, 1), 0)])
    step = 0

    while len(queue) > 0:
        src, delta, step = queue.popleft()

        for dst in src.orthogonals(board):
            if board[dst] == "#":
                continue

            next_delta = dst - src
            cost = costs[(src, delta)] + (1 if next_delta == delta else 1000)

            if costs[(dst, next_delta)] > cost:
                costs[(dst, next_delta)] = cost
                queue.append((dst, next_delta, step + 1))
                steps[dst].append(
                    Step(
                        src,
                        dst,
                        cost,
                        step + 1,
                    )
                )

    return steps


def get_coord_set(steps, end):
    min_cost = min(step.cost for step in steps[end])

    queue = deque(gather_adjacencies(steps[end], 2**32, min_cost))
    coord_set = {end}

    while len(queue) > 0:
        step = queue.popleft()
        coord_set.add(step.src)
        queue.extend(gather_adjacencies(steps[step.src], step.step, step.cost))

    return coord_set


def gather_adjacencies(visits, target_step, target_cost):
    adjacencies = []

    for step in visits:
        if step.step < target_step and step.cost <= target_cost:
            adjacencies.append(step)

    return adjacencies


def print_board(board, path_coords):
    board = board.copy()
    for coord in path_coords:
        board[coord] = "O"
    board[board == "."] = " "
    print(grid_str(board))


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 45)
    main("test_1.txt", 64)
    main("input.txt")
