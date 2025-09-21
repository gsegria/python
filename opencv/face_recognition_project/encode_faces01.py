import face_recognition
import cv2
import os
import pickle

# 已知人臉資料夾
KNOWN_FACES_DIR = "data/known_faces/"
ENCODINGS_PATH = "data/encodings.pickle"

known_encodings = []
known_names = []

# 讀取資料夾中的每張圖片
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.lower().endswith((".jpg", ".png", ".xxx")):
        path = os.path.join(KNOWN_FACES_DIR, filename)
        name = filename.split("_")[0]  # 檔名前綴當作人名

        # 載入圖片 (face_recognition 用的是 RGB)
        image = face_recognition.load_image_file(path)

        # 先找臉位置
        face_locations = face_recognition.face_locations(image, model="hog")  
        # 如果用 hog 找不到，可以改成 cnn（比較準但需要 GPU）
        # face_locations = face_recognition.face_locations(image, model="cnn")

        if not face_locations:
            print(f"[WARN] {filename} 沒有偵測到人臉！")
            continue

        # 依照臉的位置取編碼
        encodings = face_recognition.face_encodings(image, face_locations)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"[INFO] 已加入人臉：{name} ({filename})")
        else:
            print(f"[WARN] {filename} 找到臉，但無法產生編碼！")

# 存成 pickle 檔
if known_encodings:
    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)
    print(f"[INFO] Encodings 已儲存至 {ENCODINGS_PATH}")
else:
    print("[ERROR] 沒有任何人臉被編碼！")