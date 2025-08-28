import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. 訊號參數設定
fs = 5000  # 取樣率 5kHz，足夠覆蓋 1kHz 頻率
duration = 1.0  # 秒
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# 2. 模擬含有三個頻率成分的訊號：50Hz, 120Hz, 1000Hz
signal = (
    np.sin(2 * np.pi * 50 * t) +
    0.5 * np.sin(2 * np.pi * 120 * t) +
    0.8 * np.sin(2 * np.pi * 1000 * t)
)

# 3. 執行 FFT
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(t), 1 / fs)
magnitude = np.abs(fft_result) / len(t)  # 正規化
magnitude_db = 20 * np.log10(magnitude + 1e-12)  # 轉 dB，避免 log(0)
real_part = np.real(fft_result)
imag_part = np.imag(fft_result)

# 4. 只取正頻率部分
mask = frequencies >= 0
frequencies = frequencies[mask]
real_part = real_part[mask]
imag_part = imag_part[mask]
magnitude = magnitude[mask]
magnitude_db = magnitude_db[mask]

# 5. 繪製頻譜圖（線性尺度）
plt.figure(figsize=(10, 5))
plt.plot(frequencies, magnitude)
plt.title("FFT 頻譜圖 (Magnitude)")
plt.xlabel("頻率 (Hz)")
plt.ylabel("幅度")
plt.grid(True)
plt.xlim(0, fs / 2)
plt.tight_layout()
plt.show()

# 6. 可選：繪製 dB 對數頻譜圖
plt.figure(figsize=(10, 5))
plt.plot(frequencies, magnitude_db)
plt.title("FFT 頻譜圖 (dB)")
plt.xlabel("頻率 (Hz)")
plt.ylabel("幅度 (dB)")
plt.grid(True)
plt.xlim(0, fs / 2)
plt.tight_layout()
plt.show()

# 7. 將資料儲存成 CSV 檔案
df = pd.DataFrame({
    "Frequency (Hz)": frequencies,
    "Real": real_part,
    "Imag": imag_part,
    "Magnitude": magnitude,
    "Magnitude (dB)": magnitude_db
})
df.to_csv("fft_spectrum_data.csv", index=False)
print("✅ 已將 FFT 頻譜資料儲存至：fft_spectrum_data.csv")
