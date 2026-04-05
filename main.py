import configparser
import os
import cv2
from lib import image_io, preprocessing, feature_extraction, utils, detection

def main():
    # 讀取 config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # IMAGE 設定
    input_path = config['IMAGE']['input_path']
    output_path = config['IMAGE']['output_path']
    diff_path = config['IMAGE'].get('diff_path', './data/output/diff.jpg')
    gray = config['IMAGE'].getboolean('gray_scale', fallback=False)

    # resize 可選，沒設定就保留原尺寸
    resize_w = config['IMAGE'].getint('resize_width', fallback=None)
    resize_h = config['IMAGE'].getint('resize_height', fallback=None)

    # PREPROCESSING 設定
    denoise_flag = config['PREPROCESSING'].getboolean('denoise', fallback=True)
    denoise_method = config['PREPROCESSING'].get('denoise_method', fallback='gaussian')

    # FEATURE 設定
    feature_method = config['FEATURE'].get('method', fallback='ORB')
    max_features = config['FEATURE'].getint('max_features', fallback=500)

    # 1️⃣ 讀影像
    img = image_io.load_image(input_path, gray=gray)
    original_img = img.copy()  # 用於 diff

    # 2️⃣ Resize
    if resize_w and resize_h:
        img = preprocessing.resize(img, resize_w, resize_h)

    # 3️⃣ 去噪
    if denoise_flag:
        img = preprocessing.denoise(img, method=denoise_method)

    # 4️⃣ 特徵萃取
    keypoints, descriptors = feature_extraction.extract_features(
        img, method=feature_method, max_features=max_features
    )

    # 5️⃣ 畫特徵點
    img_with_kp = utils.draw_keypoints(img, keypoints)

    # 6️⃣ 物件偵測
    img_detected, contours = detection.detect_objects(img)
    print(f"Detected {len(contours)} objects using detection module.")

    # 7️⃣ 合併特徵與偵測結果
    img_final = img_with_kp.copy()
    for cnt in contours:
        cv2.drawContours(img_final, [cnt], -1, (0,0,255), 2)  # 紅色輪廓

    # 8️⃣ 存檔最終影像
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image_io.save_image(img_final, output_path)
    print(f"Processed image saved to {output_path}")

    # 9️⃣ 產生 diff.jpg
    os.makedirs(os.path.dirname(diff_path), exist_ok=True)
    utils.save_diff_image(original_img, img_final, diff_path)
    print(f"Diff image saved to {diff_path}")

if __name__ == "__main__":
    main()