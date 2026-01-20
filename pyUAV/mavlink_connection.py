# mavlink_connection.py
from pymavlink import mavutil
from config import MAVLINK_CONNECTION, MAVLINK_BAUDRATE

class MAVLinkConnection:
    def __init__(self):
        self.master = None
        self.target_system = 1
        self.target_component = 1

    def connect(self):
        try:
            self.master = mavutil.mavlink_connection(MAVLINK_CONNECTION, baud=MAVLINK_BAUDRATE)
            self.master.wait_heartbeat()
            print("已連線 Cube Orange")
        except Exception as e:
            print("連線失敗:", e)
            self.master = None

    def arm(self):
        if not self.master:
            print("尚未連線")
            return
        self.master.arducopter_arm()
        print("已解鎖")

    def takeoff(self, alt=10):
        if not self.master:
            print("尚未連線")
            return
        self.master.simple_takeoff(alt)
        print(f"起飛至 {alt} m")

    def land(self):
        if not self.master:
            print("尚未連線")
            return
        self.master.set_mode("LAND")
        print("降落中")

    def set_mode(self, mode):
        if not self.master:
            print("尚未連線")
            return
        self.master.set_mode(mode)
        print(f"切換模式: {mode}")

    def get_param_list(self):
        if not self.master:
            print("尚未連線")
            return {}
        self.master.mav.param_request_list_send(self.target_system, self.target_component)
        params = {}
        while True:
            msg = self.master.recv_match(type='PARAM_VALUE', blocking=True, timeout=1)
            if not msg:
                break
            params[msg.param_id.decode()] = msg.param_value
            if msg.param_index == msg.param_count - 1:
                break
        return params

    def set_param(self, param_id, value):
        if not self.master:
            print("尚未連線")
            return
        self.master.mav.param_set_send(
            self.target_system,
            self.target_component,
            param_id.encode(),
            value,
            mavutil.mavlink.MAV_PARAM_TYPE_REAL32
        )
