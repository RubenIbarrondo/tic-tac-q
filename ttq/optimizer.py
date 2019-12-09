#!/usr/bin/env python3

from numpy import pi
from scipy.optimize import minimize
from ttq import state_maker

# single values params
MAX_ERROR = 0.05
N = 1024
PARAMS = 3
STEP = 0.1
X0 = [1] * PARAMS

# multiple value params
BOUNDS = tuple((
    (0, 2*pi) for _ in range(PARAMS)
))

EXPECTED_VALUES = {
    '00': 0.5,
    '01': 0.2,
    '10': 0.2,
    '11': 0.1
}


def state_maker_wrapper(params):
    global EXPECTED_VALUES
    counts = state_maker.get_ensemble(
        *params, **{'N': N}
    )
    errors = {}
    # initialize missing keys
    for k in EXPECTED_VALUES.keys():
        if k not in counts.keys():
            counts[k] = 0
        errors[k] = counts[k] / N

    err = 0.0
    for state, error in errors.items():
        err += abs(EXPECTED_VALUES[state] - error)
    return err


def constraint(params):
    err = state_maker_wrapper(params)
    return 1.0 - err - MAX_ERROR


def optimize(x0):
    const = [{
        'type': 'ineq',
        'fun': constraint
    }]
    sol = minimize(state_maker_wrapper, x0,
                   method='SLSQP', bounds=BOUNDS,
                   constraints=const, options={'eps': STEP})
    return sol.x


if __name__ == '__main__':
    print(optimize(X0))
