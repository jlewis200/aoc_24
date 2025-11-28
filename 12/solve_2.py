#!/usr/bin/env python3

from itertools import product, chain
import numpy as np
from collections import deque
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import expand_grid


def solve(grid):
    """
    Get the original plot sizes, relabel plots uniquely to avoid adjacent plot
    type edge cases, expand the grid to avoid internal corridors of size 1
    edge cases.
    """
    plots = get_plots(grid)
    plot_lengths = [len(plot) for plot in plots]
    relabel_plots(grid, plots)
    grid = expand_grid(grid, 3)

    plots = get_plots(grid)
    perimeters = get_perimeters(grid, plots)
    total = 0

    for plot, perimeter, plot_length in zip(plots, perimeters, plot_lengths):
        plot_type = grid[plot.copy().pop()]
        total += plot_length * get_edges(grid, plot_type, perimeter)

    return total


def get_plots(grid):
    """
    BFS from each coordinate to find contiguous coords of the same plot type.
    """
    plots = []
    visited = set()

    for y, x in product(range(grid.shape[0]), range(grid.shape[1])):
        coord = VectorTuple(y, x)

        if coord in visited or grid[coord] == ".":
            continue

        plots.append(get_plot(grid, visited, coord))

    return plots


def get_plot(grid, visited, coord):
    """
    BFS to find contiguous coords of the same plot type.
    """
    plot = set()
    plot_type = grid[coord]
    queue = deque([coord])

    while len(queue) > 0:
        coord = queue.popleft()

        if coord in visited:
            continue

        if grid[coord] == plot_type:
            visited.add(coord)
            plot.add(coord)
            queue.extend(coord.orthogonals(grid))

    return plot


def get_perimeters(grid, plots):
    perimeters = []

    for plot in plots:
        perimeters.append(get_perimeter(grid, plot))

    return perimeters


def get_perimeter(grid, plot):
    """
    Gather the external adjacencies of each plot coordinate.
    """
    perimeter = set()
    plot_type = grid[plot.copy().pop()]

    for coord in plot:
        perimeter |= get_external_adjacencies(coord, grid, plot_type)

    return perimeter


def get_external_adjacencies(coord, grid, plot_type):
    """
    Get the external adjacencies of a coordinate, including diagonals.
    """
    external_adjacencies = set()

    for adjacency in chain(coord.orthogonals(grid), coord.diagonals(grid)):
        if grid[adjacency] != plot_type:
            external_adjacencies.add(coord)

    return external_adjacencies


def get_edges(grid, plot_type, perimeter):
    """
    Count straight sections of perimeter by counting corners of perimeter.
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


def relabel_plots(grid, plots):
    """
    Relabel plots so non-contiguous plots of same type are labeled uniquely.
    """
    for idx, plot in enumerate(plots, start=1):
        for coord in plot:
            grid[coord] = idx


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
