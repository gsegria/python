import cv2
import numpy as np

def denoise_image(image, strength=30, edge_preserve=0.8, algorithm="nl_means"):
    """
    降噪主函數
    :param image: np.array, 原始影像
    :param strength: int, 降噪強度
    :param edge_preserve: float, 邊緣保護 0~1
    :param algorithm: str, 使用算法 'bilateral' 或 'nl_means'
    :return: np.array, 降噪後影像
    """
    if algorithm == "bilateral":
        # 多次雙邊濾波疊加
        filtered = image.copy()
        for i in range(3):
            filtered = cv2.bilateralFilter(filtered, d=9,
                                           sigmaColor=strength,
                                           sigmaSpace=int(strength * edge_preserve))
        return filtered

    elif algorithm == "nl_means":
        # 非局部均值去噪
        if len(image.shape) == 3 and image.shape[2] == 3:
            # 彩色影像
            denoised = cv2.fastNlMeansDenoisingColored(image,
                                                       None,
                                                       h=strength,
                                                       hColor=strength,
                                                       templateWindowSize=7,
                                                       searchWindowSize=21)
        else:
            # 灰階影像
            denoised = cv2.fastNlMeansDenoising(image,
                                                None,
                                                h=strength,
                                                templateWindowSize=7,
                                                searchWindowSize=21)
        # 邊緣保護 (可選)
        if edge_preserve > 0:
            # 使用拉普拉斯強化邊緣
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            edges = cv2.Laplacian(gray, cv2.CV_64F)
            edges = cv2.convertScaleAbs(edges)
            edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX)
            mask = edges / 255.0 * edge_preserve
            mask = np.expand_dims(mask, axis=2) if len(image.shape) == 3 else mask
            denoised = (denoised * (1 - mask) + image * mask).astype(np.uint8)
        return denoised

    else:
        raise ValueError("Unknown algorithm: choose 'bilateral' or 'nl_means'")