
import numpy as np
import matplotlib.pyplot as plt

# 模擬一個含有兩個頻率的訊號
fs = 1000  # 取樣率 (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # 時間向量 (1秒)
signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

# 執行 FFT
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(t), 1/fs)
magnitude = np.abs(fft_result) / len(t)  # 正規化

# 只取正頻率部分
mask = frequencies >= 0
plt.plot(frequencies[mask], magnitude[mask])
plt.title("FFT 頻譜圖")
plt.xlabel("頻率 (Hz)")
plt.ylabel("幅度")
plt.grid()
plt.show()
