#!/usr/bin/env python3

import numpy as np
import networkx as nx


def solve(graph):
    cliques = list(nx.find_cliques(graph))
    idx = np.argmax(list(map(len, cliques)))
    return ",".join(sorted(cliques[idx]))


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
    main("test_0.txt", "co,de,ka,ta")
    main("input.txt")
