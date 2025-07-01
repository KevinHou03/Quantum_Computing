from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from math import pi

qc = QuantumCircuit(7, 3)

def u_13(circuit, a, b, c_, d, control):
    circuit.cswap(control, c_, d)
    circuit.cswap(control, b, c_)
    circuit.cswap(control, a, b)
    circuit.cx(control, a)
    circuit.cx(control, b)
    circuit.cx(control, c_)
    circuit.cx(control, d)

qc.h(4)
qc.h(5)
qc.h(6)

qc.x(0)

u_13(qc, 3, 2, 1, 0, 4)
u_13(qc, 3, 2, 1, 0, 5)
u_13(qc, 3, 2, 1, 0, 5)
u_13(qc, 3, 2, 1, 0, 6)
u_13(qc, 3, 2, 1, 0, 6)
u_13(qc, 3, 2, 1, 0, 6)
u_13(qc, 3, 2, 1, 0, 6)

qc.swap(4, 6)
qc.h(4)
qc.cp(-pi / 2, 4, 5)
qc.cp(-pi / 4, 4, 6)
qc.h(5)
qc.cp(-pi / 2, 5, 6)
qc.h(6)

qc.measure(4, 0)
qc.measure(5, 1)
qc.measure(6, 2)

simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()

plot_histogram(counts)
plt.title("QPE Result for a = 13 mod 15 (custom u_13)")
plt.show()