import sys
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from qiskit import QuantumCircuit, execute, Aer

class QuantumThread:
    def __init__(self, threshold_0, threshold_1):
        self.threshold_0 = threshold_0
        self.threshold_1 = threshold_1
        self.update_signal = None

    def run(self):
        circuit = QuantumCircuit(1)
        circuit.h(0)
        circuit.measure_all()

        result_str = "Step 1: Apply Hadamard gate to create equal superposition.\n"

        backend = Aer.get_backend('statevector_simulator')
        job = execute(circuit, backend)
        result = job.result()
        statevector = np.array(result.get_statevector(circuit))

        result_str += f"State after Hadamard: {statevector}\n"

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuit, backend, shots=1000)
        result = job.result()
        counts = result.get_counts(circuit)
        prob_0 = counts.get('0', 0) / 1000
        prob_1 = counts.get('1', 0) / 1000

        if self.update_signal:
            self.update_signal(result_str, statevector, np.array([prob_0, prob_1]), prob_0, prob_1)

class QuantumApp:
    def __init__(self, root):
        self.root = root
        root.title("Hadamard Gate Simulator")

        self.explanation_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
        self.explanation_text.pack()

        self.threshold_label_0 = tk.Label(root, text="Enter superposition percentage for |0⟩:")
        self.threshold_label_0.pack()

        self.threshold_entry_0 = tk.Entry(root)
        self.threshold_entry_0.pack()

        self.threshold_label_1 = tk.Label(root, text="Enter superposition percentage for |1⟩:")
        self.threshold_label_1.pack()

        self.threshold_entry_1 = tk.Entry(root)
        self.threshold_entry_1.pack()

        self.calculate_button = tk.Button(root, text="Calculate Hadamard", command=self.start_quantum_thread)
        self.calculate_button.pack()

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    def start_quantum_thread(self):
        threshold_0 = float(self.threshold_entry_0.get())
        threshold_1 = float(self.threshold_entry_1.get())

        self.calculate_button["state"] = tk.DISABLED
        self.explanation_text.delete(1.0, tk.END)
        self.figure.clear()

        self.quantum_thread = QuantumThread(threshold_0, threshold_1)
        self.quantum_thread.update_signal = self.update_explanation_and_graph
        self.quantum_thread.run()

    def update_explanation_and_graph(self, text, statevector, measured_probs, prob_0, prob_1):
        self.explanation_text.insert(tk.END, text + "\n")
        
        ax = self.figure.add_subplot(121)
        ax.bar(["|0⟩", "|1⟩"], np.abs(statevector) ** 2)
        ax.set_title("State Vector Amplitudes")
        ax.set_ylabel("Probability")
        
        ax2 = self.figure.add_subplot(122)
        ax2.bar(["|0⟩", "|1⟩"], measured_probs)
        ax2.set_title("Measured Probabilities")
        ax2.set_ylabel("Probability")
        
        self.canvas.draw()

        self.explanation_text.insert(tk.END, f"Measured probability of |0⟩: {prob_0:.2f}\n")
        self.explanation_text.insert(tk.END, f"Measured probability of |1⟩: {prob_1:.2f}\n")

        self.calculate_button["state"] = tk.NORMAL

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumApp(root)
    root.mainloop()
