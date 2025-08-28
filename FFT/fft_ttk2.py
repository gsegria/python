import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd
from scipy.signal import firwin, lfilter, butter, filtfilt, cheby1, cheby2, ellip

# 參數
fs = 8000  # 取樣率
duration = 2  # 秒
t = np.linspace(0, duration, int(fs*duration), endpoint=False)

# 產生任意頻率正弦波
def generate_signal(freq=1000):
    return np.sin(2 * np.pi * freq * t)

# FIR 濾波器設計
def design_fir(lowcut, highcut, fs, numtaps=101):
    return firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)

# IIR 濾波器設計，多種濾波器類型
def design_iir(lowcut, highcut, fs, order=4, ftype='butter'):
    nyq = fs / 2
    wp = [lowcut/nyq, highcut/nyq]
    if ftype == 'butter':
        b, a = butter(order, wp, btype='band')
    elif ftype == 'cheby1':
        b, a = cheby1(order, 0.5, wp, btype='band')
    elif ftype == 'cheby2':
        b, a = cheby2(order, 40, wp, btype='band')
    elif ftype == 'ellip':
        b, a = ellip(order, 0.5, 40, wp, btype='band')
    else:
        raise ValueError("不支援的濾波器類型")
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
        root.title("多功能音訊濾波器調整與播放")

        # 變數
        self.freq_var = tk.DoubleVar(value=1000)

        self.fir_low = tk.DoubleVar(value=100)
        self.fir_high = tk.DoubleVar(value=2000)
        self.fir_order = tk.IntVar(value=101)

        self.iir_low = tk.DoubleVar(value=100)
        self.iir_high = tk.DoubleVar(value=2000)
        self.iir_order = tk.IntVar(value=4)
        self.iir_type = tk.StringVar(value='butter')

        # 建立控制區
        control_frame = ttk.Frame(root)
        control_frame.pack(padx=10, pady=10)

        # 輸出頻率
        ttk.Label(control_frame, text="輸出頻率 (Hz):").grid(row=0, column=0, sticky='e')
        ttk.Entry(control_frame, textvariable=self.freq_var, width=10).grid(row=0, column=1)

        # FIR 參數
        ttk.Label(control_frame, text="FIR 低截止頻率 (Hz):").grid(row=1, column=0, sticky='e')
        ttk.Entry(control_frame, textvariable=self.fir_low, width=10).grid(row=1, column=1)
        ttk.Label(control_frame, text="FIR 高截止頻率 (Hz):").grid(row=1, column=2, sticky='e')
        ttk.Entry(control_frame, textvariable=self.fir_high, width=10).grid(row=1, column=3)
        ttk.Label(control_frame, text="FIR 階數:").grid(row=1, column=4, sticky='e')
        ttk.Entry(control_frame, textvariable=self.fir_order, width=10).grid(row=1, column=5)

        # IIR 參數
        ttk.Label(control_frame, text="IIR 低截止頻率 (Hz):").grid(row=2, column=0, sticky='e')
        ttk.Entry(control_frame, textvariable=self.iir_low, width=10).grid(row=2, column=1)
        ttk.Label(control_frame, text="IIR 高截止頻率 (Hz):").grid(row=2, column=2, sticky='e')
        ttk.Entry(control_frame, textvariable=self.iir_high, width=10).grid(row=2, column=3)

        ttk.Label(control_frame, text="IIR 階數:").grid(row=2, column=4, sticky='e')
        ttk.Entry(control_frame, textvariable=self.iir_order, width=10).grid(row=2, column=5)

        ttk.Label(control_frame, text="IIR 類型:").grid(row=3, column=0, sticky='e')
        iir_type_menu = ttk.OptionMenu(control_frame, self.iir_type, 'butter', 'butter', 'cheby1', 'cheby2', 'ellip')
        iir_type_menu.grid(row=3, column=1, sticky='w')

        # 按鈕區
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        self.btn_apply = ttk.Button(btn_frame, text="產生訊號 + 濾波並播放", command=self.apply_and_play)
        self.btn_apply.grid(row=0, column=0, padx=5)

        self.btn_stop = ttk.Button(btn_frame, text="停止播放", command=self.stop_audio)
        self.btn_stop.grid(row=0, column=1, padx=5)

        # 圖形區：時域與頻域波形
        self.fig, (self.ax_time, self.ax_freq) = plt.subplots(2, 1, figsize=(9, 6))
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.signal = generate_signal(self.freq_var.get())
        self.plot_signals(self.signal, self.signal)

    def plot_signals(self, sig_orig, sig_filt):
        # 時域波形
        self.ax_time.clear()
        self.ax_time.plot(t, sig_orig, label='原始訊號')
        self.ax_time.plot(t, sig_filt, label='濾波後訊號')
        self.ax_time.set_title("時域波形比較")
        self.ax_time.set_xlabel("時間 (秒)")
        self.ax_time.set_ylabel("振幅")
        self.ax_time.legend()
        self.ax_time.grid(True)

        # 頻域波形
        freq, mag_orig = compute_fft(sig_orig)
        _, mag_filt = compute_fft(sig_filt)
        self.ax_freq.clear()
        self.ax_freq.plot(freq, mag_orig, label='原始訊號頻譜')
        self.ax_freq.plot(freq, mag_filt, label='濾波後訊號頻譜')
        self.ax_freq.set_xlim(0, fs/2)
        self.ax_freq.set_title("頻域幅度頻譜")
        self.ax_freq.set_xlabel("頻率 (Hz)")
        self.ax_freq.set_ylabel("幅度")
        self.ax_freq.legend()
        self.ax_freq.grid(True)

        self.canvas.draw()

    def apply_and_play(self):
        try:
            freq = float(self.freq_var.get())
            fir_low = float(self.fir_low.get())
            fir_high = float(self.fir_high.get())
            fir_order = int(self.fir_order.get())
            iir_low = float(self.iir_low.get())
            iir_high = float(self.iir_high.get())
            iir_order = int(self.iir_order.get())
            iir_type = self.iir_type.get()

            assert 0 < freq < fs/2, "輸出頻率需在 0 到 Nyquist 頻率內"
            assert 0 < fir_low < fir_high < fs/2, "FIR 截止頻率需合理"
            assert fir_order > 0 and fir_order % 2 == 1, "FIR 階數需為正奇數"
            assert 0 < iir_low < iir_high < fs/2, "IIR 截止頻率需合理"
            assert iir_order > 0, "IIR 階數需正整數"

        except Exception as e:
            messagebox.showerror("輸入錯誤", f"請確認輸入值合理：\n{e}")
            return

        self.signal = generate_signal(freq)

        # 設計濾波器並套用
        fir_coeff = design_fir(fir_low, fir_high, fs, fir_order)
        b, a = design_iir(iir_low, iir_high, fs, iir_order, iir_type)

        filtered = apply_fir(self.signal, fir_coeff)
        filtered = apply_iir(filtered, b, a)

        # 顯示圖形與播放
        self.plot_signals(self.signal, filtered)
        play_audio(filtered)

    def stop_audio(self):
        sd.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
