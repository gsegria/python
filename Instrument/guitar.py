import tkinter as tk
import numpy as np
import sounddevice as sd

fs = 44100  # 取樣率

# 六弦吉他標準音符 (空弦)
string_names = ["E2", "A2", "D3", "G3", "B3", "E4"]

# 計算音符頻率
def note_to_freq(note):
    note_names = [
        "C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0",
        "C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1",
        "C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2",
        "C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3",
        "C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4",
        "C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5"
    ]
    A4_index = note_names.index("A4")
    n = note_names.index(note) - A4_index
    return 440 * 2**(n/12)

def play_note(note, duration=0.5):
    freq = note_to_freq(note)
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    wave = 0.3*np.sin(2*np.pi*freq*t)
    sd.play(wave, fs)
    sd.wait()

# Tkinter 視窗
root = tk.Tk()
root.title("六弦吉他示意圖")
root.geometry("800x600")

# 音符顯示 Label
note_var = tk.StringVar()
note_var.set("點擊弦按鍵發聲")
note_label = tk.Label(root, textvariable=note_var, font=("Arial", 16))
note_label.pack(pady=5)

canvas = tk.Canvas(root, width=800, height=550, bg="#F5DEB3")  # 淺木色背景
canvas.pack(fill="both", expand=True)

# 繪製指板
def draw_fretboard():
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    # 弦數與品數
    num_strings = 6
    num_frets = 12
    
    margin = 50
    fretboard_width = width - 2*margin
    fretboard_height = height - 2*margin
    
    # 弦間距
    string_spacing = fretboard_height / (num_strings-1)
    
    # 品間距
    fret_spacing = fretboard_width / num_frets
    
    # 畫弦
    for i in range(num_strings):
        y = margin + i*string_spacing
        canvas.create_line(margin, y, width-margin, y, fill="black", width=2)
    
    # 畫品柱
    for i in range(num_frets+1):
        x = margin + i*fret_spacing
        canvas.create_line(x, margin, x, height-margin, fill="gray", width=1)
    
    # 畫弦按鍵矩形，綁定事件
    for s in range(num_strings):
        y = margin + s*string_spacing
        for f in range(num_frets+1):
            x = margin + f*fret_spacing

            padding_x = 15  # 水平方向擴大範圍
            padding_y = 20  # 垂直方向擴大範圍
            rect = canvas.create_rectangle(x-padding_x, y-padding_y, x+padding_x, y+padding_y, fill="yellow", outline="black")


            note_name = string_names[s]
            canvas.tag_bind(rect, "<Button-1>", lambda e, n=note_name: [note_var.set(f"按下: {n}"), play_note(n)])

draw_fretboard()
canvas.bind("<Configure>", lambda e: draw_fretboard())

root.mainloop()
