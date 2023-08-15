import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qiskit import QuantumCircuit, execute, Aer

import numpy as np
from qiskit import QuantumCircuit, execute, Aer

import numpy as np
from qiskit import QuantumCircuit, execute, Aer

class QuantumThread(QThread):
    update_signal = pyqtSignal(str, np.ndarray, np.ndarray, float, float)

    def __init__(self, threshold_0, threshold_1):
        super().__init__()
        self.threshold_0 = threshold_0
        self.threshold_1 = threshold_1

    def run(self):
        # Simulate Hadamard gate step by step
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
        
        self.update_signal.emit(result_str, statevector, np.array([prob_0, prob_1]), prob_0, prob_1)

class QuantumApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hadamard Gate Simulator")
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        
        self.threshold_label_0 = QLabel("Enter superposition percentage for |0⟩:")
        self.threshold_entry_0 = QLineEdit()
        
        self.threshold_label_1 = QLabel("Enter superposition percentage for |1⟩:")
        self.threshold_entry_1 = QLineEdit()
        
        self.calculate_button = QPushButton("Calculate Hadamard")
        self.calculate_button.clicked.connect(self.start_quantum_thread)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.threshold_label_0)
        layout.addWidget(self.threshold_entry_0)
        layout.addWidget(self.threshold_label_1)
        layout.addWidget(self.threshold_entry_1)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.explanation_text)
        layout.addWidget(self.canvas)
        
        self.central_widget.setLayout(layout)
    
    def start_quantum_thread(self):
        threshold_0 = float(self.threshold_entry_0.text())
        threshold_1 = float(self.threshold_entry_1.text())
        
        self.calculate_button.setEnabled(False)
        self.explanation_text.clear()
        self.figure.clear()
        
        self.quantum_thread = QuantumThread(threshold_0, threshold_1)
        self.quantum_thread.update_signal.connect(self.update_explanation_and_graph)
        self.quantum_thread.finished.connect(self.thread_finished)
        
        self.quantum_thread.start()
    
    def update_explanation_and_graph(self, text, statevector, measured_probs, prob_0, prob_1):
        self.explanation_text.append(text)
        
        ax = self.figure.add_subplot(121)
        ax.bar(["|0⟩", "|1⟩"], np.abs(statevector) ** 2)
        ax.set_title("State Vector Amplitudes")
        ax.set_ylabel("Probability")
        
        ax2 = self.figure.add_subplot(122)
        ax2.bar(["|0⟩", "|1⟩"], measured_probs)
        ax2.set_title("Measured Probabilities")
        ax2.set_ylabel("Probability")
        
        self.canvas.draw()
        
        self.explanation_text.append(f"Measured probability of |0⟩: {prob_0:.2f}")
        self.explanation_text.append(f"Measured probability of |1⟩: {prob_1:.2f}")
    
    def thread_finished(self):
        self.calculate_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuantumApp()
    window.show()
    sys.exit(app.exec_())
