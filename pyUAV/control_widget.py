from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ControlWidget(QWidget):
    def __init__(self, drone):
        super().__init__()
        self.drone = drone
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.arm_btn = QPushButton("解鎖")
        self.arm_btn.clicked.connect(self.drone.arm)
        layout.addWidget(self.arm_btn)

        self.takeoff_btn = QPushButton("起飛 10m")
        self.takeoff_btn.clicked.connect(lambda: self.drone.takeoff(10))
        layout.addWidget(self.takeoff_btn)

        self.land_btn = QPushButton("降落")
        self.land_btn.clicked.connect(self.drone.land)
        layout.addWidget(self.land_btn)

        self.start_mission_btn = QPushButton("開始任務")
        self.start_mission_btn.clicked.connect(self.drone.start_mission)
        layout.addWidget(self.start_mission_btn)
