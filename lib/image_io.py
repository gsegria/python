import cv2

def load_image(path, gray=False):
    flag = cv2.IMREAD_GRAYSCALE if gray else cv2.IMREAD_COLOR
    img = cv2.imread(path, flag)
    if img is None:
        raise FileNotFoundError(f"Cannot load image from {path}")
    return img

def save_image(img, path):
    cv2.imwrite(path, img)