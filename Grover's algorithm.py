from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

n = 2

qc = QuantumCircuit(n, n)
qc.h(range(n))

oracle = QuantumCircuit(n)
oracle.cz(0, 1)
qc = qc.compose(oracle)

diffusion = QuantumCircuit(n)
diffusion.h(range(n))
diffusion.x(range(n))
diffusion.h(1)
diffusion.cx(0, 1)
diffusion.h(1)
diffusion.x(range(n))
diffusion.h(range(n))
qc = qc.compose(diffusion)

qc.measure(range(n), range(n))

simulator = Aer.get_backend('qasm_simulator')
compiled = transpile(qc, simulator)
qobj = assemble(compiled)
result = execute(qc, backend=simulator, shots=1024).result()
counts = result.get_counts()

print("measurement results:", counts)
plot_histogram(counts)
plt.show()
