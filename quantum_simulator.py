# quantum_simulator.py
from qiskit import QuantumCircuit, Aer, transpile, assemble

def simulate_quantum_circuit(threshold_0, threshold_1):
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()

    simulator = Aer.get_backend('qasm_simulator')
    job = assemble(transpile(qc, simulator), shots=1000)
    result = simulator.run(job).result()
    counts = result.get_counts()
    prob_0 = counts.get('0', 0) / 1000
    prob_1 = counts.get('1', 0) / 1000

    explanation = f"Step 1: Apply Hadamard gate to create equal superposition.\n" \
                  f"Step 2: Measuring |0⟩ probability: {prob_0:.2f} (Threshold: {threshold_0:.2f})\n" \
                  f"Step 3: Measuring |1⟩ probability: {prob_1:.2f} (Threshold: {threshold_1:.2f})"
    
    return prob_0, prob_1, explanation
