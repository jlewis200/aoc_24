#!/usr/bin/env python3

import itertools
import numpy as np
from collections import deque


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

    def __new__(self, *args):
        if len(args) == 1 and not isinstance(args[0], tuple):
            args = args[0]
        return tuple.__new__(VectorTuple, args)

    def __add__(self, other):
        return VectorTuple(
            self_element + other_element
            for self_element, other_element in zip(self, other)
        )

    def __sub__(self, other):
        return VectorTuple(
            self_element - other_element
            for self_element, other_element in zip(self, other)
        )

    def __mul__(self, other):
        return VectorTuple(
            self_element * other_element
            for self_element, other_element in zip(self, other)
        )

    def __truediv__(self, other):
        return VectorTuple(
            self_element / other_element
            for self_element, other_element in zip(self, other)
        )

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))


def adjacencies(coord, board):
    for delta in (
        VectorTuple(1, 0),
        VectorTuple(-1, 0),
        VectorTuple(0, 1),
        VectorTuple(0, -1),
    ):
        next_pos = coord + delta
        if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
            yield next_pos


def solve(board):
    plots = get_plots(board)
    perimeters = get_perimeters(board, plots)
    total = 0

    for plot, perimeter in zip(plots, perimeters):
        total += len(plot) * len(perimeter)

    return total


def get_perimeters(board, plots):
    perimeters = []

    for plot in plots:
        coord = plot.copy().pop()
        perimeters.append(get_perimeter(board, plot))

    return perimeters


def get_perimeter(board, plot):
    perimeter = list()
    plot_type = board[plot.copy().pop()]

    for coord in plot:
        perimeter.extend(get_external_adjacencies(coord, board, plot_type))

    return perimeter


def get_external_adjacencies(coord, board, plot_type):
    external_adjacencies = []

    for adjacency in adjacencies(coord, board):
        if board[adjacency] != plot_type:
            external_adjacencies.append(coord)

    return external_adjacencies


def get_plots(board):
    plots = []
    visited = set()

    for y, x in itertools.product(range(board.shape[0]), range(board.shape[1])):
        coord = VectorTuple(y, x)

        # skip visited and padding characters
        if coord in visited or board[coord] == ".":
            continue

        plots.append(get_plot(board, visited, coord))

    return plots


def get_plot(board, visited, coord):
    plot = set()
    plot_type = board[coord]
    queue = deque([coord])

    while len(queue) > 0:
        coord = queue.popleft()

        if coord in visited:
            continue

        if board[coord] == plot_type:
            visited.add(coord)
            plot.add(coord)
            queue.extend(adjacencies(coord, board))

    return plot


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(list(line.strip()))

    return np.pad(np.array(parsed), 1, constant_values=".")


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 1930)
    main("input.txt")
