import os
import configparser
from lib import image_io

def test_load_save():
    # 1️⃣ 讀取 config.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

    input_path = config['IMAGE']['input_path']
    output_path = config['IMAGE']['output_path']
    gray_scale = config['IMAGE'].getboolean('gray_scale', fallback=True)

    # 2️⃣ 確保輸出資料夾存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 3️⃣ 讀影像
    img = image_io.load_image(input_path, gray=gray_scale)

    # 4️⃣ 存影像
    image_io.save_image(img, output_path)

    print(f"Test passed: {input_path} -> {output_path}")


if __name__ == "__main__":
    test_load_save()