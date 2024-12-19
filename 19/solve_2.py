#!/usr/bin/env python3

from dataclasses import dataclass, field
from pprint import pprint


@dataclass
class Node:
    value: str = ""
    children: dict = field(default_factory=dict)
    terminal: bool = False


def solve(towels, patterns):
    trie = build_trie(towels)
    total = 0

    for pattern in patterns:
        cache = {}
        total += count_solves(pattern, trie, cache)

    return total


def build_trie(towels):
    trie = Node()

    for towel in towels:
        node = trie

        for character in towel:
            if character not in node.children:
                node.children[character] = Node(character)

            node = node.children[character]
        node.terminal = True

    return trie


def count_solves(pattern, trie, cache):
    """
    Traverse throught the trie/prefix-tree based on the pattern.  If the node
    is a terminal node (indicating a sequence in towels), recurse into the
    sub-pattern starting at the next index.  Sum across all terminal nodes
    encountered in the pattern.  Map pattern to result in cache.
    """
    if pattern in cache:
        return cache[pattern]

    if len(pattern) == 0:
        return 1

    total = 0
    node = trie

    for idx in range(len(pattern)):
        if pattern[idx] not in node.children:
            break

        node = node.children[pattern[idx]]

        if node.terminal:
            total += count_solves(pattern[idx + 1 :], trie, cache)

    cache[pattern] = total
    return total


def parse(data):
    towel_data, pattern_data = data.split("\n\n")
    towels = towel_data.strip().split(", ")
    patterns = pattern_data.strip().split()
    return towels, patterns


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 16)
    main("input.txt")
