import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.circuit.library.standard_gates import XGate

# Function to create the oracle circuit
def create_circuit(csss, hadamard = False):
    m = len(csss)
    n = len(csss[0])
    c = n.bit_length()
    
    qrx = QuantumRegister(n, "x")
    qrt = QuantumRegister(2, "t")
    qrc = QuantumRegister(c, "c")

    crx = ClassicalRegister(n, "crx")
    crc = ClassicalRegister(c, "y")
    circuit = QuantumCircuit(qrx, qrt, qrc, crx, crc)

    if hadamard:
        circuit.h(qrx)
    circuit.barrier()

    for k in range(m):
        tmp2 = QuantumCircuit(qrx, qrt, qrc)
        for i in range(n):
            if 1 not in csss[k][i]:
                continue
            tmp = QuantumCircuit(qrx, qrt, qrc)
            for j in range(i, n):
                if csss[k][i][j] and i != j:
                    tmp.cnot(qrx[j], qrt[0])
            if csss[k][i][i]:
                tmp.x(qrt[0])
            tmp2 = tmp2.compose(tmp)
            tmp2.ccx(qrx[i], qrt[0], qrt[1])
            tmp2 = tmp2.compose(tmp.inverse())
        circuit = circuit.compose(tmp2)
        circuit.barrier()
        # Increment the counter
        for i in range(c - 1, -1, -1):
            circuit.mcx(qrt[1:] + qrc[:i], qrc[i])
        
        circuit.barrier()
        circuit = circuit.compose(tmp2.inverse())
        circuit.barrier()

    circuit.barrier()
    
    circuit.measure(qrx, crx)
    circuit.measure(qrc, crc)

    return circuit

def main():
    # Define your conditions (csss) and qubits (xs)
    n = 3
    m = 3
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
                        [1, 1, 1],
                        [1, 0, 1],          #   x0 + x0 * x1 + x0 * x2 + x1 * x2
                        [1, 1, 0]
                    ],
                    [
                        [0, 0, 1],
                        [0, 1, 1],          # x0 * x2 + x1 + x1 * x2 + x2
                        [1, 1, 1]
                    ]
                ]
    '''
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
    '''
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
    # Create the Grover's oracle circuit with the dynamic counter
    grover_circuit = create_circuit(csss, hadamard=True)
    print(grover_circuit)
    print(dict(grover_circuit.count_ops()))

    # Simulate the circuit
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(grover_circuit, simulator).result()
    statevector = result.get_statevector()

    print(statevector)

    plot_bloch_multivector(statevector)

    # Measure the qubits and get the histogram of outcomes
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(grover_circuit, simulator, shots=1024).result()
    counts = result.get_counts()

    print(counts)

    # Find the solution based on the dynamic counter measurement
    for count, _ in counts.items():
        # Extract the binary part that represents the counter (remove the additional information)
        count_binary = count.split()[0]
        x = count.split()[1]
        try:
            # Convert the binary count to an integer
            count_int = int(count_binary, 2)
            
            if count_int == len(csss):
                # If the count matches the number of equations, it's a potential solution
                print("Potential solution found with count:", x)
                # You can check the state of the counter to determine which equations were satisfied

                # For example, print the binary state of the counter
                print("Counter state:", count_binary)

                # Decode the binary count to identify which equations were satisfied in this solution
                #satisfied_equations = [csss[i] for i in range(len(qrx)) if count_binary[i] == '1']
                #print("Satisfied equations:", satisfied_equations)
        except ValueError:
            # Handle the case where the string cannot be converted to an integer
            print(f"Invalid count format: {count}")