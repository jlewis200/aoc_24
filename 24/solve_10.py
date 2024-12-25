#!/usr/bin/env python3

import re
import itertools
import networkx as nx
from random import randrange
from pprint import pprint


class Circuit:

    def __init__(self, states, operations):
        self.states = states
        self.operations = operations
        self.graph = self.get_graph(operations)

    def swap(self, dst_0, dst_1):
        (
            self.operations[dst_0],
            self.operations[dst_1],
        ) = (
            self.operations[dst_1],
            self.operations[dst_0],
        )

        successors_0 = list(self.graph.successors(dst_0))
        successors_1 = list(self.graph.successors(dst_1))

        for successor in successors_0:
            self.graph.remove_edge(dst_0, successor)
            self.graph.add_edge(dst_1, successor)

        for successor in successors_1:
            self.graph.remove_edge(dst_1, successor)
            self.graph.add_edge(dst_0, successor)

    def add(self, x, y):
        """
        Execute the gates in order and return the result.
        """
        states = self.get_states(x, y)

        for destination in self.get_execution_order():
            operation, operand_0, operand_1 = self.operations[destination]
            states[destination] = self.do_operation(
                operation,
                states[operand_0],
                states[operand_1],
            )

        return self.gather_result(states)

    def get_states(self, x, y, input_bits=45):
        """
        Build the state dict with input bits matching x and y.
        """
        states = {}

        for idx, (x_bit, y_bit) in enumerate(
            zip(
                f"{x:0{input_bits}b}"[::-1],
                f"{y:0{input_bits}b}"[::-1],
            )
        ):
            states[f"x{idx:02}"] = int(x_bit)
            states[f"y{idx:02}"] = int(y_bit)

        return states

    def get_execution_order(self):
        """
        Get the gate execution order by building a graph and sorting topologically.
        """
        execution_order = []

        for destination in nx.topological_sort(self.graph):
            if destination in self.operations:
                execution_order.append(destination)

        return execution_order

    @staticmethod
    def get_graph(operations):
        """
        Build the graph based on states and operations.
        """
        graph = nx.DiGraph()

        for dst, (operator, src_0, src_1) in operations.items():
            graph.add_edge(src_0, dst)
            graph.add_edge(src_1, dst)

        return graph

    @staticmethod
    def do_operation(operation, operand_0, operand_1):
        match operation:

            case "AND":
                return operand_0 & operand_1

            case "OR":
                return operand_0 | operand_1

            case "XOR":
                return operand_0 ^ operand_1

    @staticmethod
    def gather_result(states):
        """
        Gather integer result from the circuit state.
        """
        result = 0

        for node, state in states.items():
            if node.startswith("z") and state:
                result += 2 ** int(node[1:])

        return result


def solve(states, operations):
    """
    Perform each operation in order of topological sort to resolve depencencies.


    This backtrace suggests the swap() logic or execution_order() is off:

    ./solve_10.py
    {24, 9, 20, 31}
    Traceback (most recent call last):
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 236, in <module>
        main("input.txt")
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 227, in main
        result = solve(*parse(read_file(filename)))
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 128, in solve
        return attempt_solve(circuit)
               ^^^^^^^^^^^^^^^^^^^^^^
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 143, in attempt_solve
        invalid_bits_ = get_invalid_bits(circuit)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 178, in get_invalid_bits
        actual = circuit.add(x, y)
                 ^^^^^^^^^^^^^^^^^
      File "/home/anon/projects/aoc_24/24/./solve_10.py", line 48, in add
        states[operand_0],
        ~~~~~~^^^^^^^^^^^
    KeyError: 'vgh'

    """

    circuit = Circuit(states, operations)
    return attempt_solve(circuit)


def attempt_solve(circuit):
    invalid_bits = get_invalid_bits(circuit)
    print(invalid_bits)

    swapped_edges = set()

    for idx, (dst_0, dst_1) in enumerate(
        itertools.combinations(circuit.operations.keys(), 2)
    ):
        circuit.swap(dst_0, dst_1)

        try:
            invalid_bits_ = get_invalid_bits(circuit)
        except nx.exception.NetworkXUnfeasible:
            circuit.swap(dst_0, dst_1)
            continue

        if invalid_bits_ < invalid_bits:
            swapped_edges |= {(dst_0, dst_1)}

        print(idx)
        print(dst_0, dst_1)
        print(invalid_bits_)
        print(sorted(list(swapped_edges)))
        print()

    print(f"{get_invalid_bits(operations) = }")
    print(sorted(list(swapped_edges)))
    # print(",".join(sorted(list(swapped_edges))))
    return invalid_bits, operations, swapped_edges


def get_invalid_bits(circuit, n_trials=100):
    """
    Check if a circuit is adding correctly by checking a number of random
    inputs.  Return true if all trials succeed.

    TODO: find a more deterministic method of checking for circuit errors.
    This is likely to find errors, but not guaranteed.  It's similar to
    probabilistic primality testing, but there's probably a deterministic
    approach.  I originally thought testing each bit individually woul work,
    but it doesn't seem to be the case.
    """
    invalid_bits = set()
    x, y = 0, 0

    for _ in range(n_trials):
        actual = circuit.add(x, y)
        expected = x + y

        if actual != expected:
            diff = actual ^ expected

            invalid_bits_ = set()
            for idx, bit in enumerate(bin(diff)[::-1]):
                if bit == "1":
                    invalid_bits_.add(idx)

            invalid_bits.add(min(invalid_bits_))

        x = randrange(0, 2**45)
        y = randrange(0, 2**45)

    return invalid_bits


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
    # main("test_0.txt", 4)
    # main("test_1.txt", 2024)
    main("input.txt")
