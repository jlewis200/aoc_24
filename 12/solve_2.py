#!/usr/bin/env python3

from itertools import product, chain
import numpy as np
from collections import deque


def solve(board):
    """
    Get the original plot sizes, relabel plots uniquely to avoid adjacent plot
    type edge cases, expand the board to avoid internal corridors of size 1
    edge cases.
    """
    plots = get_plots(board)
    plot_lengths = [len(plot) for plot in plots]
    relabel_plots(board, plots)
    board = expand_board(board)

    plots = get_plots(board)
    perimeters = get_perimeters(board, plots)
    total = 0

    for plot, perimeter, plot_length in zip(plots, perimeters, plot_lengths):
        plot_type = board[plot.copy().pop()]
        total += plot_length * get_edges(board, plot_type, perimeter)

    return total


def get_plots(board):
    """
    BFS from each coordinate to find contiguous coords of the same plot type.
    """
    plots = []
    visited = set()

    for y, x in product(range(board.shape[0]), range(board.shape[1])):
        coord = VectorTuple(y, x)

        if coord in visited or board[coord] == ".":
            continue

        plots.append(get_plot(board, visited, coord))

    return plots


def get_plot(board, visited, coord):
    """
    BFS to find contiguous coords of the same plot type.
    """
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
            queue.extend(coord.adjacencies(board))

    return plot


def get_perimeters(board, plots):
    perimeters = []

    for plot in plots:
        perimeters.append(get_perimeter(board, plot))

    return perimeters


def get_perimeter(board, plot):
    """
    Gather the external adjacencies of each plot coordinate.
    """
    perimeter = set()
    plot_type = board[plot.copy().pop()]

    for coord in plot:
        perimeter |= get_external_adjacencies(coord, board, plot_type)

    return perimeter


def get_external_adjacencies(coord, board, plot_type):
    """
    Get the external adjacencies of a coordinate, including diagonals.
    """
    external_adjacencies = set()

    for adjacency in chain(coord.adjacencies(board), coord.diagonals(board)):
        if board[adjacency] != plot_type:
            external_adjacencies.add(coord)

    return external_adjacencies


def get_edges(board, plot_type, perimeter):
    """
    Count straightsections of perimeter by counting corners of perimeter.
    """
    corners = 0
    up_left = VectorTuple(-1, 0), VectorTuple(0, -1)
    up_right = VectorTuple(-1, 0), VectorTuple(0, 1)
    down_right = VectorTuple(1, 0), VectorTuple(0, 1)
    down_left = VectorTuple(1, 0), VectorTuple(0, -1)

    for coord in perimeter:
        if is_corner(coord, perimeter, *up_left):
            corners += 1
        elif is_corner(coord, perimeter, *up_right):
            corners += 1
        elif is_corner(coord, perimeter, *down_right):
            corners += 1
        elif is_corner(coord, perimeter, *down_left):
            corners += 1

    return corners


def is_corner(coord, perimeter, *deltas):
    return all(coord + delta in perimeter for delta in deltas)


def expand_board(board):
    """
    Expand the board to handle cases like:
        EEEEE
        EXXXX
        EEEEE
        EXXXX
        EEEEE

    which is expanded to
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
        EEEXXXXXXXXXXXX
        EEEXXXXXXXXXXXX
        EEEXXXXXXXXXXXX
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
        EEEXXXXXXXXXXXX
        EEEXXXXXXXXXXXX
        EEEXXXXXXXXXXXX
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEE
    """
    board = np.repeat(board, 3, axis=0)
    return np.repeat(board, 3, axis=1)


def relabel_plots(board, plots):
    """
    Relabel plots so non-contiguous plots of same type are labeled uniquely.
    """
    for idx, plot in enumerate(plots, start=1):
        for coord in plot:
            board[coord] = idx


def str_board(board):
    board_str = ""
    for row in board:
        for col in row:
            board_str += f"{col}"
        board_str += "\n"
    return board_str


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

    def adjacencies(self, board):
        for delta in (
            VectorTuple(1, 0),
            VectorTuple(-1, 0),
            VectorTuple(0, 1),
            VectorTuple(0, -1),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos

    def diagonals(self, board):
        for delta in (
            VectorTuple(1, 1),
            VectorTuple(-1, -1),
            VectorTuple(-1, 1),
            VectorTuple(1, -1),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(list(line.strip()))

    return np.pad(np.array(parsed), 1, constant_values=".").astype(object)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_2.txt", 236)
    main("test_1.txt", 368)
    main("test_0.txt", 1206)
    main("input.txt")
