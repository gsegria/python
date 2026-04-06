import configparser
import os
import cv2
from lib.image_pipeline import process_image_pipeline
from lib import image_io, utils, video_io


def main():
    # 讀取設定
    config = configparser.ConfigParser()
    config.read('config.ini')

    mode = config['GENERAL'].get('mode', 'auto').lower()
    is_video = False

    # 根據 mode 決定運行類型
    if mode == 'auto':
        # 自動判斷副檔名（影片副檔名）
        auto_input = config['IMAGE']['input_path']
        is_video = auto_input.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    elif mode == 'video':
        is_video = True
    elif mode == 'image':
        is_video = False
    else:
        print(f"Unknown mode '{mode}', fallback to auto")
        auto_input = config['IMAGE']['input_path']
        is_video = auto_input.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

    if is_video:
        # 影片模式
        input_path = config['VIDEO']['input_path']
        output_dir = config['VIDEO']['output_path']  # 必須是資料夾
        print("=== Video Mode ===")
        video_io.process_video(input_path, output_dir, config)
    else:
        # 圖片模式
        input_path = config['IMAGE']['input_path']
        output_path = config['IMAGE']['output_path']
        diff_path = config['IMAGE'].get('diff_path', './data/output/diff.jpg')

        print("=== Image Mode ===")
        img = image_io.load_image(input_path, gray=False)
        original_img, img_final = process_image_pipeline(img, config)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image_io.save_image(img_final, output_path)

        os.makedirs(os.path.dirname(diff_path), exist_ok=True)
        utils.save_diff_image(original_img, img_final, diff_path)

        print(f"Processed image saved to {output_path}")
        print(f"Diff image saved to {diff_path}")


if __name__ == "__main__":
    main()