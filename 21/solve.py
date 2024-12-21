#!/usr/bin/env python3

import re
import numpy as np
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

    def __sub__(self, other):
        return VectorTuple(
            self_element - other_element
            for self_element, other_element in zip(self, other)
        )

    def __abs__(self):
        return VectorTuple((abs(element) for element in self))

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))

    def orthogonals(self, board):
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
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos

    def manhattan(self):
        """
        Get manhattan magnitude of self.
        """
        return sum(abs(self))


class Keypad:

    def get_paths(self, digit):
        """
        Get paths to target using bfs.  Terminate a path if it includes the
        empty space or if an adjacency is further from the target than the
        previous position.
        """
        queue = deque([(self.position,)])
        paths = []
        target_position = VectorTuple(*np.argwhere(self.keypad == digit))

        while len(queue) > 0:
            path = queue.popleft()
            position = path[-1]

            if position == target_position:
                paths.append(path)
                continue

            for adjacency in position.orthogonals(self.keypad):
                delta = (target_position - adjacency).manhattan()
                prev_delta = (target_position - position).manhattan()

                if self.keypad[adjacency] == "#" or delta > prev_delta:
                    continue

                queue.append(path + (adjacency,))

        self.position = target_position
        paths = [self.convert_path(path) for path in paths]
        paths = self.filter_paths(paths)
        return paths

    def filter_paths(self, paths):
        """
        Drop paths with more than 2 sections of contiguous characters.

        retained:
            <<^^
            ^^<<

        dropped:
            <^^<
            <^<^
        """
        filtered_paths = []

        for path in paths:
            contiguous_count = len(re.findall(">+|<+|v+|\^+", path))
            if contiguous_count <= 2:  # maybe 3 for edge cases
                filtered_paths.append(path)

        return filtered_paths

    def convert_path(self, path):
        """
        Convert a path of tuple location to a string representation using
        [>, <, ^, v]
        """
        converted_path = []
        path = deque(path)
        src = path.popleft()

        while len(path) > 0:
            dst = path.popleft()
            converted_path.append(self.get_character(src, dst))
            src = dst

        converted_path.append("A")
        return "".join(converted_path)

    @staticmethod
    def get_character(src, dst):
        delta = dst - src

        if delta == VectorTuple(0, 1):
            return ">"

        if delta == VectorTuple(-1, 0):
            return "^"

        if delta == VectorTuple(0, -1):
            return "<"

        if delta == VectorTuple(1, 0):
            return "v"

        if delta == VectorTuple(0, 0):
            return "A"


class DirectionalKeypad(Keypad):
    def __init__(self):
        self.keypad = np.array(
            [
                ["#", "^", "A"],
                ["<", "v", ">"],
            ],
        )
        self.position = VectorTuple(0, 2)


class NumericKeypad(Keypad):

    def __init__(self):
        self.keypad = np.array(
            [
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["#", "0", "A"],
            ],
        )
        self.position = VectorTuple(3, 2)


def solve(codes):
    return sum(get_complexity(code) for code in codes)


def get_complexity(code):
    paths = get_numeric_paths(code)

    for _ in range(2):
        paths = get_directional_paths(paths)

    length = get_min_length(paths)
    code_value = int("".join(code[:-1]))
    return length * code_value


def get_directional_paths(paths):
    """
    Get the next paths to enter current path in the directional keypad.
    """
    dpad = DirectionalKeypad()
    next_paths = []

    for path in paths:
        next_path = []

        for digit in path:

            next_path.append(dpad.get_paths(digit))
        next_paths.append(next_path)

    paths = []
    for next_path in next_paths:
        paths.extend(enumerate_paths(next_path))

    return filter_non_min_paths(paths)


def get_numeric_paths(code):
    """
    Get the paths to enter code into the numeric keypad.
    """
    npad = NumericKeypad()
    paths = []

    for digit in code:
        paths.append(npad.get_paths(digit))

    return enumerate_paths(paths)


def get_min_length(paths):
    """
    Get the minimum path length from a list of paths.
    """
    return min(map(len, paths))


def filter_non_min_paths(paths):
    """
    Drop paths with length larger than the minimum.
    """
    min_length = get_min_length(paths)
    filtered_paths = []

    for path in paths:
        if len(path) == min_length:
            filtered_paths.append(path)

    return filtered_paths


def enumerate_paths(paths):
    """
    Generate paths from every combination of sections.
    """
    next_paths = [""]

    for digit_paths in paths:
        next_next_paths = []

        for digit_path in digit_paths:
            for next_path in next_paths:
                next_path += digit_path
                next_next_paths.append(next_path)
        next_paths = next_next_paths

    return next_paths


def parse(lines):
    codes = []

    for line in lines:
        codes.append(list(line.strip()))

    return codes


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 126384)
    main("input.txt")
