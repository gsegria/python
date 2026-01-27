import psutil
import platform

def detect_interface():
    """
    自動偵測當前主要網路介面類型 (Windows / Linux 支援)
    
    回傳:
        interface_type: 'Wi-Fi', 'USB', 'Wired', '5G', 'Unknown'
        interface_name: 系統介面名稱
    """
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    system = platform.system().lower()  # windows / linux / darwin

    for name, addrs in interfaces.items():
        # 檢查介面是否啟用
        if name not in stats or not stats[name].isup:
            continue

        lname = name.lower()

        # ===== 判斷規則 =====
        # Wi-Fi / WLAN
        if 'wl' in lname or 'wifi' in lname:
            return 'Wi-Fi', name
        # USB 網卡
        if 'usb' in lname:
            return 'USB', name
        # 有線網卡
        if 'eth' in lname or 'en' in lname or 'ethernet' in lname:
            return 'Wired', name
        # 行動網路 / 5G 模組
        if 'wwan' in lname or 'rmnet' in lname:
            return '5G', name

        # Windows 特殊判斷
        if system == 'windows':
            if 'wi-fi' in lname or 'wireless' in lname:
                return 'Wi-Fi', name
            
            if 'local area connection' in lname:
                return 'Wired', name

    # 沒找到任何已啟用的介面
    return 'Unknown', 'N/A'


# ===== 測試程式 =====
if __name__ == "__main__":
    iface_type, iface_name = detect_interface()
    print(f"偵測到介面: {iface_type} ({iface_name})")
