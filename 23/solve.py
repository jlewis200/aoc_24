#!/usr/bin/env python3

import networkx as nx


def solve(graph):
    total = 0

    for cycle in nx.simple_cycles(graph, 3):
        if len(cycle) == 3 and any(computer.startswith("t") for computer in cycle):
            total += 1

    return total


def parse(lines):
    graph = nx.Graph()

    for line in lines:
        src, dst = line.strip().split("-")
        graph.add_edge(src, dst)

    return graph


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 7)
    main("input.txt")
