import random
from qiskit import execute, BasicAer, transpile, QuantumCircuit, QuantumRegister, ClassicalRegister
from Oracle import first
from Oracle import second


def run_circuits(csss, oracle, optimization_level=0):
    if oracle == 1:
        circuit = first.create_circuit(csss, hadamard=True)
    else:
        circuit = second.create_circuit(csss, hadamard=True)
    circuit.draw(output='mpl', filename=f'circuit_{oracle}.png')
    if circuit is not None:
        circuit = transpile(circuit, optimization_level=optimization_level)
        backend = BasicAer.get_backend("qasm_simulator")
        result = execute(circuit, backend=backend, shots=1000)
        solution = [e.split() for e in list(result.result().get_counts().keys())]
        if oracle == 1:
            expected = "1"
        else:
            expected =  "{0:b}".format(len(csss))
        return list([x[1][::-1] for x in filter(lambda e : e[0] == expected, solution)])
    else:
        return []

def main():
    # Test values
    n = 5
    m = 5

    if n + m > 22:
        print(f"Number of qubits {n+m+2} is greater than maximum (24) for 'qasm_simulator'.")
        return 0

    # Générez une matrice aléatoire de la taille spécifiée
    
    csss = [ [ [ 0 for _ in range(n) ] for _ in range(n) ] for _ in range(m) ]
    for k in range(m):
        for i in range(n):
            for j in range(i, n):
                csss[k][i][j] = random.randint(0,1)
                csss[k][j][i] = csss[k][i][j]
   
    csss =  [
                [
                    [0, 0, 1],
                    [0, 1, 0],
                    [1, 0, 0]
                ],
                [
                    [1, 0, 0],
                    [0, 0, 1],
                    [0, 1, 0]
                ]
            ]
     
    n = len(csss[-1])
    m = len(csss)

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
    
    print("Solution 1 : ", run_circuits(csss, 1, optimization_level=3))
    print("Solution 2 : ", run_circuits(csss, 2, optimization_level=3))

if __name__ == '__main__':
    main()