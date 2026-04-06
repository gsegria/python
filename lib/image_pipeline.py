# lib/image_pipeline.py
import cv2
from lib import preprocessing, feature_extraction, utils, detection

def process_image_pipeline(img, config):
    """image pipeline"""

    gray = config['IMAGE'].getboolean('gray_scale', fallback=False)
    resize_w = config['IMAGE'].getint('resize_width', fallback=None)
    resize_h = config['IMAGE'].getint('resize_height', fallback=None)

    denoise_flag = config['PREPROCESSING'].getboolean('denoise', fallback=True)
    denoise_method = config['PREPROCESSING'].get('denoise_method', fallback='gaussian')

    feature_method = config['FEATURE'].get('method', fallback='ORB')
    max_features = config['FEATURE'].getint('max_features', fallback=500)

    original_img = img.copy()

    # Gray
    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize
    if resize_w and resize_h:
        img = preprocessing.resize(img, resize_w, resize_h)

    # Denoise
    if denoise_flag:
        img = preprocessing.denoise(img, method=denoise_method)

    # Feature
    keypoints, descriptors = feature_extraction.extract_features(
        img, method=feature_method, max_features=max_features
    )

    img_with_kp = utils.draw_keypoints(img, keypoints)

    # Detection
    img_detected, contours = detection.detect_objects(img)
    print(f"Detected {len(contours)} objects using detection module.")

    # Combine
    img_final = img_with_kp.copy()
    for cnt in contours:
        cv2.drawContours(img_final, [cnt], -1, (0, 0, 255), 2)

    return original_img, img_final

