# map_widget.py
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QUrl
import os

class PyJSBridge(QObject):
    updateDrone = pyqtSignal(float,float,float)
    def __init__(self, drone):
        super().__init__()
        self.drone = drone

    @pyqtSlot(float,float)
    def addWaypoint(self,lat,lon):
        self.drone.waypoints.append((lat,lon))
        print(f"新增航點: {lat},{lon}")

    @pyqtSlot(int,float,float)
    def updateWaypoint(self,index,lat,lon):
        if 0<=index<len(self.drone.waypoints):
            self.drone.waypoints[index]=(lat,lon)
            print(f"更新航點 {index}: {lat},{lon}")

class MapWidget(QWidget):
    def __init__(self, drone):
        super().__init__()
        self.drone = drone
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.view = QWebEngineView()
        layout.addWidget(self.view)

        self.channel = QWebChannel()
        self.bridge = PyJSBridge(self.drone)
        self.channel.registerObject("pyjs", self.bridge)
        self.view.page().setWebChannel(self.channel)

        html_path = os.path.abspath("map.html")
        self.view.load(QUrl.fromLocalFile(html_path))

        # 定時更新飛機位置
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_drone_pos)
        self.timer.start(100)

    def send_drone_pos(self):
        # emit 三個值: lat, lon, alt
        self.bridge.updateDrone.emit(self.drone.lat, self.drone.lon, self.drone.alt)
