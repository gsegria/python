import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import matplotlib.pyplot as plt
import json

# 1. 資料預處理
def load_and_preprocess_data():
    # 載入 MNIST 數據集
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

    # 資料預處理
    x_train = x_train.astype('float32') / 255.0  # 正規化
    x_test = x_test.astype('float32') / 255.0

    # 重塑資料形狀 (28, 28) 變為 (28, 28, 1)，因為這是 CNN 預期的形狀
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    # 儲存處理後的資料集
    # 儲存成 HDF5 格式
    import h5py
    with h5py.File('data/processed_data.h5', 'w') as f:
        f.create_dataset('x_train', data=x_train)
        f.create_dataset('y_train', data=y_train)
        f.create_dataset('x_test', data=x_test)
        f.create_dataset('y_test', data=y_test)
        
    return (x_train, y_train), (x_test, y_test)

# 2. 建立 CNN 模型
def build_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # 10 類別（數字 0-9）
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

# 3. 訓練模型並儲存訓練過程
def train_and_save_model(model, x_train, y_train, x_test, y_test):
    history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))
    
    # 儲存訓練過程的圖表
    plot_training_history(history)
    
    # 儲存訓練參數與結果
    training_params = {
        'epochs': 10,
        'batch_size': 32,
        'learning_rate': 0.001,
        'train_accuracy': history.history['accuracy'],
        'val_accuracy': history.history['val_accuracy'],
        'train_loss': history.history['loss'],
        'val_loss': history.history['val_loss']
    }
    
    with open('results/training_params.json', 'w') as f:
        json.dump(training_params, f)
    
    # 儲存模型（H5 格式）
    model.save('models/mnist_model.h5')
    
    # 儲存為 TensorFlow SavedModel 格式
    model.save('models/saved_model_mnist')

# 4. 訓練過程可視化
def plot_training_history(history):
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training History')
    plt.xlabel('Epochs')
    plt.ylabel('Metrics')
    plt.legend()
    plt.savefig('results/training_history.png')

# 主函數
def main():
    # 1. 載入與預處理資料
    (x_train, y_train), (x_test, y_test) = load_and_preprocess_data()

    # 2. 建立與編譯模型
    model = build_model()

    # 3. 訓練模型並儲存結果
    train_and_save_model(model, x_train, y_train, x_test, y_test)
    
    print("Model training complete and results saved!")

# 執行主函數
if __name__ == '__main__':
    main()
