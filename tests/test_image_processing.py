# test_image_processing.py

import os
import configparser
import cv2
from lib import image_io, preprocessing, utils

def test_image_processing(input_path, output_path, resize_width=None, resize_height=None, gray_scale=False, denoise_method='gaussian', diff_path=None):
    print(f"讀取影像: {input_path}")
    
    # 1️⃣ 讀原始影像 (保留彩色，用於 diff)
    original_img = image_io.load_image(input_path, gray=False)
    print(f"原始影像尺寸: {original_img.shape}")

    # 2️⃣ Resize（如果 config 沒指定，保持原尺寸）
    if resize_width is not None and resize_height is not None:
        img_resized = preprocessing.resize(original_img, resize_width, resize_height)
        print(f"Resize 後尺寸: {img_resized.shape}")
    else:
        img_resized = original_img
        print("未指定 resize，保留原尺寸")

    # 3️⃣ 灰階
    if gray_scale:
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        print(f"灰階影像尺寸: {img_gray.shape}")
    else:
        img_gray = img_resized
        print("保留彩色影像")

    # 4️⃣ 去噪
    img_denoise = preprocessing.denoise(img_gray, method=denoise_method)
    print("去噪完成")

    # 5️⃣ 確保輸出資料夾存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 6️⃣ 存檔
    cv2.imwrite(output_path, img_denoise)
    print(f"處理後影像已存檔: {output_path}")

    # 7️⃣ 產生 diff.jpg（如果有指定 diff_path）
    if diff_path:
        diff_dir = os.path.dirname(diff_path)
        if diff_dir and not os.path.exists(diff_dir):
            os.makedirs(diff_dir)
        utils.save_diff_image(original_img, img_denoise, diff_path)
        print(f"Diff image saved to {diff_path}")


if __name__ == "__main__":
    # 讀取 config.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

    input_path = config['IMAGE']['input_path']
    output_path = config['IMAGE']['output_path']

    # 嘗試讀 resize，如果沒設定就使用 None
    resize_width = config['IMAGE'].getint('resize_width', fallback=None)
    resize_height = config['IMAGE'].getint('resize_height', fallback=None)
    gray_scale = config['IMAGE'].getboolean('gray_scale', fallback=False)
    denoise_method = config['PREPROCESSING'].get('denoise_method', fallback='gaussian')
    diff_path = config['IMAGE'].get('diff_path', None)

    test_image_processing(input_path, output_path,
                          resize_width=resize_width,
                          resize_height=resize_height,
                          gray_scale=gray_scale,
                          denoise_method=denoise_method,
                          diff_path=diff_path)