#!/usr/bin/env python3

import itertools
import numpy as np
from collections import deque
from aoc_data_structures import VectorTuple


def solve(grid):
    plots = get_plots(grid)
    perimeters = get_perimeters(grid, plots)
    total = 0

    for plot, perimeter in zip(plots, perimeters):
        total += len(plot) * len(perimeter)

    return total


def get_perimeters(grid, plots):
    perimeters = []

    for plot in plots:
        coord = plot.copy().pop()
        perimeters.append(get_perimeter(grid, plot))

    return perimeters


def get_perimeter(grid, plot):
    perimeter = list()
    plot_type = grid[plot.copy().pop()]

    for coord in plot:
        perimeter.extend(get_external_adjacencies(coord, grid, plot_type))

    return perimeter


def get_external_adjacencies(coord, grid, plot_type):
    external_adjacencies = []

    for adjacency in coord.orthogonals(grid):
        if grid[adjacency] != plot_type:
            external_adjacencies.append(coord)

    return external_adjacencies


def get_plots(grid):
    plots = []
    visited = set()

    for y, x in itertools.product(range(grid.shape[0]), range(grid.shape[1])):
        coord = VectorTuple(y, x)

        # skip visited and padding characters
        if coord in visited or grid[coord] == ".":
            continue

        plots.append(get_plot(grid, visited, coord))

    return plots


def get_plot(grid, visited, coord):
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
