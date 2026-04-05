import configparser
from lib import image_io, preprocessing, feature_extraction, utils, detection

def main():
    # 讀取設定
    config = configparser.ConfigParser()
    config.read('config.ini')

    # IMAGE 設定
    input_path = config['IMAGE']['input_path']
    output_path = config['IMAGE']['output_path']
    resize_w = int(config['IMAGE']['resize_width'])
    resize_h = int(config['IMAGE']['resize_height'])
    gray = config.getboolean('IMAGE', 'gray_scale')

    # PREPROCESSING 設定
    denoise_flag = config.getboolean('PREPROCESSING', 'denoise')
    denoise_method = config['PREPROCESSING']['denoise_method']

    # FEATURE 設定
    feature_method = config['FEATURE']['method']
    max_features = int(config['FEATURE']['max_features'])

    # 讀影像
    img = image_io.load_image(input_path, gray=gray)

    # 前處理
    img = preprocessing.resize(img, resize_w, resize_h)
    if denoise_flag:
        img = preprocessing.denoise(img, method=denoise_method)

    # 特徵萃取
    keypoints, descriptors = feature_extraction.extract_features(
        img, method=feature_method, max_features=max_features
    )

    # 視覺化特徵
    img_with_kp = utils.draw_keypoints(img, keypoints)

    # 物件偵測
    img_detected, contours = detection.detect_objects(img)
    print(f"Detected {len(contours)} objects using detection module.")

    # 合併特徵與偵測結果（疊加輪廓在特徵點圖上）
    img_final = img_with_kp.copy()
    for cnt in contours:
        import cv2
        cv2.drawContours(img_final, [cnt], -1, (0,0,255), 2)  # 紅色輪廓

    # 存檔
    image_io.save_image(img_final, output_path)
    print(f"Processed image saved to {output_path}")

if __name__ == "__main__":
    main()