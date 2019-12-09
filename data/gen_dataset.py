#!/usr/bin/env python3

from itertools import permutations
from os import makedirs
from os.path import join

O, X = 0, 1

DATA_DIR = 'out'

SAMPLES = 6
SOLUTION_FILE = 'training_set.txt'
SOLUTION_FILE_DISTINCT = 'training_set_distinct.txt'

BOARDS = [
    # 1
    [X, None, None,
     X, None, None,
     X, None, None],
    # 2
    [None, X, None,
     None, X, None,
     None, X, None],
    # 3
    [None, None, X,
     None, None, X,
     None, None, X],
    # 4
    [X, X, X,
     None, None, None,
     None, None, None],
    # 5
    [None, None, None,
     X, X, X,
     None, None, None],
    # 6
    [None, None, None,
     None, None, None,
     X, X, X],
    # 7
    [X, None, None,
     None, X, None,
     None, None, X],
    # 8
    [None, None, X,
     None, X, None,
     X, None, None],
]


def board_to_str(board):
    return ''.join(['0' if x == O else '1' for x in board])


def clean_set(solution):
    return list(set(solution))


def gen_boards():
    global BOARDS, O, X
    solution = []
    n = 0
    for board in BOARDS:
        # copy board by value
        empty_cells = []  # uninitialized cells
        for i in range(len(board)):
            if board[i] is None:
                empty_cells.append(i)

        cells = [X, X, O, O, O, O]
        perms = permutations(cells)
        for p in perms:
            b = board[:]
            for i in range(len(cells)):
                b[empty_cells[i]] = p[i]
            n += 1
            print('\rCreated {} solutions'.format(n), end='')
            solution.append(b)
    print()
    return solution


if __name__ == '__main__':
    try:
        makedirs(DATA_DIR)
    except FileExistsError:
        pass

    # all solutions
    solution = gen_boards()
    solution_str = [board_to_str(board) for board in solution]
    with open(join(DATA_DIR, SOLUTION_FILE), 'w') as f:
        for board in solution:
            f.write(board_to_str(board) + '\n')

    # unique solutions
    clean = clean_set(solution_str)
    print("Distinct solutions: {}".format(len(clean)))
    with open(join(DATA_DIR, SOLUTION_FILE_DISTINCT), 'w') as f:
        for line in clean:
            f.write(line + '\n')
