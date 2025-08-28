import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import firwin, lfilter, butter, filtfilt

# 1. 訊號參數設定
fs = 5000  # 取樣率 5kHz
duration = 1.0  # 秒
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# 2. 模擬訊號（50Hz + 120Hz + 1000Hz）
signal = (
    np.sin(2 * np.pi * 50 * t) +
    0.5 * np.sin(2 * np.pi * 120 * t) +
    0.8 * np.sin(2 * np.pi * 1000 * t)
)

# === FIR 濾波器設計: 通帶 40-150Hz (保留低頻，濾除高頻) ===
numtaps = 101  # 濾波器階數
fir_coeff = firwin(numtaps, [40, 150], pass_zero=False, fs=fs)

# FIR 濾波
signal_fir = lfilter(fir_coeff, 1.0, signal)

# === IIR 濾波器設計: 巴特沃斯帶通濾波器，40-150Hz ===
order = 4
lowcut = 40
highcut = 150
b, a = butter(order, [lowcut / (0.5 * fs), highcut / (0.5 * fs)], btype='band')

# IIR 濾波 (用 filtfilt 雙向濾波避免相位失真)
signal_iir = filtfilt(b, a, signal)

# --- 定義 FFT 計算函數 ---
def compute_fft(x, fs):
    N = len(x)
    fft_result = np.fft.fft(x)
    frequencies = np.fft.fftfreq(N, 1 / fs)
    magnitude = np.abs(fft_result) / N
    mask = frequencies >= 0
    return frequencies[mask], magnitude[mask]

# 3. FFT 計算
freq, mag_orig = compute_fft(signal, fs)
_, mag_fir = compute_fft(signal_fir, fs)
_, mag_iir = compute_fft(signal_iir, fs)

# 4. 頻譜圖比較
plt.figure(figsize=(12, 6))
plt.plot(freq, mag_orig, label='原始訊號')
plt.plot(freq, mag_fir, label='FIR 濾波結果')
plt.plot(freq, mag_iir, label='IIR 濾波結果')
plt.title('原始訊號與濾波後訊號的 FFT 頻譜比較')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.xlim(0, 1500)
plt.grid()
plt.legend()
plt.show()
