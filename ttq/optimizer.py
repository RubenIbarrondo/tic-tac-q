#!/usr/bin/env python3

from numpy import pi
from scipy.optimize import minimize
from ttq import state_maker

# single values params
_MAX_ERROR = 0.05
_N = 1024
_PARAMS = 3
_STEP = 0.1
_X0 = [1] * _PARAMS

# multiple value params
_EXPECTED_VALUES = {
    '00': 0.5,
    '01': 0.2,
    '10': 0.2,
    '11': 0.1
}


def state_maker_wrapper(params, conf):
    """
    Wrapper to enable optimization of state_maker.get_ensemble.
    It aggregates the error instead of returning the error of each state individually.
    """
    expected_values = conf.get('expected_values')
    n = conf.get('n_states')

    counts = state_maker.get_ensemble(
        *params, **{'N': n}
    )
    errors = {}
    # initialize missing keys
    for k in expected_values.keys():
        if k not in counts.keys():
            counts[k] = 0
        errors[k] = counts[k] / n

    err = 0.0
    for state, error in errors.items():
        err += abs(expected_values[state] - error)
    return err


def constraint(params, conf):
    """
    Constraint function of the
    """
    max_error = conf.get('max_error')
    err = state_maker_wrapper(params, conf)
    return 1.0 - err - max_error


def optimize(conf):
    bound = conf.get('bound')
    max_iter = conf.get('max_iter')
    step = conf.get('step')
    x0 = conf.get('x0')

    bounds = tuple((
        (bound[0], bound[1]) for _ in range(len(x0))
    ))

    const = [{
        'type': 'ineq',
        'fun': constraint,
        'args': [conf]
    }]
    options = {'eps': step}
    if max_iter is not None:
        options['maxiter'] = int(max_iter)
    sol = minimize(state_maker_wrapper,
                   x0,
                   method='SLSQP',
                   bounds=bounds,
                   args=conf,
                   constraints=const,
                   options=options)
    return sol.x


if __name__ == '__main__':
    conf = {
        'bound': [0, 2 * pi],
        'expected_values': _EXPECTED_VALUES,
        'max_error': _MAX_ERROR,
        'max_iter': None,
        'n_states': _N,
        'step': _STEP,
        'x0': [0] * _PARAMS
    }
    print(optimize(conf))
