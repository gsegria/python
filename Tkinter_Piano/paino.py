import tkinter as tk
import numpy as np
import sounddevice as sd

fs = 44100  # 取樣率

note_names = [
    "A0","A#0","B0",
    "C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1",
    "C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2",
    "C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3",
    "C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4",
    "C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5",
    "C6","C#6","D6","D#6","E6","F6","F#6","G6","G#6","A6","A#6","B6",
    "C7","C#7","D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7",
    "C8"
]

def note_to_freq(note):
    A4_index = note_names.index("A4")
    n = note_names.index(note) - A4_index
    return 440 * 2**(n/12)

def play_note(note, duration=0.5):
    freq = note_to_freq(note)
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    wave = 0.3 * np.sin(2 * np.pi * freq * t)
    sd.play(wave, fs)
    sd.wait()

root = tk.Tk()
root.title("88鍵鋼琴")

canvas = tk.Canvas(root, height=200, bg="gray")
canvas.pack(fill="both", expand=True)

white_keys = []
black_keys = []

def draw_keys(event=None):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    num_white = sum(1 for n in note_names if "#" not in n)
    white_width = width / num_white
    white_height = height
    black_width = white_width * 0.6
    black_height = height * 0.6

    # 畫白鍵
    white_index = 0
    for i, note in enumerate(note_names):
        if "#" not in note:
            x0 = white_index * white_width
            x1 = x0 + white_width
            rect = canvas.create_rectangle(x0, 0, x1, white_height, fill="white", outline="black")
            canvas.tag_bind(rect, "<Button-1>", lambda e, n=note: play_note(n))
            white_index += 1

    # 畫黑鍵
    black_positions = [0,1,3,4,5,7,8,10,11,12,14,15,17,18,19,21,22,24,25,26,28,29,31,32,
                       33,35,36,38,39,40,42,43,45,46,47]
    for i, note in enumerate(note_names):
        if "#" in note:
            white_idx = sum(1 for n in note_names[:i] if "#" not in n)
            x0 = white_idx * white_width - black_width/2
            x1 = x0 + black_width
            rect = canvas.create_rectangle(x0, 0, x1, black_height, fill="black", outline="black")
            canvas.tag_bind(rect, "<Button-1>", lambda e, n=note: play_note(n))

# 初次繪製
draw_keys()

# 視窗大小改變時自動重繪
canvas.bind("<Configure>", draw_keys)

root.mainloop()
