# tic-tac-q
Inferring the rules of Tic-Tac-Toe with a Quantum Born Machine (Issue \#17)

##



## Deliverable

* The presentation can be found at the root folder in
pdf
format or in the media folder in
pptx
format.

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
