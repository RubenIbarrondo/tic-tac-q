#!/usr/bin/env python3

from ttq import state_maker

N = 1024
EXPECTED_VALUES = {
    '00': 512,
    '01': 205,
    '10': 204,
    '11': 103
}


def state_maker_wrapper(theta0, theta1, theta2, n=N):
    counts = state_maker.get_ensemble(
        theta0, theta1, theta2, N
    )
    err = 0.0
    for state, count in counts.items():
        err += abs(EXPECTED_VALUES[state] - count)
    return err
