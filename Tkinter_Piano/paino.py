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

root = tk.Tk()
root.title("88鍵鋼琴")

# Label 顯示按鍵
label_var = tk.StringVar()
label_var.set("按下琴鍵顯示音符")
note_label = tk.Label(root, textvariable=label_var, font=("Arial", 16))
note_label.pack(pady=5)

canvas = tk.Canvas(root, height=200, bg="gray")
canvas.pack(fill="both", expand=True)

def play_note(note):
    label_var.set(f"按下: {note}")
    freq = note_to_freq(note)
    t = np.linspace(0, 0.5, int(fs * 0.5), endpoint=False)
    wave = 0.3 * np.sin(2 * np.pi * freq * t)
    sd.play(wave, fs)

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
            
            # 顯示音符名稱 & 指法
            finger = (white_index % 5) + 1
            y_text = white_height - 20
            canvas.create_text((x0+x1)/2, y_text, text=f"{note}\n{finger}", fill="blue", font=("Arial", int(white_width/3)))
            white_index += 1

    # 畫黑鍵
    for i, note in enumerate(note_names):
        if "#" in note:
            white_idx = sum(1 for n in note_names[:i] if "#" not in n)
            x0 = white_idx * white_width - black_width/2
            x1 = x0 + black_width
            rect = canvas.create_rectangle(x0, 0, x1, black_height, fill="black", outline="black")
            canvas.tag_bind(rect, "<Button-1>", lambda e, n=note: play_note(n))

draw_keys()
canvas.bind("<Configure>", draw_keys)

root.mainloop()
