#!/usr/bin/env python3

from collections import defaultdict


def solve(stones, steps):
    stones = {stone: 1 for stone in stones}

    for _ in range(steps):
        stones = get_next_stones(stones)

    return sum(stones.values())


def get_next_stones(stones):
    new_stones = defaultdict(lambda: 0)

    for stone, count in stones.items():
        apply_rules(stone, count, new_stones)

    return new_stones


def apply_rules(stone, count, new_stones):
    if stone == "0":
        new_stones["1"] += count

    elif len(stone) % 2 == 0:
        length = len(stone) // 2
        new_stones[str(int(stone[:length]))] += count
        new_stones[str(int(stone[length:]))] += count

    else:
        new_stones[str(int(stone) * 2024)] += count


def parse(data):
    return data.strip().split()


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, steps, expected=None):
    result = solve(parse(read_file(filename)), steps)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 25, 55312)
    main("input.txt", 25)
    main("input.txt", 75)
