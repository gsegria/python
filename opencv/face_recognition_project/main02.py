import cv2
import face_recognition
import pickle
import datetime
import numpy as np
from ultralytics import YOLO
from fer import FER
import os
import time
import json
import csv

# ===== 資料夾檢查 =====
os.makedirs("results", exist_ok=True)
os.makedirs("data_json", exist_ok=True)

# ===== 人臉設定 =====
with open("data/encodings.pickle", "rb") as f:
    data = pickle.load(f)

known_encodings = data.get("encodings", [])
known_names = data.get("names", [])

# ===== 物品偵測 =====
model = YOLO("yolov8n.pt")
common_items = ["apple","banana","orange","cake","pizza",
                "chair","couch","bed","dining table",
                "cell phone","keyboard","remote","scissors","cup","bottle"]

# ===== 表情偵測 =====
emotion_detector = FER(mtcnn=True)

# ===== 攝影機開啟 =====
cap = cv2.VideoCapture(0)
last_saved_time = 0
all_frames_data = []  # 累積資料

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_data = {"timestamp": datetime.datetime.now().isoformat(),
                  "faces": [], "objects": []}

    # ===== 物品偵測 =====
    results = model(frame, verbose=False)
    for r in results:
        if r.boxes is not None and len(r.boxes) > 0:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                conf = float(box.conf[0])
                if label in common_items:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    frame_data["objects"].append({
                        "label": label,
                        "confidence": round(conf, 2),
                        "bbox": [x1, y1, x2, y2]
                    })

    # ===== 人臉辨識 =====
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for (top, right, bottom, left), encoding in zip(boxes, encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.6)
        face_distances = face_recognition.face_distance(known_encodings, encoding)

        name = "Unknown"
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        face_img = frame[top:bottom, left:right]
        top_emotion = None
        score = None
        if face_img.size != 0:
            top_emotion, score = emotion_detector.top_emotion(face_img)
            if top_emotion:
                cv2.putText(frame, f"{top_emotion}", (left, bottom + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        frame_data["faces"].append({
            "name": name,
            "bbox": [left, top, right, bottom],
            "emotion": top_emotion,
            "emotion_score": round(score, 2) if score else None
        })

    # 控制存檔間隔 (2 秒)
    if time.time() - last_saved_time > 2:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_image_path = f"results/output_{now}.jpg"
        cv2.imwrite(output_image_path, frame)
        all_frames_data.append(frame_data)
        last_saved_time = time.time()

    cv2.imshow("Face + Object + Emotion", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ===== 儲存單一 JSON =====
json_path = "data_json/all_data.json"
with open(json_path, "w") as jf:
    json.dump(all_frames_data, jf, indent=2)

# ===== 儲存單一 CSV =====
csv_path = "data_json/all_data.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["timestamp", "type", "name_or_label", "bbox", "emotion", "emotion_score", "confidence"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for frame in all_frames_data:
        timestamp = frame["timestamp"]
        # 人臉
        for f in frame["faces"]:
            writer.writerow({
                "timestamp": timestamp,
                "type": "face",
                "name_or_label": f["name"],
                "bbox": f["bbox"],
                "emotion": f["emotion"],
                "emotion_score": f["emotion_score"],
                "confidence": ""
            })
        # 物品
        for o in frame["objects"]:
            writer.writerow({
                "timestamp": timestamp,
                "type": "object",
                "name_or_label": o["label"],
                "bbox": o["bbox"],
                "emotion": "",
                "emotion_score": "",
                "confidence": o["confidence"]
            })
