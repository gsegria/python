import cv2

def extract_features(img, method='ORB', max_features=500):
    if method.upper() == 'ORB':
        orb = cv2.ORB_create(nfeatures=max_features)
        keypoints, descriptors = orb.detectAndCompute(img, None)
    elif method.upper() == 'SIFT':
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(img, None)
    else:
        keypoints, descriptors = [], None
    return keypoints, descriptors