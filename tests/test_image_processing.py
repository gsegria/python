import os
import configparser
import cv2
from lib import image_io, preprocessing

def test_image_processing(input_path, output_path, resize_width=None, resize_height=None, gray_scale=False, denoise_method='gaussian'):
    print(f"讀取影像: {input_path}")
    
    # 1️⃣ 讀影像
    img = image_io.load_image(input_path, gray=False)
    print(f"原始影像尺寸: {img.shape}")

    # 2️⃣ Resize（如果 config 沒指定，保持原尺寸）
    if resize_width is not None and resize_height is not None:
        img_resized = preprocessing.resize(img, resize_width, resize_height)
        print(f"Resize 後尺寸: {img_resized.shape}")
    else:
        img_resized = img
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

    test_image_processing(input_path, output_path,
                          resize_width=resize_width,
                          resize_height=resize_height,
                          gray_scale=gray_scale,
                          denoise_method=denoise_method)