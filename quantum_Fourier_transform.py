from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import QFT

def prepare_state():
    qc = QuantumCircuit(4, 4)
    qc.h(0)  # Creates (|0000⟩ + |1000⟩)/√2
    return qc

def apply_qft_and_measure(qc):
    qft = QFT(num_qubits=4, do_swaps=True).to_gate()
    qc.append(qft, range(4))  # Apply QFT
    qc.measure(range(4), range(4))  # Measure all qubits
    return qc

qc = prepare_state()
qc = apply_qft_and_measure(qc)

simulator = Aer.get_backend("qasm_simulator")
job = execute(qc, backend=simulator, shots=1024)
counts = job.result().get_counts()

print("Results:")
for state in sorted(counts):
    print(f"{state}: {counts[state]}")
