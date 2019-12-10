#!/usr/bin/env python3

from json import loads
from sys import argv

import gen_dataset as data_gen


files = argv[1:]

solution = data_gen.gen_boards()
solution_str = sorted([data_gen.board_to_str(board) for board in solution])
win_games = set(data_gen.clean_set(solution_str))

for f in files:
    data = ''
    with open(f, 'r') as df:
        data = loads(df.read())
    wins, loses = 0, 0
    print(f'file: \'{f}\'')
    for r, c in data.get('results').items():
        if r in win_games:
            wins += c
        else:
            loses += c
        total = wins + loses
        print(f'\rtotal: {total} wins: {wins} ({wins/total*100}%) loses: {loses} ({loses/total*100}%)' + ' '*20, end='')
    print()
