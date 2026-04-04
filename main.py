import configparser
import os
import cv2
from lib.denoise import denoise_image

def main():
    # 讀取設定
    config = configparser.ConfigParser()
    config.read("config.ini")

    image_path = config["INPUT"]["image_path"]
    save_path = config["OUTPUT"]["save_path"]
    strength = int(config["PARAMS"].get("denoise_strength", 30))
    edge_preserve = float(config["PARAMS"].get("edge_preserve", 0.8))
    algorithm = config["PARAMS"].get("algorithm", "nl_means")

    # 確保輸出資料夾存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 讀取影像
    image = cv2.imread(image_path)
    if image is None:
        print(f"無法讀取影像: {image_path}")
        return

    # 影像降噪
    denoised = denoise_image(image, strength=strength, edge_preserve=edge_preserve, algorithm=algorithm)

    # 顯示結果
    cv2.imshow("Original", image)
    cv2.imshow("Denoised", denoised)
    cv2.imwrite(save_path, denoised)
    print(f"降噪後影像已保存: {save_path}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()