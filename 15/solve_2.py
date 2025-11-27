#!/usr/bin/env python3

from collections import deque
from os import environ
import numpy as np
from dataclasses import dataclass
from time import sleep
from aoc_data_structures import VectorTuple


@dataclass
class Box:
    left: VectorTuple
    right: VectorTuple

    def __hash__(self):
        return hash(self.left) + hash(self.right)


@dataclass
class Wall:
    coord: VectorTuple

    def __hash__(self):
        return hash(self.coord)


def solve(board, directions):
    coords = get_coords(board)
    robot = VectorTuple(*np.argwhere(board == "@"))
    animate = "ANIMATE" in environ

    for direction in directions:
        robot = attempt_move(coords, direction, robot)

        if animate:
            print(board_str(construct_board(coords, robot)))
            sleep(0.05)

    return get_gps(coords, robot)


def attempt_move(coords, direction, robot):
    """
    Attempt to move the robot.  Return updated position if successful.  Return
    original position if blocked by a wall.
    """
    try:
        move(coords, direction, robot)
        return robot + get_delta(direction)

    except ValueError:
        return robot


def move(coords, direction, robot):
    """
    Gather all adjacent boxes and update their positions.
    """
    delta = get_delta(direction)
    adjacent = gather_adjacent_boxes(coords, robot, delta)

    for box in adjacent:
        coords.pop(box.left)
        coords.pop(box.right)

    for box in adjacent:
        box.left += delta
        box.right += delta
        coords[box.left] = box
        coords[box.right] = box


def gather_adjacent_boxes(coords, robot, delta):
    """
    Gather adjacent boxes using a directional bfs.  Raise ValueError if a wall
    is encountered.
    """
    adjacent = set()
    visited = set()
    queue = deque([robot])

    while len(queue) > 0:
        position = queue.popleft() + delta

        if position in visited or position not in coords:
            continue

        if isinstance(coords[position], Wall):
            raise ValueError

        visited.add(position)
        adjacent.add(coords[position])
        queue.extend((coords[position].left, coords[position].right))

    return adjacent


def get_delta(direction):
    """
    Get a movement vector based on direction.
    """
    match direction:
        case "^":
            return VectorTuple(-1, 0)
        case "v":
            return VectorTuple(1, 0)
        case "<":
            return VectorTuple(0, -1)
        case ">":
            return VectorTuple(0, 1)


def get_gps(coords, robot):
    total = 0

    for item in set(coords.values()):

        if isinstance(item, Box):
            item.left *= VectorTuple(100, 1)
            total += sum(tuple(item.left))

    return total


def get_coords(board):
    """
    Construct dict mapping position:object.
    """
    coords = {}

    for wall in np.argwhere(board == "#"):
        wall = VectorTuple(wall)
        coords[wall] = Wall(wall)

    for box in np.argwhere(board == "["):
        left = VectorTuple(box)
        right = VectorTuple(box + VectorTuple(0, 1))
        box = Box(left, right)
        coords[left] = box
        coords[right] = box

    return coords


def construct_board(coords, robot):
    """
    Construct numpy array from position:item dict.
    """
    board = np.full((70, 100), " ")

    for item in coords.values():

        if isinstance(item, Wall):
            board[item.coord] = "#"

        else:
            board[item.left] = "["
            board[item.right] = "]"

    board[robot] = "@"
    return board


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def parse(data):
    board = []
    directions = []

    board_data, directions_data = data.split("\n\n")

    for line in board_data.split("\n"):
        expanded_line = []
        for char in list(line.strip()):
            if char == "#":
                expanded_line.extend(["#", "#"])
            if char == "O":
                expanded_line.extend(["[", "]"])
            if char == ".":
                expanded_line.extend([".", "."])
            if char == "@":
                expanded_line.extend(["@", "."])

        board.append(expanded_line)

    directions = list(directions_data.replace("\n", ""))

    return np.array(board), directions


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_1.txt", 9021)
    main("input.txt")
