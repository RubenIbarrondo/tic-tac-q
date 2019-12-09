from qiskit import QuantumCircuit, Aer

def state_maker(theta, ang0, ang1):
    '''
        Creates the circuit:
        
                ┌───────────────┐     ┌───────────┐
        q_0: |0>┤ U3(theta,0,0) ├──■──┤ U3(ang0)  ├
                └───────────────┘┌─┴─┐├───────────┤
        q_1: |0>─────────────────┤ X ├┤ U3(ang1)  ├
                                 └───┘└───────────┘
         c_0: 0 ═══════════════════════════════════

         c_1: 0 ═══════════════════════════════════
         
         Where U3(x,y,z) is the general unitary described in
         https://community.qiskit.org/textbook/ch-gates/quantum-gates.html
         
         This circuit can be used to get any desired two-qubit state.
         
         Args:
            theta: float parameter in range [0, 2pi)
            ang0: arry of form [t1, t2, t3], each value is in range [0, 2pi)
            ang1: arry of form [t1, t2, t3], each value is in range [0, 2pi)
            
         Returns:
            circ: QuantumCircuit according to the given arguments
         
    '''
    circ = QuantumCircuit(2,2)

    circ.u3(theta, 0, 0, 0)
    circ.cx(0, 1)
    circ.u3(*ang1, 1)
    circ.u3(*ang0, 0)
    
    return circ

def get_ensemble(theta, ang0, ang1, N=1024):
    '''
        Simulates (qasm_simulator) the measures the output of the circuit:
         
                ┌───────────────┐     ┌───────────┐┌─┐   
        q_0: |0>┤ U3(theta,0,0) ├──■──┤ U3(ang0)  ├┤M├───
                └───────────────┘┌─┴─┐├───────────┤└╥┘┌─┐
        q_1: |0>─────────────────┤ X ├┤ U3(ang1)  ├─╫─┤M├
                                 └───┘└───────────┘ ║ └╥┘
         c_0: 0 ════════════════════════════════════╩══╬═
                                                       ║ 
         c_1: 0 ═══════════════════════════════════════╩═
         
         Where U3(x,y,z) is the general unitary described in
         https://community.qiskit.org/textbook/ch-gates/quantum-gates.html
         
         This circuit can be used to get any desired two-qubit state. Note 
         that the measurement is performed in the computational basis, resulting
         in a probability distribution of the involved superposed states.
         
         This means, that with this function you can get any desired probability
         distribution of the states |00>,|01>,|10>,|11>.
         
         Args:
            theta: float parameter in range [0, 2pi)
            ang0: arry of form [t1, t2, t3], each value is in range [0, 2pi)
            ang1: arry of form [t1, t2, t3], each value is in range [0, 2pi)
            N: integer number of shots for the measurements.
            
         Returns:
            circ: QuantumCircuit according to the given arguments
         
    '''

    circuit = state_maker(theta, ang0, ang1)
    
    circuit.measure(2,2)
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend = simulator, shots = N).result()
    counts = result.get_counts()
    
    return counts
