# godcore_interface.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
import vispy.scene
from vispy.scene import visuals, SceneCanvas
import numpy as np
import json
import time

class GodcoreInterface(QMainWindow):
    def __init__(self, memory):
        super().__init__()
        self.memory = memory
        self.setWindowTitle("GODCORE INTERFACE v2.0 - Victor Online")
        self.setGeometry(100, 100, 1400, 900)

        # Main Layout
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Status Label
        self.status_label = QLabel("Connecting to Victor...")
        layout.addWidget(self.status_label)

        # 3D Canvas
        self.canvas = SceneCanvas(keys='interactive', show=True)
        layout.addWidget(self.canvas.native)
        self.view = self.canvas.central_widget.add_view()

        # Neural Web (Glyphs)
        self.glyph_nodes = visuals.Markers()
        self.glyph_nodes.set_data(np.random.randn(30, 3), symbol='sphere', size=15, edge_color='cyan')
        self.view.add(self.glyph_nodes)

        # Dissonance Flare
        self.dissonance_flare = visuals.Markers()
        self.dissonance_flare.set_data(np.zeros((1, 3)), symbol='ring', size=60, edge_color='red', visible=False)
        self.view.add(self.dissonance_flare)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_from_victor)
        self.timer.start(1000)

    def update_from_victor(self):
        try:
            directives = self.memory.retrieve("core/directives")
            if directives:
                self.status_label.setText(f"Directives: {', '.join(directives)}")

            if np.random.rand() < 0.2:
                pos = np.random.randn(1, 3) * 2
                self.dissonance_flare.set_data(pos, visible=True)
                print(f"[GODCORE] COGNITIVE DISSONANCE DETECTED")
            else:
                self.dissonance_flare.visible = False

            self.glyph_nodes.set_data(self.glyph_nodes.pos + np.random.randn(30, 3) * 0.02)
        except Exception as e:
            print(f"[GODCORE] Interface error: {e}")

if __name__ == "__main__":
    memory = VictorMemory()
    app = QApplication(sys.argv)
    window = GodcoreInterface(memory)
    window.show()
    app.exec_()
