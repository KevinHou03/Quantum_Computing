from qiskit import QuantumCircuit, Aer, execute
from numpy import pi
import numpy as np

# 定义 Bell pair
def create_bell_pair(circuit):
    circuit.h(1)
    circuit.cx(1, 0)

def apply_measurement_basis(circuit, setting, qubit):
    if setting == "A":       # Z basis
        pass
    elif setting == "A'":    # X basis
        circuit.h(qubit)
    elif setting == "B":     # (T H S) dagger = S† H† T†
        circuit.tdg(qubit)
        circuit.h(qubit)
        circuit.sdg(qubit)
    elif setting == "B'":    # X basis
        circuit.h(qubit)

def build_chsh_circuit(a_basis, b_basis):
    qc = QuantumCircuit(2, 2)
    create_bell_pair(qc)
    apply_measurement_basis(qc, a_basis, 1)  # Alice = qubit 1
    apply_measurement_basis(qc, b_basis, 0)  # Bob = qubit 0
    qc.measure(1, 0)  # Alice's
    qc.measure(0, 1)  # Bob's
    return qc

#计算 E(ab)
def compute_expectation(counts):
    shots = sum(counts.values())
    E = 0
    for bitstring, count in counts.items():
        a = int(bitstring[1])  # c0 -> Alice
        b = int(bitstring[0])  # c1 -> Bob
        parity = 1 if a == b else -1
        E += parity * count
    return E / shots

#所有测量组合
settings = [("A", "B"), ("A", "B'"), ("A'", "B"), ("A'", "B'")]
simulator = Aer.get_backend('qasm_simulator')

results = []
for a, b in settings:
    qc = build_chsh_circuit(a, b)
    qc.name = f"{a}{b}"
    job = execute(qc, simulator, shots=8192)
    counts = job.result().get_counts()
    E = compute_expectation(counts)
    print(f"E({a}, {b}) = {E:.4f}")
    results.append(E)

# 计算S
S = results[0] + results[1] + results[2] - results[3]
print(f"\nCHSH S = {S:.4f}")
