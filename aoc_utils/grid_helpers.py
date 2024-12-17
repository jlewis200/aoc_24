import numpy as np


def expand_board(board, expansion_size=2):
    """
    Expand a 2-d numpy array by duplicating elements.

    Example expand by 2:

        original:
            1 0
            0 1

        expanded:
            1 1 0 0
            1 1 0 0
            0 0 1 1
            0 0 1 1
    """
    board = np.repeat(board, expansion_size, axis=0)
    return np.repeat(board, expansion_size, axis=1)


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    string = ""
    for row in board:
        for col in row:
            string += f"{col}"
        string += "\n"
    return string


def hash_array(array):
    return hash("".join(array.flatten()))
