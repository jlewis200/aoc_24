#!/usr/bin/env python3

import re
import itertools
import networkx as nx
from pprint import pprint


def solve(states, operations):
    """
    Perform each operation in order of topological sort to resolve depencencies.
    """
    graph = get_graph(states, operations)

    for destination in nx.topological_sort(graph):
        if destination in operations:
            operation, operand_0, operand_1 = operations[destination]
            states[destination] = do_operation(
                operation,
                states[operand_0],
                states[operand_1],
            )

    return gather_result(states)


def get_graph(states, operations):
    """
    Build the graph based on states and operations.
    """
    graph = nx.DiGraph()

    for dst, (operator, src_0, src_1) in operations.items():
        graph.add_edge(src_0, dst)
        graph.add_edge(src_1, dst)

    for node, state in states.items():
        graph.nodes[node]["value"] = state

    return graph


def do_operation(operation, operand_0, operand_1):
    match operation:

        case "AND":
            return operand_0 & operand_1

        case "OR":
            return operand_0 | operand_1

        case "XOR":
            return operand_0 ^ operand_1


def gather_result(states):
    """
    Gather integer result from the circuit state.
    """
    result = 0

    for node, state in states.items():
        if node.startswith("z") and state:
            result += 2 ** int(node[1:])

    return result


def parse(data):
    states = {}
    operations = {}

    states_data, operations_data = data.split("\n\n")

    for line in states_data.split("\n"):
        key, value = line.split(":")
        states[key.strip()] = value.strip() == "1"

    for line in operations_data.strip().split("\n"):
        match = re.fullmatch(
            "(?P<operand_0>.+) (?P<operator>.*) (?P<operand_1>.*) -> (?P<destination>.*)",
            line,
        )
        operations[match.group("destination")] = (
            match.group("operator"),
            match.group("operand_0"),
            match.group("operand_1"),
        )

    return states, operations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 4)
    main("test_1.txt", 2024)
    main("input.txt")
