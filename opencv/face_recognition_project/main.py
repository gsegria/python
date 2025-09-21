import cv2
import face_recognition
import pickle
import datetime

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

    # 轉成 RGB (face_recognition 使用 RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 偵測人臉位置 & 特徵
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    # 比對每張臉
    for (top, right, bottom, left), encoding in zip(boxes, encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        # 畫框 + 顯示名稱
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # 存檔（每次偵測都可以存一張）
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"results/output_{name}_{now}.jpg"
        cv2.imwrite(output_path, frame)

    cv2.imshow("Face Recognition (Press Q to Quit)", frame)

    # 按 Q 離開
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
