import cv2

def draw_keypoints(img, keypoints):
    return cv2.drawKeypoints(img, keypoints, None, color=(0,255,0))