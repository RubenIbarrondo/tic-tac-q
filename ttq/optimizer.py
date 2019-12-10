#!/usr/bin/env python3


from itertools import product
from json import dumps
from math import ceil, log
import numpy as np
from scipy.optimize import minimize
from time import sleep

from ttq import gen_dataset as data_gen
from ttq import state_maker

ATTEMPT_N = 0

# single values params
_MAX_ERROR = 0.05
_N = 1024
_PARAMS = 4
_STEP = 0.1
# _X0 = [1] * _PARAMS
_X0 = [0.0, 0.5, 1.0, 1.5]

# multiple value params
_EXPECTED_VALUES = {
    '00': 0.5,
    '01': 0.2,
    '10': 0.2,
    '11': 0.1
}

CONF_TEMPLATE = {
        'bound': [0, 2 * np.pi],
        'expected_values': [
            np.array([0.5, 0.2, 0.2, 0.1])
        ],
        'max_error': _MAX_ERROR,
        'max_iter': None,
        'n_states': _N,
        'q': 2,
        'step': _STEP,
        'x0': _X0
}


def gen_expected_values_1(n):
    """
    Util function to generate expected values
    """
    return np.full(n, 1/n)


def gen_expected_values_2(n):
    """
    Util function to generate expected values
    """
    zeroes = np.zeros(n - n//2)
    non_zeroes = np.full(n//2, 2/n)
    return np.concatenate((zeroes, non_zeroes))


def group_params(single_list):
    """
    Group parameters into pairs
    """
    result = []
    for i in range(0, len(single_list), 2):
        result.append([single_list[i], single_list[i + 1]])
    return result


def ungroup_params(double_list):
    """
    Make a list from pairs of parameters
    """
    result = []
    for pair in double_list:
        result.append(pair[0])
        result.append(pair[1])
    return np.asarray(result)


def state_maker_wrapper(params, conf):
    """
    Wrapper to enable optimization of state_maker.get_ensemble.
    It aggregates the error instead of returning the error of each state individually.
    """
    global ATTEMPT_N
    if ATTEMPT_N % 10 == 0:
        print('\rAttempt number: {}'.format(ATTEMPT_N), end='')
    ATTEMPT_N += 1

    expected_values = conf.get('expected_values')
    n = conf.get('n_states')
    q = conf.get('q')

    size = len(expected_values)
    counts = state_maker.get_ensemble_Q(
        *[group_params(params)], **{'Q': q, 'T': n}
    )

    # generator of binary strings
    binary_states = [x for x in map(''.join, product('01', repeat=q))]

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
    Constraint function of the optimization
    """
    max_error = conf.get('max_error')
    err = state_maker_wrapper(params, conf)
    return 1.0 - err - max_error


def optimize(conf):
    """
    Optimization function
    @param conf: contains the following parameters
        'bound': [<min_val>, <max_val>],
        'expected_values': np.array([<expected_values>]),
        'max_error': <max_error>,
        'max_iter': <None or maximum_number_of_iterations],
        'n_states': <number of states, usually 1024>,
        'step': <optimization_step (e.g. 0.1)>,
        'x0': [<initial_version_of_params>]
    }
    @return [<optimal_values>]
    """
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


def gen_boards():
    solution = data_gen.gen_boards()
    solution_str = sorted([data_gen.board_to_str(board) for board in solution])
    # winning games
    winning_games = sorted(data_gen.clean_set(solution_str))
    # all games
    wins = len(winning_games)
    boards_gen = [x for x in map(''.join, product('01', repeat=9))]
    probabilities = {}
    for i in range(512):
        board = boards_gen[i]
        probabilities[board] = 1/wins if board in winning_games else 0
    return probabilities


if __name__ == '__main__':
    # generate probabilities
    expected_values = gen_boards()
    expected_values = np.asarray(list(expected_values.values()))

    fn = 1
    while True:
        # configure optimization parameters
        conf = dict(CONF_TEMPLATE)
        conf['expected_values'] = expected_values
        conf['max_iter'] = 30
        conf['max_error'] = 0.02
        # obtain q values
        q = ceil(log(len(expected_values), 2))
        conf['q'] = q
        conf['x0'] = [0.3 * fn] * (q * 2)
        # run configuration
        opt_values = optimize(conf)
        result = state_maker.get_ensemble_Q(
            thetas=group_params(opt_values),
            Q=q,
            T=1024
        )
        output = {
            'thetas': list(opt_values),
            'results': result
        }
        with open('out/result_{}.txt'.format(fn), 'w') as f:
            f.write(dumps(output, indent=4))
        fn += 1
        print()
        print(f'Finished {fn}')
        ATTEMPT_N = 0
        sleep(15)

