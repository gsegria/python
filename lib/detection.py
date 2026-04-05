import cv2

def detect_objects(img, method='contours'):
    """
    簡單物件偵測範例
    method:
        - 'contours' : 透過邊緣/輪廓偵測
    """
    detected_img = img.copy()
    
    if method == 'contours':
        # 轉灰階
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape)==3 else img
        # 邊緣偵測
        edges = cv2.Canny(gray, 50, 150)
        # 找輪廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 畫輪廓
        cv2.drawContours(detected_img, contours, -1, (0,255,0), 2)
    
    return detected_img, contours