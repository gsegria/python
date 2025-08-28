import numpy as np
import soundfile as sf
from scipy.signal import firwin, lfilter, butter, filtfilt

# 基本參數
fs = 8000  # 取樣率
duration = 2.0  # 秒
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# 建立多頻率訊號
def generate_multitone(freqs=[500, 1000, 1500], amps=[1.0, 0.5, 0.3]):
    signal = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        signal += a * np.sin(2 * np.pi * f * t)
    return signal

# FIR 濾波器設計
def design_fir(lowcut, highcut, fs, numtaps=101):
    return firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)

def apply_fir(signal, coeff):
    return lfilter(coeff, 1.0, signal)

# IIR 濾波器設計
def design_iir(lowcut, highcut, fs, order=4):
    b, a = butter(order, [lowcut / (fs / 2), highcut / (fs / 2)], btype='band')
    return b, a

def apply_iir(signal, b, a):
    return filtfilt(b, a, signal)

# 產生訊號
signal = generate_multitone()

# 套用 FIR 濾波器
fir_coeff = design_fir(300, 2000, fs, numtaps=101)
filtered = apply_fir(signal, fir_coeff)

# 套用 IIR 濾波器
b, a = design_iir(300, 2000, fs, order=4)
filtered = apply_iir(filtered, b, a)

# 正規化並儲存為 WAV
filtered /= np.max(np.abs(filtered))  # 避免爆音
sf.write('filtered_output.wav', filtered, fs)
print("✅ 已儲存為 filtered_output.wav")
