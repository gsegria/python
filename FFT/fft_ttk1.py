import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd
from scipy.signal import firwin, lfilter, butter, filtfilt

# 參數
fs = 8000  # 取樣率
duration = 2  # 秒
t = np.linspace(0, duration, int(fs*duration), endpoint=False)

# 產生 1kHz 正弦波訊號
def generate_signal():
    return np.sin(2 * np.pi * 1000 * t)

# FIR 濾波器設計
def design_fir(lowcut, highcut, fs, numtaps=101):
    return firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)

# IIR 濾波器設計
def design_iir(lowcut, highcut, fs, order=4):
    from scipy.signal import butter
    b, a = butter(order, [lowcut/(fs/2), highcut/(fs/2)], btype='band')
    return b, a

# 濾波函數
def apply_fir(signal, coeff):
    return lfilter(coeff, 1.0, signal)

def apply_iir(signal, b, a):
    return filtfilt(b, a, signal)

# 計算頻譜
def compute_fft(signal):
    N = len(signal)
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(N, 1/fs)
    mag = np.abs(fft_result) / N
    mask = freq >= 0
    return freq[mask], mag[mask]

# 播放音訊（非阻塞）
def play_audio(signal):
    sd.play(signal, fs)

# GUI 介面
class FilterApp:
    def __init__(self, root):
        self.root = root
        root.title("1kHz 音訊 + FIR/IIR 濾波器調整")

        # 預設參數
        self.fir_low = tk.DoubleVar(value=100)
        self.fir_high = tk.DoubleVar(value=2000)
        self.iir_low = tk.DoubleVar(value=100)
        self.iir_high = tk.DoubleVar(value=2000)

        # 輸入框架
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="FIR 低截止頻率 (Hz)").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.fir_low, width=10).grid(row=0, column=1)
        ttk.Label(frame, text="FIR 高截止頻率 (Hz)").grid(row=0, column=2)
        ttk.Entry(frame, textvariable=self.fir_high, width=10).grid(row=0, column=3)

        ttk.Label(frame, text="IIR 低截止頻率 (Hz)").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.iir_low, width=10).grid(row=1, column=1)
        ttk.Label(frame, text="IIR 高截止頻率 (Hz)").grid(row=1, column=2)
        ttk.Entry(frame, textvariable=self.iir_high, width=10).grid(row=1, column=3)

        # 按鈕
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        self.btn_apply = ttk.Button(btn_frame, text="應用濾波器並播放", command=self.apply_and_play)
        self.btn_apply.grid(row=0, column=0, padx=5)

        self.btn_stop = ttk.Button(btn_frame, text="停止播放", command=self.stop_audio)
        self.btn_stop.grid(row=0, column=1, padx=5)

        # 頻譜繪圖
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # 初始訊號
        self.signal = generate_signal()
        self.plot_spectrum(self.signal, "原始訊號頻譜")

    def plot_spectrum(self, signal, title):
        freq, mag = compute_fft(signal)
        self.ax.clear()
        self.ax.plot(freq, mag)
        self.ax.set_xlim(0, 3000)
        self.ax.set_ylim(0, np.max(mag)*1.1)
        self.ax.set_title(title)
        self.ax.set_xlabel("頻率 (Hz)")
        self.ax.set_ylabel("幅度")
        self.ax.grid(True)
        self.canvas.draw()

    def apply_and_play(self):
        # 讀取參數並驗證
        try:
            fir_low = float(self.fir_low.get())
            fir_high = float(self.fir_high.get())
            iir_low = float(self.iir_low.get())
            iir_high = float(self.iir_high.get())
            assert 0 < fir_low < fir_high < fs/2
            assert 0 < iir_low < iir_high < fs/2
        except Exception as e:
            tk.messagebox.showerror("輸入錯誤", f"請輸入合理的截止頻率：\n{e}")
            return

        # 設計濾波器
        fir_coeff = design_fir(fir_low, fir_high, fs)
        b, a = design_iir(iir_low, iir_high, fs)

        # 依序套用 FIR 與 IIR
        filtered = apply_fir(self.signal, fir_coeff)
        filtered = apply_iir(filtered, b, a)

        # 顯示頻譜
        self.plot_spectrum(filtered, "濾波後訊號頻譜")

        # 播放濾波後音訊
        play_audio(filtered)

    def stop_audio(self):
        sd.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
