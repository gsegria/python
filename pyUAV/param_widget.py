# param_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
import json

class ParamWidget(QWidget):
    def __init__(self, drone):
        super().__init__()
        self.drone = drone
        self.setWindowTitle("Cube Orange+ 參數列表")
        self.setGeometry(200, 200, 700, 800)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 參數表格
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # 按鈕
        self.load_btn = QPushButton("從檔案載入")
        self.load_btn.clicked.connect(self.load_from_file)
        self.save_btn = QPushButton("儲存至檔案")
        self.save_btn.clicked.connect(self.save_to_file)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.save_btn)

        # 初始化 Cube Orange+ 15kg 參數
        self.init_params()
        self.load_params()

    # 初始化真實 MP PARAM
    def init_params(self):
        self.drone.params = {
            "FORMAT_VERSION":120,
            "FRAME_CLASS":1,
            "FRAME_TYPE":1,
            "FLIGHT_OPTIONS":18,
            # ACRO
            "ACRO_BAL_PITCH":1,
            "ACRO_BAL_ROLL":1,
            "ACRO_OPTIONS":0,
            "ACRO_RP_EXPO":0.3,
            "ACRO_RP_RATE":360,
            "ACRO_RP_RATE_TC":0,
            "ACRO_THR_MID":0,
            "ACRO_TRAINER":2,
            "ACRO_Y_EXPO":0,
            "ACRO_Y_RATE":202.5,
            "ACRO_Y_RATE_TC":0,
            # ATC / PID
            "ATC_ANG_PIT_P":4.0,
            "ATC_ANG_RLL_P":4.0,
            "ATC_ANG_YAW_P":4.0,
            "ATC_INPUT_TC":0.12,
            "ATC_RAT_PIT_P":0.12,
            "ATC_RAT_PIT_I":0.12,
            "ATC_RAT_PIT_D":0.003,
            "ATC_RAT_RLL_P":0.12,
            "ATC_RAT_RLL_I":0.12,
            "ATC_RAT_RLL_D":0.003,
            "ATC_RAT_YAW_P":0.16,
            "ATC_RAT_YAW_I":0.016,
            "ATC_RAT_YAW_D":0,
            "ATC_ACCEL_P_MAX":110000,
            "ATC_ACCEL_R_MAX":110000,
            "ATC_ACCEL_Y_MAX":25000,
            "ATC_ANGLE_BOOST":1,
            # MOT / ESC
            "MOT_PWM_MIN":1000,
            "MOT_PWM_MAX":2000,
            "MOT_THST_HOVER":0.44,
            "MOT_THST_EXPO":0.58,
            "MOT_SPIN_ARM":0.07,
            "MOT_SPIN_MIN":0.1,
            "MOT_SPIN_MAX":0.95,
            "MOT_SLEW_UP_TIME":0,
            "MOT_SLEW_DN_TIME":0,
            "MOT_SAFE_DISARM":0,
            "MOT_SAFE_TIME":1,
            "SERVO_DSHOT_ESC":1,
            # BATT / ARM / SAFETY
            "BATT_CAPACITY":22000,
            "BATT_MONITOR":26,
            "BATT_LOW_VOLT":14.8,
            "BATT_ARM_VOLT":15.1,
            "BATT_CRT_VOLT":14.4,
            "ARMING_CHECK":64,
            "ARMING_ACCTHRESH":0.75,
            "ARMING_OPTIONS":0,
            "FS_THR_ENABLE":1,
            "FS_EKF_ACTION":1,
            # EKF / AHRS / COMPASS
            "EK3_ENABLE":1,
            "EK3_PRIMARY":0,
            "EK3_IMU_MASK":3,
            "EK3_SRC1_POSXY":3,
            "EK3_SRC1_POSZ":1,
            "EK3_SRC1_VELXY":3,
            "EK3_SRC1_VELZ":3,
            "EK3_SRC1_YAW":1,
            "AHRS_ORIENTATION":0,
            "AHRS_RP_P":0.2,
            "AHRS_YAW_P":0.2,
            "AHRS_GPS_USE":1,
            "AHRS_COMP_BETA":0.1,
            "AHRS_EKF_TYPE":3,
            "COMPASS_EXTERNAL":1,
            # GPS / CAN
            "CAN_D1_PROTOCOL":1,
            "CAN_D2_PROTOCOL":1,
            "GPS1_TYPE":1,
            "GPS2_TYPE":0,
            "GPS_HDOP_GOOD":150,
            "GPS_GLITCH_RPD":20,
            # RC / RCMAP
            "RCMAP_ROLL":1,
            "RCMAP_PITCH":2,
            "RCMAP_THROTTLE":3,
            "RCMAP_YAW":4,
            "RC1_TRIM":1500,
            "RC2_TRIM":1500,
            "RC3_TRIM":989,
            "RC4_TRIM":1502,
            "RC_OPTIONS":15136,
            "RC_PROTOCOLS":512,
            # FLIGHT MODES
            "FLTMODE1":0,
            "FLTMODE2":2,
            "FLTMODE3":5,
            "FLTMODE4":6,
            "FLTMODE5":21,
            "FLTMODE6":9,
            # Cube Orange+ Hardware
            "BRD_HEAT_TARG":45,
            "BRD_IO_ENABLE":1,
            "MNT_TYPE":0,
            # 其他
            "LOG_BITMASK":65535,
            "OSD_ENABLE":1,
            "SERVO_BLH":0
        }

    # 顯示參數
    def load_params(self):
        try:
            self.table.cellChanged.disconnect()
        except:
            pass

        params = self.drone.params
        self.table.setRowCount(len(params))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Param","Value"])

        for i,(k,v) in enumerate(params.items()):
            self.table.setItem(i,0,QTableWidgetItem(k))
            item = QTableWidgetItem(str(v))
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i,1,item)

        self.table.cellChanged.connect(self.update_param)

    # 更新參數
    def update_param(self, row, col):
        if col != 1:
            return
        item_value = self.table.item(row,1)
        item_param = self.table.item(row,0)
        if not item_value or not item_param:
            return
        key = item_param.text()
        try:
            val = float(item_value.text())
        except ValueError:
            # 輸入非數字恢復原值
            item_value.setText(str(self.drone.params[key]))
            return
        self.drone.params[key] = val

    # 儲存到 JSON
    def save_to_file(self):
        fname,_ = QFileDialog.getSaveFileName(self,"儲存參數","","JSON Files (*.json)")
        if fname:
            with open(fname,"w") as f:
                json.dump(self.drone.params,f,indent=4)
            print(f"參數已儲存至 {fname}")

    # 從 JSON 載入
    def load_from_file(self):
        fname,_ = QFileDialog.getOpenFileName(self,"載入參數","","JSON Files (*.json)")
        if fname:
            with open(fname,"r") as f:
                data = json.load(f)
            for k,v in data.items():
                if k in self.drone.params:
                    self.drone.params[k] = v
            self.load_params()
            print(f"參數已從 {fname} 載入")
