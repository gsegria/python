import cv2
import face_recognition
import pickle
import datetime
import numpy as np

# 載入 encodings
with open("data/encodings.pickle", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

# 開啟攝影機
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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

        # 畫框 + 顯示名稱
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # 存檔（只在辨識到人臉時才存）
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_path = f"results/output_{name}_{now}.jpg"
        cv2.imwrite(output_path, frame)

    cv2.imshow("Face Recognition (Press Q to Quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
