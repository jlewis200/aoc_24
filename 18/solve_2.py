#!/usr/bin/env python3

from collections import deque


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

    def __new__(cls, *args):
        if len(args) == 1 and not isinstance(args[0], tuple):
            args = args[0]
        return tuple.__new__(VectorTuple, args)

    def __add__(self, other):
        return VectorTuple(
            self_element + other_element
            for self_element, other_element in zip(self, other)
        )

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))

    def orthogonals(self, board_size):
        """
        Generate E, N, W, S adjacencies.
        """
        for delta in (
            VectorTuple(0, 1),
            VectorTuple(-1, 0),
            VectorTuple(0, -1),
            VectorTuple(1, 0),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board_size + 1), range(board_size + 1)):
                yield next_pos


def solve(coords, size, steps):
    """
    Perform binary search to get an index within 1 of the first failing index.
    Check offsets -1, 0, +1 in order and return first failing.
    """
    lower = 0
    upper = len(coords)

    while lower < upper:
        mid = (lower + upper) // 2

        if has_path(coords[:mid], size):
            lower = mid + 1

        else:
            upper = mid - 1

    for idx in range(lower - 1, lower + 2):
        if not has_path(coords[:idx], size):
            break

    return ",".join(map(str, coords[idx - 1]))


def has_path(coords, size):
    """
    BFS to check if a path exists.  If terminal position is not target position
    there is no path.
    """
    target = VectorTuple(size, size)
    position = VectorTuple(0, 0)
    queue = deque([(position, 0)])
    visited = set()

    while len(queue) > 0 and position != target:
        position, step = queue.popleft()

        for adjacency in position.orthogonals(size):
            if adjacency not in coords and adjacency not in visited:
                queue.append((adjacency, step + 1))
                visited.add(adjacency)

    return position == target


def parse(lines):
    coords = []

    for line in lines:
        coords.append(VectorTuple(*map(int, line.strip().split(","))))

    return coords


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, size, steps, expected=None):
    result = solve(parse(read_file(filename)), size, steps)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 6, 12, "6,1")
    main("input.txt", 70, 1024)
