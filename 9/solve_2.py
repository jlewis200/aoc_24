#!/usr/bin/env python3

from collections import deque
from dataclasses import dataclass


@dataclass
class File:
    index: int
    length: int
    file_id: int


@dataclass
class Freespace:
    index: int
    length: int


def solve(files, freespaces):
    for file in files[::-1]:
        for freespace in freespaces:
            if file.index > freespace.index and file.length <= freespace.length:
                file.index = freespace.index
                freespace.length -= file.length
                freespace.index += file.length
                if freespace.length == 0:
                    freespaces.remove(freespace)
                break

    return get_checksum(files)


def get_checksum(files):
    checksum = 0

    for file in files:
        checksum += file.file_id * sum(range(file.index, file.index + file.length))

    return checksum


def parse(data):
    data = deque(data.strip())
    files = []
    freespaces = []

    file_id = 0
    index = 0
    while len(data) > 0:
        file_length = int(data.popleft())
        files.append(File(index, file_length, file_id))
        index += file_length
        file_id += 1

        if len(data) > 0:
            freespace_length = int(data.popleft())
            freespaces.append(Freespace(index, freespace_length))
            index += freespace_length

    return files, freespaces


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 2858)
    main("input.txt")
