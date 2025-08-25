import tensorflow as tf
from tensorflow.keras import layers, models, preprocessing
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. 載入 IMDb 資料集
num_words = 10000  # 僅使用前 1 萬常見單字
maxlen = 200       # 每個評論長度補齊到 200

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=num_words)

# Padding 對齊長度
x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)

# 2. 建立模型 (LSTM)
model = models.Sequential([
    layers.Embedding(num_words, 128, input_length=maxlen),
    layers.LSTM(128, dropout=0.2, recurrent_dropout=0.2),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 3. 訓練
history = model.fit(x_train, y_train,
                    epochs=3,
                    batch_size=64,
                    validation_split=0.2)

# 4. 評估
loss, acc = model.evaluate(x_test, y_test, verbose=2)
print(f"✅ 測試準確率: {acc:.4f}")

# 5. 產生混淆矩陣
y_pred = (model.predict(x_test) > 0.5).astype("int32")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# 6. 儲存模型
model.save("imdb_lstm_model.h5")
print("💾 模型已儲存")
