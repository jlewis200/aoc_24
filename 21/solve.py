#!/usr/bin/env python3

import re
import numpy as np
from collections import deque, defaultdict
from itertools import pairwise
from itertools import product
from aoc_data_structures import VectorTuple


class Keypad:

    def get_paths(self, src, dst):
        """
        Get paths to target using bfs.  Terminate a path if it includes the
        forbidden space or if an adjacency is further from the target than the
        previous position.
        """
        queue = deque([(src,)])
        target_position = dst

        paths = []

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

        paths = [self.convert_path(path) for path in paths]
        return paths

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

        return "".join(converted_path + ["A"])

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


class NumericKeypad(Keypad):
    cache = {}

    def __init__(self):
        self.keypad = np.array(
            [
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["#", "0", "A"],
            ],
        )
        self.position = VectorTuple(*np.argwhere(self.keypad == "A"))

        for src in np.argwhere(self.keypad != "#"):
            src = VectorTuple(*src)

            for dst in np.argwhere(self.keypad != "#"):
                dst = VectorTuple(*dst)
                paths = self.get_paths(src, dst)
                self.cache[self.keypad[src] + self.keypad[dst]] = paths

    def get_numeric_paths(self, code):
        """
        Get the paths to enter code into the numeric keypad.
        """
        paths = []

        for src, dst in pairwise(["A"] + code):
            paths.append(self.cache[src + dst])

        return self.enumerate_paths(paths)

    @staticmethod
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


class DirectionalKeypad(Keypad):
    cache = {}

    def __init__(self):
        self.keypad = np.array(
            [
                ["#", "^", "A"],
                ["<", "v", ">"],
            ],
        )
        self.position = VectorTuple(0, 2)
        self.build_cache()

    def build_cache(self):
        """
        Build a cache mapping adjacent src and dst characters to paths.  In
        some case more than one path is possible, so these are stored as a list.

        schema:
            {
                ('<', '<'): ['A'],
                ('<', '>'): ['>>A'],
                ('<', 'A'): ['>>^A', '>^>A'],
                ...
            }
        """
        for src in np.argwhere(self.keypad != "#"):
            src = VectorTuple(*src)

            for dst in np.argwhere(self.keypad != "#"):
                dst = VectorTuple(*dst)
                key = (self.keypad[src], self.keypad[dst])
                self.cache[key] = self.get_paths(src, dst)

    def enumerate_cache_versions(self):
        """
        When more than one valid path exists between 2 characters, there isn't
        an obvious way to choose the best among paths of the same length.  Some
        downstream dependencies may affect which is actually the best for the
        given number.  This generator yields all possible permutations of the
        cache.
        """
        index_ranges = []

        for value in self.cache.values():
            index_ranges.append(range(len(value)))

        for indices in product(*index_ranges):
            yield {
                key: value[index]
                for (key, value), index in zip(self.cache.items(), indices)
            }


def solve(codes, depth):
    return sum(get_complexity(code, depth) for code in codes)


def get_complexity(code, depth):
    """
    Get the directional pad path length for each combination of directional
    cache and path.  Use the minimum length to find the code complexity.
    """
    paths = NumericKeypad().get_numeric_paths(code)
    lengths = []

    for cache in DirectionalKeypad().enumerate_cache_versions():
        for path in paths:
            lengths.append(get_directional_length(path, cache, depth))

    code_value = int("".join(code[:-1]))
    return min(lengths) * code_value


def get_directional_length(path, cache, depth):
    """
    Find the directional path length for a particular path/movement-cache
    combination.
    """
    count_cache = initialize_count_cache(path)

    for _ in range(depth):
        count_cache = get_next_cache_count(count_cache, cache)

    return sum(len(key) * value for key, value in count_cache.items())


def initialize_count_cache(path):
    count_cache = defaultdict(lambda: 0)

    for segment in re.findall("[^A]*A", path):
        count_cache[segment] += 1

    return count_cache


def get_next_cache_count(count_cache, cache):
    next_count_cache = defaultdict(lambda: 0)

    for segment, count in count_cache.items():
        segment = "A" + segment

        for src, dst in pairwise(segment):
            next_count_cache[cache[(src, dst)]] += count

    return next_count_cache


def parse(lines):
    codes = []

    for line in lines:
        codes.append(list(line.strip()))

    return codes


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, depth, expected=None):
    result = solve(parse(read_file(filename)), depth)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 2, 126384)
    main("input.txt", 2)
    main("test_0.txt", 25)
    main("input.txt", 25)
