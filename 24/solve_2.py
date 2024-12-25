#!/usr/bin/env python3

import re
from itertools import product, combinations
import numpy as np
import networkx as nx
from random import randrange
from tqdm import tqdm


class Circuit:

    def __init__(self, states, operations):
        self.states = states
        self.operations = operations
        self.graph = self.get_graph(operations)
        self._execution_order = None

    def swap(self, dst_0, dst_1):
        """
        Swap the predecessors of the specified nodes.  Also swap the
        operations.  Set _execution_order to None to force regeneration in the
        next call to get_execution_order()
        """
        (
            self.operations[dst_0],
            self.operations[dst_1],
        ) = (
            self.operations[dst_1],
            self.operations[dst_0],
        )

        predecessors_0 = list(self.graph.predecessors(dst_0))
        predecessors_1 = list(self.graph.predecessors(dst_1))

        self.graph.remove_edges_from(
            [(predecessor, dst_0) for predecessor in predecessors_0]
        )
        self.graph.remove_edges_from(
            [(predecessor, dst_1) for predecessor in predecessors_1]
        )
        self.graph.add_edges_from(
            [(predecessor, dst_0) for predecessor in predecessors_1]
        )
        self.graph.add_edges_from(
            [(predecessor, dst_1) for predecessor in predecessors_0]
        )

        self._execution_order = None

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
        if self._execution_order is None:
            execution_order = []

            for destination in nx.topological_sort(self.graph):
                if destination in self.operations:
                    execution_order.append(destination)

            self._execution_order = execution_order

        return self._execution_order

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
    Generate swap candidates and check each combination of per-bit swap
    candidates.
    """
    circuit = Circuit(states, operations)
    swap_candidates = get_swap_candidates(circuit)
    swap_combination = get_correct_combination(circuit, swap_candidates)
    return ",".join(sorted(np.array(swap_combination).flatten().tolist()))


def get_swap_candidates(circuit):
    """
    Generate swap candidates by trying every possible swap and checking if the
    set of invalid bits has improved.  Improved meaning the new set of invalid
    bits is a subset of the original invalid bits.  This ensures the swap fixes
    at least one invalid bit and doesn't introduce new invalid bits.
    """
    invalid_bits = get_invalid_bits(circuit)
    swap_candidates = {bit: set() for bit in invalid_bits}

    for dst_0, dst_1 in tqdm(
        list(combinations(circuit.operations.keys(), 2)),
        desc="generating swap candidates",
    ):
        circuit.swap(dst_0, dst_1)

        try:
            new_invalid_bits = get_invalid_bits(circuit)
        except nx.exception.NetworkXUnfeasible:
            continue
        finally:
            circuit.swap(dst_0, dst_1)

        if new_invalid_bits < invalid_bits:
            fixed_bit = (invalid_bits - new_invalid_bits).pop()
            swap_candidates[fixed_bit].add((dst_0, dst_1))

    return swap_candidates


def get_correct_combination(circuit, swap_candidates):
    """
    Try every combination of per-bit swap candidates.  If the swap combination
    has less than 8 unique values this indicates a gate is being swapped more
    than once.  This violates the problem description and the combination is
    skipped to prevent corrupting the circuit.
    """
    for swap_combination in tqdm(
        list(product(*swap_candidates.values())),
        desc="finding swap combination",
    ):
        if len(set(np.array(swap_combination).flatten())) != 8:
            continue

        for swap in swap_combination:
            circuit.swap(*swap)

        try:
            if len(get_invalid_bits(circuit)) == 0:
                return swap_combination
        except nx.exception.NetworkXUnfeasible:
            pass

        for swap in swap_combination:
            circuit.swap(*swap)


def get_invalid_bits(circuit, n_trials=200):
    """
    Check if a circuit is adding correctly by checking a number of random
    inputs.  Return true if all trials succeed.

    TODO: find a more deterministic method of checking for circuit errors.
    This is likely to find errors, but not guaranteed.  It's similar to
    probabilistic primality testing, but there's probably a deterministic
    approach.  I originally thought testing each bit individually would work,
    but it doesn't seem to be the case.

    Another issue is invalid bits will also produce larger invalid bits until
    both x and y bits are 0 in that position.  For example if bit position 9
    is invalid, bits 10, 11, 12, ... may also be identified as invalid.  The
    workaround implemented here is to take just the minimum erroneous bit per
    trial.  This relies on producing x/y combinations that result in only a
    single error for each of the erroneous bits, which isn't guaranteed due to
    the random generation method.
    """
    invalid_bits = set()

    for _ in range(n_trials):
        x, y = randrange(0, 2**45), randrange(0, 2**45)
        actual = circuit.add(x, y)
        expected = x + y

        if actual != expected:
            diff = actual ^ expected  # produces 1 where bits differ

            for idx, bit in enumerate(bin(diff)[::-1]):
                if bit == "1":
                    invalid_bits.add(idx)
                    break

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
    main("input.txt")
