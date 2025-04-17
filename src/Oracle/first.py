from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
from qiskit.visualization import plot_histogram
import random
""" Given a system of quadratic equations over F_2, output a quantum
    circuit (in Nielsen and Chuang's qasm format), that can be used
    as the oracle in Grover's algorithm, to solve it.
    We use a standard form for the system of equations.  A system of
    m quadratic equations over n variables is given by a `cube' (l^k_ij)
    over F_2 where l^k_ij = 0 if i > j.  x_1, ..., x_n is a solution if
        \sum_{1 <= i <= j <= n} l^k_ij x_i x_j = 1
    for each 1 <= k <= m.  """

# NOTE this file is from mqgrover-{1,2,3}.py
def create_circuit(csss, hadamard = False):
    """ Creates Circuit for Grover oracle that solves the system of
        quadratic equations sqe over F_2 in standard form
    
            n: number of variables x_i in sqe
            m: number of equations in sqe
            sqe[k][i][j]: true if x_ix_j occurs in the k-th equation. """
    # First, create helper circuit that puts E^(k) into e_k
    n = len(csss[0])
    m = len(csss)

    qrx = QuantumRegister(n, "x")
    qrt = QuantumRegister(1, "t")
    qre = QuantumRegister(m + 1, "e")

    crx = ClassicalRegister(n, "crx")
    y = ClassicalRegister(1, "y")

    qc = QuantumCircuit(qrx, qrt, qre, crx, y)
    
    if hadamard:
        for i in range(n):
            qc.h(qrx[i])
        qc.barrier()
        
    E_circuit = QuantumCircuit(qrx, qrt, qre)

    for k in range(m):
        for i in range(n):
            if 1 not in csss[k][i]:
                continue
            y_circuit = QuantumCircuit(qrx, qrt, qre)
            for j in range(i, n):
                if csss[k][i][j] and i != j:
                    y_circuit.cx(qrx[j], qrt)
            if csss[k][i][i]:
                y_circuit.x(qrt)
            # XOR the value (x_i AND  y_i^(k)) into e_k
            # and clear t afterwards
            E_circuit = E_circuit.compose(y_circuit)  # first put y_i^(k) into t
            E_circuit.ccx(qrx[i], qrt, qre[k]) #
            E_circuit = E_circuit.compose(y_circuit.inverse())  # uncompute t
        E_circuit.barrier()
    qc = qc.compose(E_circuit)  # put E^(k) into e_k
    # put result into y
    qc.barrier()
    qc.mcx(qre[:-1], qre[-1])
    qc.barrier()
    qc = qc.compose(E_circuit.inverse())  # uncompute e_k
    
    qc.barrier()
    qc.measure(qrx, crx)
    qc.measure(qre[-1], y)
    
    return qc

import sys
import textwrap

def main():
    # Test values
    n = 2
    m = 2

    # Générez une matrice aléatoire de la taille spécifiée
    
    csss = [ [ [ 0 for _ in range(n) ] for _ in range(n) ] for _ in range(m) ]
    for k in range(m):
        for i in range(n):
            for j in range(i, n):
                csss[k][i][j] = random.randint(0,1)
                csss[k][j][i] = csss[k][i][j]
    '''
    csss =   [
                [
                    [1, 0, 0],
                    [0, 1, 1],          #   x0 + x1 + x1 * x2
                    [0, 1, 0]
                ],
                [
                    [0, 1, 1],
                    [1, 0, 1],          #   x0 + x0 * x1 + x0 * x2 + x1 * x2
                    [1, 1, 0]
                ],
                [
                    [0, 0, 1],
                    [0, 1, 1],          # x0 * x2 + x1 + x1 * x2 + x2
                    [1, 1, 0]
                ]
            ]
    csss = [
                [
                    [0, 1],
                    [1, 1]
                ],
                [
                    [1, 0],
                    [0, 1]
                ]
            ]
    csss =  [
                [
                    [0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 0],
                    [1, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 1, 0, 0, 1],
                    [0, 1, 0, 0, 0],
                    [0, 1, 1, 0, 1]
                ],
                [
                    [1, 1, 0, 1, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [1, 1, 1, 0, 1],
                    [0, 0, 1, 1, 1]
                ],
                [
                    [0, 0, 1, 0, 1],
                    [0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0]
                ]
            ]
    '''
    for k in range(m):
        for i in range(n):
            print(csss[k][i])
        print('\n')
        eq = ""
        for k in range(m):
            for i in range(n):
                for j in range(i, n):
                    if csss[k][i][j] == 1:
                        if eq != "" and eq[-1] != '\n':
                            eq += " + "
                        eq += (f'x{i}' if i == j else f'x{i} * x{j}')
            if eq != "" and eq[-1] != '\n':
                eq += '\n'
    print(eq)

    qc = create_circuit(csss, hadamard = True)
    print(qc)

    backend = BasicAer.get_backend("qasm_simulator")
    result = execute(qc, backend=backend, shots=1000).result()
    
    print(result.get_counts())
    print(dict(qc.count_ops()))
    
    #print or measure the value of the qubits
    s = [e[2:] for e in list(filter(lambda k : k[0] == '1', result.get_counts().keys()))]
    print("Solution : ", s) 

#def main():
#    n, m, sqe = parse_args()
#    # Hack to let qasm use n-qubit toffoli gate:
#    print("    def toffoli{0},{1},'o'".format(m, m))
#    create_circuit(n, m, sqe).print_qasm()

def parse_args():
    if len(sys.argv) != 4:
        print(textwrap.dedent('   '+__doc__))
        print("")
        usg = ("usage: {0} [n] [m] [l^1_183gg(1,1)][l^1_(1,2)]..."
                        "[l^1_(2,1)]...")
        print(usg.format(sys.argv[0]))
        sys.exit()
    n, m = int(sys.argv[1]), int(sys.argv[2])
    idx = 0
    ret = []
    for _ in range(m):
        row = []
        for i in range(n):
            term = []
            for _ in range(0, i):
                term.append(False)
            for _ in range(i, n):
                term.append(bool(int(sys.argv[3][idx])))
                idx += 1
            row.append(term)
        ret.append(row)
    return n, m, ret

if __name__ == '__main__':
    main()