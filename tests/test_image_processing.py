import os
import configparser
import cv2
from lib import image_io, preprocessing

def test_image_processing(input_path, output_path):
    print(f"讀取影像: {input_path}")
    
    # 1️⃣ 讀影像
    img = image_io.load_image(input_path, gray=False)
    print(f"原始影像尺寸: {img.shape}")

    # 2️⃣ Resize
    width, height = 640, 480
    img_resized = preprocessing.resize(img, width, height)
    print(f"Resize 後尺寸: {img_resized.shape}")

    # 3️⃣ 灰階
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    print(f"灰階影像尺寸: {img_gray.shape}")

    # 4️⃣ 去噪
    img_denoise = preprocessing.denoise(img_gray, method='gaussian')
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

    test_image_processing(input_path, output_path)