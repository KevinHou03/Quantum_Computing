from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import numpy as np

def qft_rotations(circuit, n):
    """Apply QFT rotations"""
    for j in range(n):
        circuit.h(j)
        for k in range(j+1, n):
            circuit.cp(np.pi / (2 ** (k - j)), k, j)

def inverse_qft(circuit, n):
    """Apply inverse QFT"""
    for j in reversed(range(n)):
        for k in reversed(range(j+1, n)):
            circuit.cp(-np.pi / (2 ** (k - j)), k, j)
        circuit.h(j)

def add_quantum_adder(a, b, n=3):
    """
    Add integers a and b using QFT-based quantum adder
    Args:
        a (int): First number (stored in top register)
        b (int): Second number (added via phase rotations)
        n (int): Number of qubits
    """
    qc = QuantumCircuit(n)

    # Load |a⟩ into register
    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)

    # Apply QFT
    qft_rotations(qc, n)

    for i in range(n):
        for j in range(i+1):
            if (b >> j) & 1:
                qc.p(np.pi / (2 ** (i - j)), i)

    inverse_qft(qc, n)

    # Measure
    qc.measure_all()

    return qc

# example: add 3 + 2
qc = add_quantum_adder(a=3, b=2, n=3)

# run simulation
sim = Aer.get_backend('aer_simulator')
qobj = assemble(transpile(qc, sim))
result = sim.run(qobj).result()
counts = result.get_counts()

print(counts)
plot_histogram(counts)
