#!/usr/bin/env python3

import numpy as np


def solve(reports):
    return sum(valid(report) for report in reports)


def valid(report):
    valid_report = valid_raw(report)
    idx = 0

    while not valid_report and idx < len(report):
        valid_report |= valid_raw(report[:idx] + report[idx + 1 :])
        idx += 1

    return valid_report


def valid_raw(report):
    report = np.array(report)
    diff = report[1:] - report[:-1]
    safe_increasing = ((diff >= 1) & (diff <= 3)).sum() == diff.shape[0]
    safe_decreasing = ((diff <= -1) & (diff >= -3)).sum() == diff.shape[0]
    return safe_increasing or safe_decreasing


def parse(lines):
    reports = []

    for line in lines:
        reports.append(list(map(int, line.strip().split())))

    return reports


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 4)
    main("input.txt")
