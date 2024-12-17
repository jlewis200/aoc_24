from z3 import *


def z3_example(game):

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
