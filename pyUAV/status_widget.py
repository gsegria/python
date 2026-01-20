from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer

class StatusWidget(QWidget):
    def __init__(self, drone):
        super().__init__()
        self.drone = drone
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(200)

    def update_status(self):
        text = f"模式: {self.drone.flight_mode}\nARM: {self.drone.armed}\nLat: {self.drone.lat:.6f}\nLon: {self.drone.lon:.6f}\nAlt: {self.drone.alt:.1f} m"
        self.label.setText(text)
