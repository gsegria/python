import cv2
import os

def save_diff_image(img1, img2, diff_path):
    """
    計算兩張影像差異，存檔
    img1, img2: BGR numpy arrays
    diff_path: 儲存路徑
    """
    # 尺寸統一
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # 計算差異
    diff = cv2.absdiff(img1, img2)

    # 儲存
    diff_dir = os.path.dirname(diff_path)
    if diff_dir and not os.path.exists(diff_dir):
        os.makedirs(diff_dir)
    cv2.imwrite(diff_path, diff)
    print(f"Diff image saved to {diff_path}")

def draw_keypoints(img, keypoints):
    return cv2.drawKeypoints(img, keypoints, None, color=(0,255,0))