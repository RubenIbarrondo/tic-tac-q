#!/usr/bin/env python3

from itertools import product
from math import ceil, log
import numpy as np
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

CONF_TEMPLATE = {
        'bound': [0, 2 * np.pi],
        'expected_values': np.array([0.5, 0.2, 0.2, 0.1]),
        'max_error': _MAX_ERROR,
        'max_iter': None,
        'n_states': _N,
        'step': _STEP,
        'x0': [0] * _PARAMS
}


def gen_expected_values(n):
    return np.full(n, 1/n)


def gen_expected_values_aux(n):
    zeroes = np.zeros(n - n//2)
    non_zeroes = np.full(n//2, 2/n)
    return np.concatenate((zeroes, non_zeroes))


def group_params(single_list):
    result = []
    for i in range(len(single_list), step=2):
        result.append([single_list[i], single_list[i + 1]])
    return result


def ungroup_params(double_list):
    result = []
    for pair in double_list:
        result.append(pair[0])
        result.append(pair[1])
    return result


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

    size = len(expected_values)

    # generator of binary strings
    binary_states = [x for x in map(''.join, product('01', repeat=ceil(log(size, 2))))]

    # initialize array with values of er
    count_values = np.zeros(size)
    # get keys of counts ('000', '001', ...)
    count_keys = sorted(counts.keys())
    for i in range(size):
        k = binary_states[i]
        # if key is found, use probability (count/n) of that count
        if k in count_keys:
            count_values[i] = counts.get(k) / n

    # absolute value of each error
    err_array = np.subtract(expected_values, count_values)
    err_array = np.absolute(err_array)

    # sum of all values
    return np.sum(err_array)


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
        'bound': [0, 2 * np.pi],
        # 'expected_values': gen_expected_values(4),
        'expected_values': np.array([0.5, 0.2, 0.2, 0.1]),
        'max_error': _MAX_ERROR,
        'max_iter': None,
        'n_states': _N,
        'step': _STEP,
        'x0': [0] * _PARAMS
    }
    print(optimize(conf))
