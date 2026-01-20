# drone_sim.py
import threading
import time

class DroneSim:
    def __init__(self):
        self.lat, self.lon, self.alt = 25.04, 121.55, 0
        self.flight_mode = "STANDBY"
        self.armed = False
        self.waypoints = []
        self.flight_path = []
        self.speed = 0.0005
        self.descent_speed = 0.2

        # 初始化參數 (Cube Orange 15kg Quad X)
        self.params = {
            "MOT_THST_HOVER":0.44,
            "ATC_RAT_PIT_P":0.12,
            "ATC_RAT_PIT_I":0.12,
            "ATC_RAT_PIT_D":0.003,
            "ATC_RAT_RLL_P":0.12,
            "ATC_RAT_RLL_I":0.12,
            "ATC_RAT_RLL_D":0.003,
            "ATC_RAT_YAW_P":0.16,
            "ATC_RAT_YAW_I":0.016,
            "ATC_RAT_YAW_D":0,
        }

    def get_param_list(self):
        return self.params.copy()

    def set_param(self, key, value):
        self.params[key] = value
        print(f"Set param {key}={value}")

    def arm(self):
        self.armed = True
        print("解鎖完成")

    def takeoff(self, alt=10):
        if not self.armed:
            print("請先解鎖")
            return
        self.alt = alt
        self.flight_mode = "GUIDED"
        print(f"起飛至 {alt} m")

    def land(self):
        if self.alt <= 0: return
        self.flight_mode = "LAND"
        print("降落中")
        threading.Thread(target=self._descent).start()

    def _descent(self):
        while self.alt > 0:
            self.alt -= self.descent_speed
            if self.alt < 0: self.alt = 0
            time.sleep(0.1)
        self.flight_mode = "STANDBY"
        print("降落完成")

    def set_mode(self, mode):
        self.flight_mode = mode
        print(f"切換模式: {mode}")

    def start_mission(self):
        def fly():
            for wp in self.waypoints:
                while abs(self.lat - wp[0]) > 0.00001 or abs(self.lon - wp[1]) > 0.00001:
                    self.lat += (wp[0]-self.lat)*self.speed
                    self.lon += (wp[1]-self.lon)*self.speed
                    self.flight_path.append((self.lat,self.lon))
                    time.sleep(0.05)
            print("任務完成")
        threading.Thread(target=fly).start()
