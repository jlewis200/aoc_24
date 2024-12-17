#!/usr/bin/env python3


def solve(rules, pages):
    invalid = get_invalid(rules, pages)
    pages = sort_pages(rules, invalid)
    return sum(page[len(page) // 2] for page in pages)


def sort_pages(rules, pages):
    for page in pages:
        changed = True

        while changed:
            changed = sort_page(rules, page)

    return pages


def sort_page(rules, page):
    changed = False

    for rule in rules:
        if not rule_satisfied(rule, page):
            swap(rule, page)
            changed = True

    return changed


def swap(rule, page):
    value_0, value_1 = rule
    idx_0 = page.index(value_0)
    idx_1 = page.index(value_1)
    page[idx_0], page[idx_1] = value_1, value_0


def get_invalid(rules, pages):
    invalid = []

    for page in pages:
        if not all(rule_satisfied(rule, page) for rule in rules):
            invalid.append(page)

    return invalid


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
        pages.append(list(map(int, page.strip().split(","))))

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
    main("test_0.txt", 123)
    main("input.txt")
