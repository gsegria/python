import configparser
from lib import image_io
import os

def test_load_save():
    # 讀取 config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    input_path = config['IMAGE']['input_path']
    output_path = config['IMAGE']['output_path']

    # 確保輸出資料夾存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 讀影像
    img = image_io.load_image(input_path, gray=True)

    # 存影像
    image_io.save_image(img, output_path)

    print(f"Test passed: {input_path} -> {output_path}")

if __name__ == "__main__":
    test_load_save()