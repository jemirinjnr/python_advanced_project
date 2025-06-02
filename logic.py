import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.parent = parent
        self.on_close = on_close

        self.overrideredirect(True)
        self.geometry("500x200+500+300")
        self.configure(bg="#2c3e50")

        self.label = tk.Label(self, text="Welcome to Escape Python Advanced",
                              font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50")
        self.label.pack(pady=30)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.progress_value = 0
        self.after(100, self.update_progress)

    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 2
            self.progress['value'] = self.progress_value
            self.after(60, self.update_progress)
        else:
            self.destroy()
            self.on_close()

class InstructionScreen(tk.Toplevel):
    def __init__(self, parent, on_start):
        super().__init__(parent)
        self.on_start = on_start
        self.title("Escape Python Advanced - How to Play")
        self.geometry("600x400+500+250")
        self.configure(bg="#000000")

        instruction_text = (
            "Welcome to the Game - Escape Python Advanced!\n\n"
            "In this game, you will go through 3 levels, each based on topics from your Python Advanced course.\n\n"
            "- Each level has 3 questions.\n"
            "- Correctly answering a question gives you 2 characters of a 6-character code.\n"
            "- The questions are shuffled — use your logic to arrange the code in the order of topics taught.\n"
            "- Enter the correct code to unlock the next level.\n\n"
            "Good luck!"
        )

        label = tk.Label(self, text=instruction_text, font=("Arial", 18), justify="left", wraplength=550,
                         bg="#000000", fg="#ffffff")
        label.pack(pady=20)

        start_btn = tk.Button(self, text="Start Game", font=("Arial", 20), bg="#ffffff", fg="#000000",
                              command=self.start_game)
        start_btn.pack(pady=20)

    def start_game(self):
        self.destroy()
        self.on_start()

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape Python Advanced")
        self.root.geometry("800x600")
        self.level = 1
        # Style for progress bar
        self.style = ttk.Style(self.root)
        self.style.theme_use('default')
        self.style.configure("Green.Horizontal.TProgressbar", foreground="#006400", background="#006400")

        self.bg_image = Image.open("background_fullscreen.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.frame = None

        self.levels = {
            1: lambda: self.load_questions_from_file(1),
            2: lambda: self.load_questions_from_file(2),
            3: lambda: self.load_questions_from_file(3)
        }
        self.start_level()

    def clear_window(self):
        if self.frame is not None:
            self.frame.destroy()

    def start_level(self):
        self.clear_window()
        self.questions = self.levels[self.level]()  # Get fresh questions list
        self.questions = random.sample(self.questions, len(self.questions))  # Shuffle fresh copy
        self.collected_codes = []
        self.current_question = 0

        # Reset hint tracking for the level
        self.hint_count = 0
        self.max_hints = 3

        self.show_question()

    def show_question(self):
        self.clear_window()
        self.frame = tk.Frame(self.canvas, bg="#000000", bd=0)
        self.frame.place(x=20, y=60)

        # NEW: Progress bar with dark green fill
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=300,
                                        mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress["maximum"] = len(self.questions)
        self.progress["value"] = self.current_question
        self.progress.pack(anchor="w", pady=(10, 0))

        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]

            self.label_header = tk.Label(self.frame,
                                         text=f"Level {self.level} - Question {self.current_question + 1}",
                                         font=("Arial", 20, "bold"), bg="#000000", fg="#0000ff")
            self.label_header.pack(anchor="w", pady=(0, 5))

            self.label_question = tk.Label(self.frame, text=q['question'],
                                           wraplength=1000, justify="left", font=("Arial", 18),
                                           bg="#000000", fg="#ffffff")
            self.label_question.pack(anchor="w", pady=(0, 10))

            self.entry = tk.Entry(self.frame, width=30, font=("Arial", 16))
            self.entry.pack(anchor="w", pady=(0, 10))

            self.submit_btn = tk.Button(self.frame, text="Submit", command=self.check_answer, font=("Arial", 16))
            self.submit_btn.pack(anchor="w", pady=(0, 5))

            self.hint_btn = tk.Button(self.frame, text="Hint", command=self.show_hint, font=("Arial", 16))
            self.hint_btn.pack(anchor="w")

            # NEW: Hint usage counter
            self.hint_counter_label = tk.Label(self.frame,
                                               text=f"Hints used: {self.hint_count}/{self.max_hints}",
                                               font=("Arial", 14), bg="#000000", fg="#ffcc00")
            self.hint_counter_label.pack(anchor="w", pady=(5, 0))
        else:
            self.prompt_code_entry()

    def check_answer(self):
        user_answer = self.entry.get().strip()
        correct_answer = self.questions[self.current_question]["answer"]

        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Correct!", f"Code segment received: "
                                            f"{self.questions[self.current_question]['code']}")
            self.collected_codes.append({
                'code': self.questions[self.current_question]['code'],
                'order': self.questions[self.current_question]['order']
            })
            self.current_question += 1
            self.progress["value"] = self.current_question  # Update progress bar
            self.show_question()
        else:
            messagebox.showwarning("Try Again", "Incorrect answer. Please try again.")

    def show_hint(self):
        if self.hint_count >= self.max_hints:
            messagebox.showwarning("Hint Limit Reached", "You have used all your hints for this level.")
            return

        self.hint_count += 1
        hint = self.questions[self.current_question]["hint"]

        # Custom hint popup window
        hint_window = tk.Toplevel(self.root)
        hint_window.title("Hint")
        hint_window.geometry("300x200")
        hint_window.configure(bg="#000000")  # Teal color

        label = tk.Label(hint_window, text=f"HINT ({self.hint_count}/{self.max_hints})",
                         font=("Arial", 18, "bold"), bg="#000000", fg="white")
        label.pack(pady=(20, 10))

        hint_label = tk.Label(hint_window, text=hint, wraplength=350, justify="center",
                              font=("Arial", 16), bg="#000000", fg="white")
        hint_label.pack(pady=(0, 20))

        ok_button = tk.Button(hint_window, text="Got it", command=hint_window.destroy,
                              font=("Arial", 16), bg="white", fg="black")
        ok_button.pack()

        # Update the hint usage display
        self.hint_counter_label.config(text=f"Hints used: {self.hint_count}/{self.max_hints}")

    def prompt_code_entry(self):
        self.clear_window()
        self.frame = tk.Frame(self.canvas, bg="#000000", bd=0)
        self.frame.place(x=20, y=20)

        self.label = tk.Label(self.frame, text=f"Level {self.level} Complete!\n\n"
                                               f"Enter the 6-character access code to continue:",
                              font=("Arial", 20), bg="#000000", fg="#ffffff")
        self.label.pack(anchor="w", pady=(0, 10))

        self.entry = tk.Entry(self.frame, width=20, font=("Arial", 18))
        self.entry.pack(anchor="w", pady=(0, 10))

        self.submit_btn = tk.Button(self.frame, text="Enter Code", command=self.verify_code, font=("Arial", 18))
        self.submit_btn.pack(anchor="w")

    def verify_code(self):
        entered_code = self.entry.get().strip()
        self.code_segments = [c['code'] for c in sorted(self.collected_codes, key=lambda x: x['order'])]
        correct_code = ''.join(self.code_segments)
        if entered_code == correct_code:
            if self.level == 3:
                messagebox.showinfo("🏁 Game Complete!", "You have escaped for now!\nYour project is next...")
                self.root.destroy()
            else:
                messagebox.showinfo("Access Granted", f"Welcome to Level {self.level + 1}!")
                self.level += 1
                self.start_level()
        else:
            messagebox.showerror("Access Denied", "Incorrect code. Please try again.")

    def load_questions_from_file(self, level):
        questions = []
        current_question = {}
        recording = False

        with open("questions.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip empty lines

                # Detect LEVEL line, case-insensitive and strip spaces
                if line.upper().startswith("LEVEL:"):
                    try:
                        current_level = int(line.split(":")[1].strip())
                    except Exception:
                        current_level = None
                    recording = (current_level == level)
                    if not recording and current_question:
                        questions.append(current_question)
                        current_question = {}
                    continue

                if not recording:
                    continue

                # Parse question fields
                if line.upper().startswith("QUESTION:"):
                    if current_question:
                        questions.append(current_question)
                        current_question = {}
                    current_question["question"] = line[len("QUESTION:"):].strip()
                elif line.upper().startswith("ANSWER:"):
                    current_question["answer"] = line[len("ANSWER:"):].strip()
                elif line.upper().startswith("HINT:"):
                    current_question["hint"] = line[len("HINT:"):].strip()
                elif line.upper().startswith("CODE:"):
                    current_question["code"] = line[len("CODE:"):].strip()
                elif line.upper().startswith("ORDER:"):
                    try:
                        current_question["order"] = int(line[len("ORDER:"):].strip())
                    except ValueError:
                        current_question["order"] = 0
                else:
                    # Append to question multiline (if exists)
                    if "question" in current_question:
                        current_question["question"] += "\n" + line

        # Append last question if any
        if current_question:
            questions.append(current_question)

        return questions


def start_game():
    def launch_main_game():
        root.deiconify()
        Game(root)

    InstructionScreen(root, launch_main_game)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    splash = SplashScreen(root, start_game)
    root.mainloop()