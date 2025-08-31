import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import soundfile as sf
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import RectangleSelector, Cursor
from scipy.signal import firwin, lfilter, butter, filtfilt

# ✅ 字體設定（支援中文顯示）
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 或 'SimHei' for 簡體
matplotlib.rcParams['axes.unicode_minus'] = False

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

        # 安全關閉（處理右上角 X）
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        frame.pack(padx=10, pady=5, fill='x')

        for i in range(3):
            ttk.Label(frame, text=f"頻率 {i+1} (Hz)").grid(row=i, column=0)
            ttk.Entry(frame, textvariable=self.freq_vars[i], width=8).grid(row=i, column=1)
            ttk.Label(frame, text="振幅").grid(row=i, column=2)
            ttk.Entry(frame, textvariable=self.amp_vars[i], width=6).grid(row=i, column=3)

        ttk.Label(frame, text="FIR Low").grid(row=0, column=4)
        ttk.Scale(frame, variable=self.fir_low, from_=50, to=fs//2 - 100, orient="horizontal").grid(row=0, column=5, sticky='ew')

        ttk.Label(frame, text="FIR High").grid(row=1, column=4)
        ttk.Scale(frame, variable=self.fir_high, from_=100, to=fs//2, orient="horizontal").grid(row=1, column=5, sticky='ew')

        ttk.Label(frame, text="FIR Order").grid(row=2, column=4)
        ttk.Entry(frame, textvariable=self.fir_order, width=5).grid(row=2, column=5)

        ttk.Label(frame, text="IIR Low").grid(row=0, column=6)
        ttk.Scale(frame, variable=self.iir_low, from_=50, to=fs//2 - 100, orient="horizontal").grid(row=0, column=7, sticky='ew')

        ttk.Label(frame, text="IIR High").grid(row=1, column=6)
        ttk.Scale(frame, variable=self.iir_high, from_=100, to=fs//2, orient="horizontal").grid(row=1, column=7, sticky='ew')

        ttk.Label(frame, text="IIR Order").grid(row=2, column=6)
        ttk.Entry(frame, textvariable=self.iir_order, width=5).grid(row=2, column=7)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="播放濾波音訊", command=self.play_filtered).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="儲存為 WAV", command=self.save_audio).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="更新圖表", command=self.update_plot).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="離開", command=self.root.destroy).grid(row=0, column=3, padx=5)

    def build_plot(self):
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(fill='both', expand=True)

        self.fig, (self.ax_time, self.ax_freq) = plt.subplots(2, 1, figsize=(8, 6))
        self.fig.tight_layout(pad=2.0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)

        # 工具列
        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()
        self.toolbar.pack(side='top', fill='x')

        # 滑鼠滾輪縮放（✅ 現在支援 time + freq）
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("button_press_event", self.on_button_press)
        self.canvas.mpl_connect("button_press_event", self.on_drag_start)
        self.canvas.mpl_connect("motion_notify_event", self.on_drag_motion)
        self.canvas.mpl_connect("button_release_event", self.on_drag_end)

        # 右鍵選單
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="放大一倍", command=self.zoom_in)
        self.menu.add_command(label="縮小一倍", command=self.zoom_out)
        self.menu.add_separator()
        self.menu.add_command(label="重設範圍", command=self.reset_zoom)

        # ====== 框選放大（time + freq 各一個 selector）======
        self.selectors = []
        for ax in (self.ax_time, self.ax_freq):
            try:
                sel = RectangleSelector(
                    ax, lambda eclick, erelease, ax=ax: self.on_select(eclick, erelease, ax),
                    drawtype='box', useblit=True,
                    button=[1], minspanx=5, minspany=5,
                    spancoords='pixels', interactive=True
                )
            except TypeError:
                sel = RectangleSelector(ax, lambda eclick, erelease, ax=ax: self.on_select(eclick, erelease, ax), button=[1])
            self.selectors.append(sel)

        # 游標顯示（頻譜圖保留即可）
        self.cursor = Cursor(self.ax_freq, useblit=True, color='red', linewidth=1)
        self.annotation = self.ax_freq.annotate(
            "", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points", ha="left", va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7),
            arrowprops=dict(arrowstyle="->")
        )
        self.annotation.set_visible(False)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

        self.update_plot()



    # --- 左右平移（拖曳） ---
    def on_drag_start(self, event):
        if event.button == 1 and event.inaxes in [self.ax_time, self.ax_freq]:
            self._dragging = True
            self._drag_start_x = event.xdata
            self._drag_ax = event.inaxes
            self._orig_xlim = self._drag_ax.get_xlim()

    def on_drag_motion(self, event):
        if not self._dragging or event.xdata is None or event.inaxes != self._drag_ax:
            return
        dx = self._drag_start_x - event.xdata
        x0, x1 = self._orig_xlim
        width = x1 - x0
        self._drag_ax.set_xlim(x0 + dx, x0 + dx + width)
        self.canvas.draw_idle()

    def on_drag_end(self, event):
        self._dragging = False
        self._drag_start_x = None
        self._drag_ax = None
        self._orig_xlim = None

    # ---------- 互動功能處理 ----------
    def on_scroll(self, event):
        """滑鼠滾輪縮放（時域 & 頻譜皆可）"""
        if event.inaxes not in [self.ax_time, self.ax_freq]:
            return
        ax = event.inaxes
        x_min, x_max = ax.get_xlim()
        x_range = (x_max - x_min) * 0.5
        x_mid = (x_max + x_min) * 0.5
        scale = 0.8 if event.button == "up" else 1.25
        new_half = x_range * scale
        ax.set_xlim(x_mid - new_half, x_mid + new_half)
        self.canvas.draw_idle()


    def on_button_press(self, event):
        """處理雙擊重設與右鍵選單"""
        if event.inaxes != self.ax_freq:
            return
        # 雙擊左鍵：重設範圍
        if getattr(event, 'dblclick', False) and event.button == 1:
            self.reset_zoom()
            return
        # 右鍵：彈出選單
        if event.button == 3:
            try:
                # TkAgg 有時 event.guiEvent 可能為 None，保險用視窗座標
                x_root = self.root.winfo_pointerx()
                y_root = self.root.winfo_pointery()
                self.menu.tk_popup(x_root, y_root)
            finally:
                self.menu.grab_release()

    def on_select(self, eclick, erelease):
        """框選放大：支援時域 & 頻譜"""
        if eclick.xdata is None or erelease.xdata is None:
            return
        x_min, x_max = sorted([eclick.xdata, erelease.xdata])
        y_min, y_max = sorted([eclick.ydata, erelease.ydata])
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        self.canvas.draw_idle()

    def on_mouse_move(self, event):
        """滑鼠移動時顯示當前頻率 & 幅度"""
        if event.inaxes == self.ax_freq and event.xdata is not None and event.ydata is not None:
            x, y = event.xdata, event.ydata
            self.annotation.xy = (x, y)
            self.annotation.set_text(f"f = {x:.1f} Hz\nAmp = {y:.3f}")
            self.annotation.set_visible(True)
            self.canvas.draw_idle()
        else:
            if self.annotation.get_visible():
                self.annotation.set_visible(False)
                self.canvas.draw_idle()

    # ---------- 音訊與繪圖 ----------
    def get_filtered_signal(self):
        freqs = [f.get() for f in self.freq_vars]
        amps = [a.get() for a in self.amp_vars]
        signal = generate_multitone(freqs, amps)

        fir_coeff = design_fir(self.fir_low.get(), self.fir_high.get(), fs, self.fir_order.get())
        signal = apply_fir(signal, fir_coeff)

        b, a = design_iir(self.iir_low.get(), self.iir_high.get(), fs, self.iir_order.get())
        signal = apply_iir(signal, b, a)

        maxv = np.max(np.abs(signal))
        if maxv > 0:
            signal = signal / maxv  # normalize，避免除以 0
        return t, signal

    def update_plot(self):
        freqs = [f.get() for f in self.freq_vars]
        amps = [a.get() for a in self.amp_vars]
        original = generate_multitone(freqs, amps)

        fir_coeff = design_fir(self.fir_low.get(), self.fir_high.get(), fs, self.fir_order.get())
        filtered = apply_fir(original, fir_coeff)

        b, a = design_iir(self.iir_low.get(), self.iir_high.get(), fs, self.iir_order.get())
        filtered = apply_iir(filtered, b, a)

        maxv = np.max(np.abs(filtered))
        if maxv > 0:
            filtered = filtered / maxv

        # 時域
        self.ax_time.clear()
        display_len = int(fs * 0.05)
        self.ax_time.plot(t[:display_len], original[:display_len], label="原始訊號", alpha=0.6)
        self.ax_time.plot(t[:display_len], filtered[:display_len], label="濾波後訊號", alpha=0.8)
        self.ax_time.set_title("時域波形圖（前 0.05 秒）")
        self.ax_time.set_xlabel("時間（秒）")
        self.ax_time.set_ylabel("振幅")
        self.ax_time.grid(True)
        self.ax_time.legend()

        # 頻譜（只取單邊）
        self.ax_freq.clear()
        N = len(original)
        fft_orig = np.abs(np.fft.fft(original)) / N
        fft_filt = np.abs(np.fft.fft(filtered)) / N
        freq = np.fft.fftfreq(N, d=1/fs)
        mask = freq >= 0
        self.ax_freq.plot(freq[mask], fft_orig[mask], label="原始 FFT", alpha=0.5)
        self.ax_freq.plot(freq[mask], fft_filt[mask], label="濾波後 FFT", alpha=0.9)
        self.ax_freq.set_title("FFT 頻譜圖（頻率分佈）")
        self.ax_freq.set_xlabel("頻率（Hz）")
        self.ax_freq.set_ylabel("幅度")
        self.ax_freq.set_xlim(0, fs // 2)
        self.ax_freq.grid(True)
        self.ax_freq.legend()

        self.canvas.draw_idle()

    def play_filtered(self):
        _, signal = self.get_filtered_signal()
        sd.play(signal, fs)

    def save_audio(self):
        _, signal = self.get_filtered_signal()
        sf.write("filtered_output_gui.wav", signal, fs)
        messagebox.showinfo("完成", "音訊已儲存為 filtered_output_gui.wav")

    # ---------- 右鍵選單操作 ----------
    def zoom_in(self):
        x_min, x_max = self.ax_freq.get_xlim()
        center = (x_min + x_max) / 2
        half = (x_max - x_min) / 4  # 縮一半的寬度
        self.ax_freq.set_xlim(max(0, center - half), min(fs/2, center + half))
        self.canvas.draw_idle()

    def zoom_out(self):
        x_min, x_max = self.ax_freq.get_xlim()
        center = (x_min + x_max) / 2
        half = (x_max - x_min)
        self.ax_freq.set_xlim(max(0, center - half), min(fs/2, center + half))
        self.canvas.draw_idle()

    def reset_zoom(self):
        self.ax_freq.set_xlim(0, fs/2)
        self.canvas.draw_idle()

    def on_closing(self):
        import sys
        try:
            sd.stop()
        except Exception:
            pass
        try:
            plt.close('all')
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)


# 執行 GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = FilterGUI(root)
    root.mainloop()
