import cv2

def resize(img, width, height):
    return cv2.resize(img, (width, height))

def denoise(img, method='gaussian'):
    if method == 'gaussian':
        return cv2.GaussianBlur(img, (5,5), 0)
    elif method == 'median':
        return cv2.medianBlur(img, 5)
    else:
        return img
    