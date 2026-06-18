import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import pygame

from data.paragraphs import (
    easy_paragraphs,
    medium_paragraphs,
    hard_paragraphs
)

from utils.achievements import get_achievement
from utils.themes import LIGHT_THEME, DARK_THEME
from flask import Flask, render_template ,jsonify

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")
@app.route("/get-paragraph/<difficulty>")
def get_paragraph(difficulty):

    if difficulty == "Easy":
        paragraph = random.choice(easy_paragraphs)

    elif difficulty == "Medium":
        paragraph = random.choice(medium_paragraphs)

    else:
        paragraph = random.choice(hard_paragraphs)

    return jsonify({
        "paragraph": paragraph
    })
class TypingSpeedTester:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced Typing Speed Tester")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Sound
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("sounds/success.wav")
        except Exception:
            pass

        # Variables
        self.start_time = None
        self.timer_running = False
        self.time_limit = 60
        self.time_left = self.time_limit

        self.best_wpm = 0
        self.dark_mode = False
        self.current_paragraph = ""

        self.setup_ui()
        self.load_paragraph()
    

    def setup_ui(self):

        self.root.configure(bg="white")

        self.title_label = tk.Label(
            self.root,
            text="⌨ Advanced Typing Speed Tester",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.title_label.pack(pady=15)

        top_frame = tk.Frame(self.root, bg="white")
        top_frame.pack()

        tk.Label(
            top_frame,
            text="Difficulty:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=0, column=0, padx=5)

        self.difficulty = ttk.Combobox(
            top_frame,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=15
        )
        self.difficulty.bind(
            "<<ComboboxSelected>>",
            self.change_difficulty
        )
        self.difficulty.set("Easy")
        self.difficulty.grid(row=0, column=1, padx=5)
    
        self.theme_btn = tk.Button(
            top_frame,
            text="🌙 Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_btn.grid(row=0, column=2, padx=20)

        self.timer_label = tk.Label(
            self.root,
            text="Time Left: 60",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        self.timer_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(
            self.root,
            length=500,
            maximum=100
        )
        self.progress_bar.pack(pady=5)

        self.progress_label = tk.Label(
            self.root,
            text="Progress: 0%",
            bg="white",
            font=("Arial", 11)
        )
        self.progress_label.pack()

        self.paragraph_label = tk.Label(
            self.root,
            text="",
            wraplength=850,
            justify="left",
            font=("Segoe UI", 12),
            bg="white"
        )
        self.paragraph_label.pack(pady=20)

        self.text_box = tk.Text(
            self.root,
            width=100,
            height=10,
            font=("Consolas", 12)
        )
        self.text_box.pack(pady=10)

        self.text_box.bind("<KeyPress>", self.start_test)
        self.text_box.bind("<KeyRelease>", self.live_stats)

        self.text_box.bind("<Control-v>", self.block_paste)
        self.text_box.bind("<Control-V>", self.block_paste)
        self.text_box.bind("<Shift-Insert>", self.block_paste)
        self.text_box.bind("<Button-3>", self.block_paste)

        stats_frame = tk.Frame(self.root, bg="white")
        stats_frame.pack(pady=15)

        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", bg="white")
        self.wpm_label.grid(row=0, column=0, padx=20)

        self.acc_label = tk.Label(stats_frame, text="Accuracy: 0%", bg="white")
        self.acc_label.grid(row=0, column=1, padx=20)

        self.mistake_label = tk.Label(stats_frame, text="Mistakes: 0", bg="white")
        self.mistake_label.grid(row=0, column=2, padx=20)

        self.best_label = tk.Label(stats_frame, text="Best WPM: 0", bg="white")
        self.best_label.grid(row=0, column=3, padx=20)

        self.achievement_label = tk.Label(
            self.root,
            text="Achievement: None",
            font=("Segoe UI", 24, "bold"),
            bg="white"
        )
        self.achievement_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="New Paragraph",
            width=18,
            command=self.new_test
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Restart Test",
            width=18,
            command=self.restart_test
        ).grid(row=0, column=1, padx=10)
    
    def new_test(self):
        self.timer_running = False
        self.time_left = self.time_limit
        self.start_time = None
        self.timer_label.config(
            text=f"Time Left: {self.time_limit}"
        )
        self.progress_bar["value"] = 0
        self.progress_label.config(
            text="Progress: 0%"
        )
        self.text_box.config(
            state="normal"
        )
        self.text_box.delete(
            "1.0",
            tk.END
        )
        self.load_paragraph()

    def change_difficulty(self, event=None):
        if self.timer_running:
            return
        self.load_paragraph()
        self.text_box.delete(
            "1.0",
            tk.END
        )

    def block_paste(self, event):
        messagebox.showwarning(
            "Blocked",
            "Paste is not allowed."
        )
        return "break"
    
    def load_paragraph(self):

        difficulty = self.difficulty.get()

        if difficulty == "Easy":
            self.current_paragraph = random.choice(easy_paragraphs)
        elif difficulty == "Medium":
            self.current_paragraph = random.choice(medium_paragraphs)
        else:
            self.current_paragraph = random.choice(hard_paragraphs)

        self.paragraph_label.config(text=self.current_paragraph)
        self.text_box.delete(
            "1.0",
            tk.END
        )
    def toggle_theme(self):

        self.dark_mode = not self.dark_mode
        theme = DARK_THEME if self.dark_mode else LIGHT_THEME

        self.root.configure(bg=theme["bg"])

        widgets = [
            self.title_label,
            self.timer_label,
            self.progress_label,
            self.paragraph_label,
            self.wpm_label,
            self.acc_label,
            self.mistake_label,
            self.best_label,
            self.achievement_label
        ]

        for widget in widgets:
            try:
                widget.config(bg=theme["bg"], fg=theme["fg"])
            except Exception:
                pass

        self.text_box.config(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )

    # FIXED POSITION (this was the main bug)
    def start_test(self, event=None):

        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.countdown()

    def countdown(self):

        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}")
            self.root.after(1000, self.countdown)
        else:
            self.finish_test()

    def calculate_mistakes(self, typed_text):

        mistakes = 0

        for i in range(min(len(typed_text), len(self.current_paragraph))):
            if typed_text[i] != self.current_paragraph[i]:
                mistakes += 1

        mistakes += max(0, len(typed_text) - len(self.current_paragraph))
        return mistakes

    def live_stats(self, event=None):

        if not self.timer_running:
            return

        typed_text = self.text_box.get("1.0", tk.END).strip()

        if not typed_text:
            return

        elapsed_time = max(time.time() - self.start_time, 1)

        words = len(typed_text.split())
        wpm = round((words / elapsed_time) * 60)

        mistakes = self.calculate_mistakes(typed_text)

        accuracy = round(
            ((len(typed_text) - mistakes) / max(len(typed_text), 1)) * 100,
            2
        )

        progress = min(
            100,
            round((len(typed_text) / len(self.current_paragraph)) * 100, 1)
        )

        self.progress_bar["value"] = progress
        self.progress_label.config(text=f"Progress: {progress}%")
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.acc_label.config(text=f"Accuracy: {accuracy}%")
        self.mistake_label.config(text=f"Mistakes: {mistakes}")

        if wpm > self.best_wpm:
            self.best_wpm = wpm
            self.best_label.config(text=f"Best WPM: {self.best_wpm}")

        if typed_text.strip() == self.current_paragraph.strip():
            self.finish_test()

    def finish_test(self):

        if not self.timer_running:
            return

        self.timer_running = False

        typed_text = self.text_box.get("1.0", tk.END).strip()
        elapsed_time = max(time.time() - self.start_time, 1)

        total_words = len(self.current_paragraph.split())
        gross_wpm = round((total_words / elapsed_time) * 60)

        mistakes = self.calculate_mistakes(typed_text)
        net_wpm = max(0, gross_wpm - mistakes)

        accuracy = round(
            ((len(self.current_paragraph) - mistakes) / len(self.current_paragraph)) * 100,
            2
        )

        achievement = get_achievement(net_wpm)

        self.achievement_label.config(text=f"Achievement: {achievement}")

        try:
            pygame.mixer.music.play()
        except Exception:
            pass

        messagebox.showinfo(
            "Typing Test Result",
            f"""
Achievement: {achievement}
Gross WPM: {gross_wpm}
Net WPM: {net_wpm}
Accuracy: {accuracy}%
Mistakes: {mistakes}
Time Taken: {round(elapsed_time,2)} sec
"""
        )

        self.text_box.config(state="disabled")

    def restart_test(self):

        self.timer_running = False
        self.time_left = self.time_limit
        self.start_time = None

        self.timer_label.config(text=f"Time Left: {self.time_limit}")
        self.progress_bar["value"] = 0
        self.progress_label.config(text="Progress: 0%")

        self.wpm_label.config(text="WPM: 0")
        self.acc_label.config(text="Accuracy: 0%")
        self.mistake_label.config(text="Mistakes: 0")

        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)

        self.load_paragraph()


# if __name__ == "__main__":

#     root = tk.Tk()
#     app = TypingSpeedTester(root)
#     root.mainloop()
if __name__ == "__main__":
    app.run(debug=True)