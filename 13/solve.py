#!/usr/bin/env python3

from re import search
from z3 import *


def solve(games):
    return sum(solve_game(game) for game in games)


def solve_game(game):
    (dy_a, dx_a), (dy_b, dx_b), (target_y, target_x) = game

    presses_a, presses_b = Ints("presses_a presses_b")

    solver = Solver()
    solver.add(presses_a <= 100)
    solver.add(presses_b <= 100)
    solver.add(dy_a * presses_a + dy_b * presses_b == target_y)
    solver.add(dx_a * presses_a + dx_b * presses_b == target_x)

    if solver.check() == sat:
        model = solver.model()
        return model[presses_a].as_long() * 3 + model[presses_b].as_long()

    return 0


def parse(data):
    parsed = []

    for game in data.split("\n\n"):
        parsed.append(parse_game(game))

    return parsed


def parse_game(game):
    match_a = search("Button A: X(?P<dx>.+), Y(?P<dy>.+)", game)
    match_b = search("Button B: X(?P<dx>.+), Y(?P<dy>.+)", game)
    match_target = search("Prize: X=(?P<x>.+), Y=(?P<y>.+)", game)

    button_a = int(match_a.group("dy")), int(match_a.group("dx"))
    button_b = int(match_b.group("dy")), int(match_b.group("dx"))
    target = int(match_target.group("y")), int(match_target.group("x"))

    return button_a, button_b, target


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 480)
    main("input.txt")
