# Tic Tac Q

Inferring the rules of Tic-Tac-Toe with a Quantum Born Machine (Issue \#17).

## Objective

We went for the `deep-learning` objective.

## Deliverable

* The presentation can be found in the media folder in both
[pptx](https://github.com/mikelsr/tic-tac-q/blob/master/media/Tic-Tac-Q_Presentation.pptx)
and
[pdf](https://github.com/mikelsr/tic-tac-q/blob/master/media/Tic-Tac-Q_Presentation.pdf)
formats.

* Code can be found at the [ttq](https://github.com/mikelsr/tic-tac-q/tree/master/ttq)
module folder.

* Some of the generated data can be found at the
[data](https://github.com/mikelsr/tic-tac-q/tree/master/data)
directory.

* Some Jupyter Notebooks are available in the root directory.

* There are additional development components in
[test_doc](https://github.com/mikelsr/tic-tac-q/tree/master/test_doc).

## Summary

### What we set to do

We wanted do create a Quantum Born Machine that generated winning Tic-Tac-Toe games based on a training set.

### What we actually did

We developed a 9 qubit circuit optimized with an scalable algorithm to replicate our desired behaviour.
The win ratios shown in the presentation take into account that illegal games the circuit considered
as won are actually a wrong game.

An optimization with random parameters gave a result slightly better than a random configuration while
a correctly parametrized optimization gives much better results. See presentation page 16.

### Where do those defer and what we would like to improve
 
We only took for won games complete games where 5 `X` and 4 `O` where used, meaning
we left no room for blank cells and illegal games where discarded as invalid games.

We would like to:

* Improve the parametrization to obtain better results.

* Add the possibility of a state being blank.

* Experiment with results obtained from smaller training sets.


## Abstract
Quantum Circuit Born Machines (QCBM) are quantum circuits with tunable parameters.
Their output -a quantum pure state- is measured canonically to yield a probability distribution,
where some binary outputs are more probable than others. We tune the parameters so that this
probability distribution resembles a desired training set, and our QCBM will serve as a generative
model for that training set.

For this project, if the training set is obtained from a finite ensemble of Tic-Tac-Toe grids where
player X -player 1- won (you may write them as arrays of 9 elements), the QCBM would yield with high
probability binary outcomes where player X won, maybe even configurations not originally in the
training set. All of this without us writing the rules of the game explicitly.
Can you make a Quantum Machine infer the win condition of Tic-Tac-Toe?

## Useful Resources

PRA publication: https://journals.aps.org/pra/abstract/10.1103/PhysRevA.98.062324

## Initial approach

Our fist goal was to get a quantum circuit that could get any desired state as a function of some tunable
parameters. As we are only interested in the probabilities of measuring each state we only search states
that differ in the absolute value of the amplitudes (of the computational basis states), that is we don't
need to fit the relative phases of the states.

For the proposed problem we need 9-qubit states (one for each cell in the Tic-Tac-Toe board).
The circuit that can get any desired state is shown bellow for a 4-qubit circuit.

![alt text](https://github.com/mikelsr/tic-tac-q/blob/master/media/img/State_maker_4-qubit.png "4-qubit Quantum Circuit to generate a desired quantum state (only the module of the amplitudes are selected).")

Where the unitary transformations are described as

<img src="https://github.com/mikelsr/tic-tac-q/blob/master/media/img/U3_thetaj.png" width="200"/>

the parameters of those gates are the ones to be tuned by our optimization algorithm.
