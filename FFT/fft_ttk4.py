import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import firwin, lfilter, butter, filtfilt

fs = 8000  # 取樣率
duration = 2.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

def generate_multitone(freqs, amps):
    signal = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        signal += a * np.sin(2 * np.pi * f * t)
    return signal

def design_fir(lowcut, highcut, fs, numtaps=101):
    return firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)

def apply_fir(signal, coeff):
    return lfilter(coeff, 1.0, signal)

def design_iir(lowcut, highcut, fs, order=4):
    return butter(order, [lowcut / (fs / 2), highcut / (fs / 2)], btype='band')

def apply_iir(signal, b, a):
    return filtfilt(b, a, signal)

class FilterGUI:
    def __init__(self, root):
        self.root = root
        root.title("多音源 + 即時濾波 GUI")

        self.freq_vars = [tk.DoubleVar(value=f) for f in [500, 1000, 1500]]
        self.amp_vars = [tk.DoubleVar(value=a) for a in [1.0, 0.5, 0.3]]

        self.fir_low = tk.DoubleVar(value=300)
        self.fir_high = tk.DoubleVar(value=2000)
        self.fir_order = tk.IntVar(value=101)

        self.iir_low = tk.DoubleVar(value=300)
        self.iir_high = tk.DoubleVar(value=2000)
        self.iir_order = tk.IntVar(value=4)

        self.build_controls()
        self.build_plot()

    def build_controls(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=5)

        for i in range(3):
            ttk.Label(frame, text=f"頻率 {i+1} (Hz)").grid(row=i, column=0)
            ttk.Entry(frame, textvariable=self.freq_vars[i], width=8).grid(row=i, column=1)
            ttk.Label(frame, text="振幅").grid(row=i, column=2)
            ttk.Entry(frame, textvariable=self.amp_vars[i], width=6).grid(row=i, column=3)

        ttk.Label(frame, text="FIR Low").grid(row=0, column=4)
        ttk.Scale(frame, variable=self.fir_low, from_=50, to=fs//2 - 100, orient="horizontal").grid(row=0, column=5)

        ttk.Label(frame, text="FIR High").grid(row=1, column=4)
        ttk.Scale(frame, variable=self.fir_high, from_=100, to=fs//2, orient="horizontal").grid(row=1, column=5)

        ttk.Label(frame, text="FIR Order").grid(row=2, column=4)
        ttk.Entry(frame, textvariable=self.fir_order, width=5).grid(row=2, column=5)

        ttk.Label(frame, text="IIR Low").grid(row=0, column=6)
        ttk.Scale(frame, variable=self.iir_low, from_=50, to=fs//2 - 100, orient="horizontal").grid(row=0, column=7)

        ttk.Label(frame, text="IIR High").grid(row=1, column=6)
        ttk.Scale(frame, variable=self.iir_high, from_=100, to=fs//2, orient="horizontal").grid(row=1, column=7)

        ttk.Label(frame, text="IIR Order").grid(row=2, column=6)
        ttk.Entry(frame, textvariable=self.iir_order, width=5).grid(row=2, column=7)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="播放濾波音訊", command=self.play_filtered).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="儲存為 WAV", command=self.save_audio).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="更新圖表", command=self.update_plot).grid(row=0, column=2, padx=5)

    def build_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        self.update_plot()

    def get_filtered_signal(self):
        freqs = [f.get() for f in self.freq_vars]
        amps = [a.get() for a in self.amp_vars]
        signal = generate_multitone(freqs, amps)

        fir_coeff = design_fir(self.fir_low.get(), self.fir_high.get(), fs, self.fir_order.get())
        signal = apply_fir(signal, fir_coeff)

        b, a = design_iir(self.iir_low.get(), self.iir_high.get(), fs, self.iir_order.get())
        signal = apply_iir(signal, b, a)

        signal /= np.max(np.abs(signal))  # normalize
        return t, signal

    def update_plot(self):
        t_vals, signal = self.get_filtered_signal()
        self.ax.clear()
        self.ax.plot(t_vals[:800], signal[:800])  # Show first 0.1s
        self.ax.set_title("時域波形 (前 0.1 秒)")
        self.ax.set_xlabel("時間 (秒)")
        self.ax.set_ylabel("振幅")
        self.ax.grid(True)
        self.canvas.draw()

    def play_filtered(self):
        _, signal = self.get_filtered_signal()
        sd.play(signal, fs)

    def save_audio(self):
        _, signal = self.get_filtered_signal()
        sf.write("filtered_output_gui.wav", signal, fs)
        messagebox.showinfo("完成", "音訊已儲存為 filtered_output_gui.wav")

# 執行 GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = FilterGUI(root)
    root.mainloop()
