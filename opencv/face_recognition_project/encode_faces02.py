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
        name_prefix = filename.split("_")[0]  # 檔名前綴當作人名

        # 載入圖片 (face_recognition 用 RGB)
        image = face_recognition.load_image_file(path)

        # --- 優化1: 調整圖片大小，最大邊長 800px ---
        h, w = image.shape[:2]
        max_dim = max(h, w)
        if max_dim > 800:
            scale = 800 / max_dim
            image = cv2.resize(image, (int(w*scale), int(h*scale)))

        # --- 偵測臉位置 ---
        face_locations = face_recognition.face_locations(image, model="hog")
        # 如果想要更準，可改成 cnn
        # face_locations = face_recognition.face_locations(image, model="cnn")

        if not face_locations:
            print(f"[WARN] {filename} 沒有偵測到人臉！")
            continue

        # --- 編碼所有偵測到的人臉 ---
        encodings = face_recognition.face_encodings(image, face_locations)

        for i, enc in enumerate(encodings):
            known_encodings.append(enc)
            # 如果同一張圖片多臉，用 Name_1, Name_2
            known_names.append(f"{name_prefix}_{i+1}" if len(encodings) > 1 else name_prefix)
        
        print(f"[INFO] {filename} 偵測到 {len(encodings)} 張人臉，已加入編碼。")

# --- 存成 pickle 檔 ---
if known_encodings:
    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)
    print(f"[INFO] Encodings 已儲存至 {ENCODINGS_PATH}")
else:
    print("[ERROR] 沒有任何人臉被編碼！")
