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
    if filename.lower().endswith((".jpg", ".png", ".jfif")):
        path = os.path.join(KNOWN_FACES_DIR, filename)
        name = filename.split("_")[0]  # 以檔名開頭作為人名，例如 Alice_01.jpg → Alice

        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"[INFO] 已加入人臉：{name} ({filename})")

# 存成 pickle 檔
data = {"encodings": known_encodings, "names": known_names}
with open(ENCODINGS_PATH, "wb") as f:
    pickle.dump(data, f)

print(f"[INFO] Encodings 已儲存至 {ENCODINGS_PATH}")
