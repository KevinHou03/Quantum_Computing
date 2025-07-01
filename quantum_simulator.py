from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

IBM_TOKEN = "abe0cb28a30e5cfdabbdcffefe7e7990928858b15021af62ea7dc63219b498d3704a8f7183e0cc6c83c8055e39368042728455c0f973f55287b8047604ff3db1"  # 替换为你的 IBM 账户 Token
BACKEND_NAME = "ibm_brisbane"


qasm = """
 OPENQASM 2.0;
 include "qelib1.inc";

 gate sum cin, a, b {
     cx a, b;
     cx cin, b;
 }

 gate carry cin, a, b, cout {
     ccx a, b, cout;
     cx a, b;
     ccx cin, b, cout;
 }

 gate carrydg cin, a, b, cout {
     ccx cin, b, cout;
     cx a, b;
     ccx a, b, cout;
 }

 qreg c[2];  // 
 qreg a[2];  //
 qreg b[3];  // 
 creg bc[3]; // 


 x a[0]; // a = 01
 x b[0]; // b = 11
 x b[1];

 carry c[0], a[0], b[0], c[1];  
 carry c[1], a[1], b[1], b[2]; 

 cx a[1], b[1];
 sum c[1], a[1], b[1];

 carrydg c[0], a[0], b[0], c[1];
 sum c[0], a[0], b[0];

 measure b -> bc;
 """


circuit = QuantumCircuit.from_qasm_str(qasm)


def simulate_circuit(qc):
    simulator = AerSimulator()
    transpiled_circuit = transpile(qc, simulator)
    result = simulator.run(transpiled_circuit, shots=1024).result()
    counts = result.get_counts(transpiled_circuit)

    # 显示结果
    plot_histogram(counts).show()
    return counts


sim_counts = simulate_circuit(circuit)
print("Simulated counts:", sim_counts)

service = QiskitRuntimeService(channel="ibm_quantum", token=IBM_TOKEN)
backend = service.backend(BACKEND_NAME)
print(f"Selected backend: {backend.name}")

pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
isa_circuit = pm.run(circuit)

sampler = Sampler(backend)

job = sampler.run([isa_circuit])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")

result = job.result()
pub_result = result[0]
values = pub_result.get("__value__")
datavalues = values.get("data_prep")

print("Quantum device results:", datavalues.c.get_counts())

