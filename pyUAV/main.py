import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from drone_sim import DroneSim
from map_widget import MapWidget
from control_widget import ControlWidget
from status_widget import StatusWidget
from param_widget import ParamWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python MissionPlanner 原型")
        self.setGeometry(100,100,1200,800)

        self.drone = DroneSim()
        self.map_widget = MapWidget(self.drone)
        self.status_widget = StatusWidget(self.drone)
        self.control_widget = ControlWidget(self.drone)

        self.param_btn = QPushButton("開啟參數列表")
        self.param_btn.clicked.connect(self.open_param_widget)
        self.param_widget = None

        self.exit_btn = QPushButton("離開 / 關閉")
        self.exit_btn.clicked.connect(self.close_app)

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)
        layout.addWidget(self.status_widget)
        layout.addWidget(self.control_widget)
        layout.addWidget(self.param_btn)
        layout.addWidget(self.exit_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_param_widget(self):
        if self.param_widget is None:
            self.param_widget = ParamWidget(self.drone)
        self.param_widget.show()
        self.param_widget.raise_()

    def close_app(self):
        if self.param_widget:
            self.param_widget.close()
        self.close()
        QApplication.quit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
