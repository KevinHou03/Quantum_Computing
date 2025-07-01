from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

service = QiskitRuntimeService(channel="ibm_quantum", token="abe0cb28a30e5cfdabbdcffefe7e7990928858b15021af62ea7dc63219b498d3704a8f7183e0cc6c83c8055e39368042728455c0f973f55287b8047604ff3db1")

# all available backends
#
qasm = """
OPENQASM 2.0;
include "qelib1.inc";

// Define the quantum sum gate.
gate sum cin, a, b {
    cx a, b;
    cx cin, b;
}

// Define the quantum carry gate.
gate carry cin, a, b, cout {
    ccx a, b, cout;
    cx a, b;
    ccx cin, b, cout;
}

// Define the inverse of the quantum carry gate.
gate carrydg cin, a, b, cout {
    ccx cin, b, cout;
    cx a, b;
    ccx a, b, cout;
}

// Declare the quantum registers.
qreg c[4];
qreg a[4];
qreg b[5];

// Declare the classical registers.
creg bc[5];

// Set the input states by applying X gates.
x a[1];
x a[2];
x a[3]; // a = 1110
x b[0];
x b[1];
x b[3]; // b = 1011

// Perform quantum addition (|a>|b> becomes |a>|a+b>)
carry c[0], a[0], b[0], c[1];
carry c[1], a[1], b[1], c[2];
carry c[2], a[2], b[2], c[3];
carry c[3], a[3], b[3], b[4];

cx a[3], b[3];
sum c[3], a[3], b[3];

carrydg c[2], a[2], b[2], c[3];
sum c[2], a[2], b[2];

carrydg c[1], a[1], b[1], c[2];
sum c[1], a[1], b[1];

carrydg c[0], a[0], b[0], c[1];
sum c[0], a[0], b[0];

// Measure the sum and store in classical register.
measure b -> bc;
"""

# Load
circuit = QuantumCircuit.from_qasm_str(qasm)

# 2
def simulate_circuit(qc):
    """Simulates the circuit using AerSimulator."""
    simulator = AerSimulator()
    transpiled_circuit = transpile(qc, simulator)
    result = simulator.run(transpiled_circuit).result()
    counts = result.get_counts(transpiled_circuit)

    # plot
    plot_histogram(counts).show()
    return counts

print("Running simulation...")
sim_counts = simulate_circuit(circuit)
print("Simulated counts:", sim_counts)

#3
IBM_TOKEN = "abe0cb28a30e5cfdabbdcffefe7e7990928858b15021af62ea7dc63219b498d3704a8f7183e0cc6c83c8055e39368042728455c0f973f55287b8047604ff3db1"
BACKEND_NAME = "ibm_brisbane"
service = QiskitRuntimeService(channel="ibm_quantum", token=IBM_TOKEN)
backend = service.backend(BACKEND_NAME)
print(f"Selected backend: {backend.name}")
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
isa_circuit = pm.run(circuit)

sampler = Sampler(backend)

# submit the job,
job = sampler.run([isa_circuit])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")

result = job.result()
pub_result = result[0]
values = pub_result.get("__value__")
datavalues = values.get("data_prep")

print("Quantum device results:", datavalues.c.get_counts())

print("Script execution complete!")
