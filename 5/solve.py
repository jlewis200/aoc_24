#!/usr/bin/env python3


def solve(rules, pages):
    total = 0

    for page in pages:
        if all(rule_satisfied(rule, page) for rule in rules):
            total += page[len(page) // 2]

    return total


def rule_satisfied(rule, page):
    value_0, value_1 = rule
    try:
        idx_0 = page.index(value_0)
        idx_1 = page.index(value_1)
        return idx_0 < idx_1
    except ValueError:
        return True


def parse(data):
    rules = []
    pages = []

    rule_data, page_data = data.split("\n\n")

    for rule in rule_data.strip().split():
        rules.append(tuple(map(int, rule.strip().split("|"))))

    for page in page_data.strip().split():
        pages.append(tuple(map(int, page.strip().split(","))))

    return rules, pages


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 143)
    main("input.txt")
