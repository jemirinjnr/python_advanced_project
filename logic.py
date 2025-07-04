import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import os

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
        self.geometry("700x600")
        self.configure(bg="#000000")
        # Create a hidden button (1x1 pixel) in the bottom-right corner
        hidden_btn = tk.Button(self, text="", command=self.open_admin_login,
                               bg="#000000", activebackground="#000000", borderwidth=0, highlightthickness=0)
        hidden_btn.place(x=680, y=560, width=20, height=20)  # small but clickable area

        # Optionally make the button completely transparent (harder to click but invisible)
        hidden_btn.config(bg=self['bg'], activebackground=self['bg'])

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

        self.selected = tk.StringVar(value="Medium")

        diff_label = tk.Label(self, text="Select Time Difficulty:", font=("Arial", 20, "bold"), bg="#000000", fg="white")
        diff_label.pack(pady=(10, 5))

        options = [("Easy (Unlimited Time)", "Easy"),
                   ("Medium (10 minutes)", "Medium"),
                   ("Hard (5 minutes)", "Hard"),
                   ("Impossible (3 minutes)", "Impossible")]

        for text, mode in options:
            rb = tk.Radiobutton(self, text=text, variable=self.selected, value=mode,
                                font=("Arial", 16), bg="#000000", fg="white",
                                selectcolor="#333333", activebackground="#222222", activeforeground="white")
            rb.pack(anchor="w", padx=60)

        start_btn = tk.Button(self, text="Start Game", font=("Arial", 20), bg="#ffffff", fg="#000000",
                              command=self.start_game)
        start_btn.pack(pady=20)

        quit_btn = tk.Button(self, text="Quit", font=("Arial", 16), bg="#ffffff", fg="#000000",
                             command=self.quit_game)
        quit_btn.pack()

    def open_admin_login(self, event=None):
        AdminLogin(self, self.open_admin_window)

    def open_admin_window(self):
        AdminWindow(self)

    def start_game(self):
        difficulty = self.selected.get()
        self.destroy()
        self.on_start(difficulty)

    def quit_game(self):
        self.destroy()
        self.master.destroy()
class AdminWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Panel")
        self.geometry("600x400")
        self.configure(bg="#1c1c1c")

        tk.Label(self, text="Admin Panel", font=("Arial", 20, "bold"),
                 bg="#1c1c1c", fg="white").pack(pady=20)

        tk.Button(self, text="View Questions File", font=("Arial", 16),
                  command=self.open_questions_file).pack(pady=10)

        tk.Button(self, text="Modify Question", font=("Arial", 16),
                  command=self.modify_question).pack(pady=5)

        tk.Button(self, text="Close", font=("Arial", 16),
                  command=self.destroy).pack(pady=20)

    def open_questions_file(self):
        filename = "questions.txt"
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"{filename} not found.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        top = tk.Toplevel(self)
        top.title("Questions File")
        top.geometry("700x500")
        text = tk.Text(top, wrap="word", font=("Courier", 12), bg="#000000")
        text.insert("1.0", content)
        text.config(state="disabled")
        text.pack(expand=True, fill="both")

    def modify_question(self):
        AdminModifyWindow(self)

def load_all_questions():
    # Returns list of dicts with keys: level, question, answer, hint, code, order
    if not os.path.exists("questions.txt"):
        messagebox.showerror("Error", f"{"questions.txt"} not found.")
        return []
    questions = []
    current_level = None
    question_data = {}
    buffer = []
    current_key = None

    def flush_buffer():
        nonlocal current_key, buffer, question_data
        if current_key and buffer:
            question_data[current_key] = "\n".join(buffer).strip()
        current_key = None
        buffer = []

    with open("questions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip("\n")
        if not line.strip():
            flush_buffer()
            if question_data:
                question_data.setdefault("level", current_level)
                questions.append(question_data)
            question_data = {}
            continue

        if line.startswith("# Level"):
            flush_buffer()
            try:
                current_level = int(line.split("Level")[1].strip())
            except:
                current_level = None
            question_data = {}
            continue

        if line.startswith("QUESTION:"):
            flush_buffer()
            current_key = "question"
            buffer = [line[len("QUESTION:"):].strip()]
        elif line.startswith("ANSWER:"):
            flush_buffer()
            current_key = "answer"
            buffer = [line[len("ANSWER:"):].strip()]
        elif line.startswith("HINT:"):
            flush_buffer()
            current_key = "hint"
            buffer = [line[len("HINT:"):].strip()]
        elif line.startswith("CODE:"):
            flush_buffer()
            current_key = "code"
            buffer = [line[len("CODE:"):].strip()]
        elif line.startswith("ORDER:"):
            flush_buffer()
            try:
                question_data["order"] = int(line[len("ORDER:"):].strip())
            except:
                question_data["order"] = 0
        else:
            buffer.append(line)

    flush_buffer()
    if question_data:
        question_data.setdefault("level", current_level)
        questions.append(question_data)

    return questions

def save_all_questions(questions):
    # questions is a list of dicts with keys level, question, answer, hint, code, order
    # Writes back to QUESTIONS_FILE in the same format
    with open("questions.txt", "w", encoding="utf-8") as f:
        current_level = None
        for q in questions:
            lvl = q.get("level")
            if lvl != current_level:
                current_level = lvl
                f.write(f"# Level {current_level}\n\n")
            f.write(f"ORDER: {q.get('order', 0)}\n")
            f.write(f"QUESTION: {q.get('question', '')}\n")
            f.write(f"ANSWER: {q.get('answer', '')}\n")
            f.write(f"HINT: {q.get('hint', '')}\n")
            f.write(f"CODE: {q.get('code', '')}\n\n")

class AdminModifyWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modify Questions")
        self.geometry("600x500")

        self.questions = load_all_questions()
        if not self.questions:
            self.destroy()
            return

        tk.Label(self, text="Select Level:").pack(pady=5)
        levels = sorted(set(q["level"] for q in self.questions if q["level"] is not None))
        self.level_var = tk.IntVar()
        self.level_cb = ttk.Combobox(self, values=levels, textvariable=self.level_var, state="readonly")
        self.level_cb.pack()
        self.level_cb.bind("<<ComboboxSelected>>", self.update_question_list)

        tk.Label(self, text="Select Question Order:").pack(pady=5)
        self.question_var = tk.IntVar()
        self.question_cb = ttk.Combobox(self, values=[], textvariable=self.question_var, state="readonly")
        self.question_cb.pack()
        self.question_cb.bind("<<ComboboxSelected>>", self.load_question_data)

        tk.Label(self, text="Question:").pack(pady=5)
        self.question_entry = tk.Text(self, height=4, width=70)
        self.question_entry.pack()

        tk.Label(self, text="Answer:").pack(pady=5)
        self.answer_entry = tk.Entry(self, width=70)
        self.answer_entry.pack()

        tk.Label(self, text="Hint:").pack(pady=5)
        self.hint_entry = tk.Entry(self, width=70)
        self.hint_entry.pack()

        tk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=15)

    def update_question_list(self, event=None):
        level = self.level_var.get()
        orders = sorted(q["order"] for q in self.questions if q["level"] == level)
        self.question_cb['values'] = orders
        if orders:
            self.question_cb.current(0)
            self.load_question_data()

    def load_question_data(self, event=None):
        level = self.level_var.get()
        order = self.question_var.get()
        for q in self.questions:
            if q["level"] == level and q["order"] == order:
                self.question_entry.delete('1.0', tk.END)
                self.question_entry.insert(tk.END, q.get("question", ""))
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.insert(0, q.get("answer", ""))
                self.hint_entry.delete(0, tk.END)
                self.hint_entry.insert(0, q.get("hint", ""))
                break

    def save_changes(self):
        level = self.level_var.get()
        order = self.question_var.get()
        question_text = self.question_entry.get('1.0', tk.END).strip()
        answer_text = self.answer_entry.get().strip()
        hint_text = self.hint_entry.get().strip()

        if not question_text or not answer_text:
            messagebox.showerror("Error", "Question and Answer cannot be empty.")
            return

        # Update the question in memory
        updated = False
        for q in self.questions:
            if q["level"] == level and q["order"] == order:
                q["question"] = question_text
                q["answer"] = answer_text
                q["hint"] = hint_text
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Selected question not found.")
            return

        # Save all questions back to the file
        save_all_questions(self.questions)
        messagebox.showinfo("Success", f"Level {level} question {order} updated and saved.")

class AdminLogin(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Admin Login")
        self.geometry("400x400")
        self.configure(bg="#1c1c1c")
        self.on_success = on_success
        self.credentials_file = "admin_credentials.txt"

        tk.Label(self, text="Admin Login", font=("Arial", 20, "bold"), bg="#1c1c1c", fg="white").pack(pady=10)

        tk.Label(self, text="Username:", bg="#1c1c1c", fg="white", font=("Arial", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#1c1c1c", fg="white", font=("Arial", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", font=("Arial", 14), command=self.check_login).pack(pady=10)

        tk.Label(self, text="---------------------------------------", bg="#222222", fg="white").pack(pady=5)

        tk.Label(self, text="Create Admin Account", font=("Arial", 16, "bold"), bg="#222222", fg="white").pack(pady=10)

        tk.Label(self, text="Username:", bg="#222222", fg="white").pack(anchor="w", padx=20)
        self.new_username_entry = tk.Entry(self, width=30)
        self.new_username_entry.pack(padx=20, pady=5)

        tk.Label(self, text="Password:", bg="#222222", fg="white").pack(anchor="w", padx=20)
        self.new_password_entry = tk.Entry(self, width=30, show="*")
        self.new_password_entry.pack(padx=20, pady=5)

        tk.Button(self, text="Create Account", command=self.create_account).pack(pady=15)

        if not os.path.exists(self.credentials_file):
            tk.Label(self, text="No admin account found. Please create one.", font=("Arial", 12), bg="#1c1c1c", fg="orange").pack()
            tk.Button(self, text="Create Admin", font=("Arial", 12), command=self.create_account).pack(pady=(5, 10))

    def create_account(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

            # Check if username already exists
        if self.check_username_exists(username):
            messagebox.showwarning("User Exists", "This username already exists. Choose another.")
            return

            # Save username and password
        with open("admin_credentials.txt", "a") as f:
            f.write(f"{username}:{password}\n")

        messagebox.showinfo("Success", "Admin account created successfully!")
        self.new_username_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)

    def check_username_exists(self, username):
        if not os.path.exists("admin_credentials.txt"):
            return False
        with open("admin_credentials.txt", "r") as f:
            for line in f:
                saved_username = line.strip().split(":")[0]
                if username == saved_username:
                    return True
        return False

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not os.path.exists(self.credentials_file):
            messagebox.showerror("Error", "No admin credentials found. Create an admin account.")
            return

        try:
            with open(self.credentials_file, "r") as f:
                credentials = [line.strip() for line in f if line.strip()]

            for cred in credentials:
                try:
                    stored_username, stored_password = cred.split(":")
                    if username == stored_username and password == stored_password:
                        messagebox.showinfo("Success", "Login successful!")
                        self.destroy()
                        self.on_success()
                        return  # Exit after successful login
                except ValueError:
                    continue  # Skip malformed lines

            messagebox.showerror("Error", "Incorrect username or password.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def load_questions_from_file(level):
        filename = "questions.txt"
        questions = []
        current_level = None

        if not os.path.exists(filename):
            messagebox.showerror("Missing File", f"{filename} not found.")
            return []

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        question_data = {}
        current_key = None
        buffer = []

        def flush_buffer():
            nonlocal current_key, buffer
            if current_key and buffer:
                question_data[current_key] = "\n".join(buffer).strip()
                current_key = None
                buffer = []

        for line in lines:
            line = line.rstrip("\n")

            if not line.strip():
                flush_buffer()
                if question_data and current_level == level:
                    questions.append(question_data)
                question_data = {}
                current_key = None
                buffer = []
                continue

            if line.startswith("# Level"):
                flush_buffer()
                try:
                    current_level = int(line.split("Level")[1].strip())
                except ValueError:
                    current_level = None
                question_data = {}
                current_key = None
                buffer = []
                continue

            if current_level == level:
                if line.startswith("QUESTION:"):
                    flush_buffer()
                    current_key = "question"
                    buffer = [line[len("QUESTION:"):].strip()]
                elif line.startswith("ANSWER:"):
                    flush_buffer()
                    current_key = "answer"
                    buffer = [line[len("ANSWER:"):].strip()]
                elif line.startswith("HINT:"):
                    flush_buffer()
                    current_key = "hint"
                    buffer = [line[len("HINT:"):].strip()]
                elif line.startswith("CODE:"):
                    flush_buffer()
                    current_key = "code"
                    buffer = [line[len("CODE:"):].strip()]
                elif line.startswith("ORDER:"):
                    flush_buffer()
                    current_key = "order"
                    try:
                        question_data["order"] = int(line[len("ORDER:"):].strip())
                    except ValueError:
                        question_data["order"] = 0
                    current_key = None
                    buffer = []
                else:
                    buffer.append(line)
        flush_buffer()
        if question_data and current_level == level:
            questions.append(question_data)

        return questions


class Game:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("Escape Python Advanced")
        self.root.geometry("800x600")
        self.level = 1

        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)

        self.style = ttk.Style(self.root)
        self.style.theme_use('default')
        self.style.configure("Green.Horizontal.TProgressbar", foreground="#006400", background="#006400")

        if not os.path.exists("background_fullscreen.png"):
            messagebox.showerror("Missing File", "Required background image not found.")
            self.root.destroy()
            return

        self.bg_image = Image.open("background_fullscreen.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.frame = None
        self.levels = {
            1: self.get_level1_questions,
            2: self.get_level2_questions,
            3: self.get_level3_questions
        }

        self.difficulty = difficulty
        self.time_left = self.set_time_for_difficulty(difficulty)
        self.timer_id = None

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                                    bg="#000000", fg="#ffffff")
        self.timer_label.place(x=650, y=50)

        self.collected_codes = []

        self.start_level()

        if self.time_left is not None:
            self.start_timer()
        else:
            self.timer_label.config(text="Unlimited Time")

    def confirm_quit(self):
        answer = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
        if answer:
            self.root.destroy()

    def add_quit_button(self):
        quit_btn = tk.Button(self.root, text="Quit", font=("Arial", 14),
                             command=self.confirm_quit, bg="#ffffff", fg="#000000")
        quit_btn.place(x=720, y=550)  # Adjust position as needed

    def set_time_for_difficulty(self, difficulty):
        return {
            "Easy": None,
            "Medium": 10 * 60,
            "Hard": 5 * 60,
            "Impossible": 3 * 60
        }.get(difficulty, None)

    def clear_window(self):
        if self.frame is not None:
            self.frame.destroy()

    def start_level(self):
        self.clear_window()
        self.collected_codes = []
        self.questions = self.levels[self.level]()
        self.shuffled_questions = self.questions.copy()
        random.shuffle(self.shuffled_questions)
        self.questions = self.shuffled_questions
        self.current_question = 0
        self.hint_count = 0
        self.max_hints = 3
        self.hint_window = None
        self.show_question()
        self.add_quit_button()

    def show_question(self):
        self.clear_window()
        self.frame = tk.Frame(self.canvas, bg="#000000", bd=0)
        self.frame.place(x=20, y=40)

        self.progress_bar = ttk.Progressbar(self.canvas, orient="horizontal", length=760,
                                            mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress_bar.place(x=20, y=20)
        self.progress_bar["maximum"] = len(self.questions)
        self.progress_bar["value"] = self.current_question

        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]

            tk.Label(self.frame, text=f"Level {self.level} - Question {self.current_question + 1}",
                     font=("Arial", 20, "bold"), bg="#000000", fg="#0000ff").pack(anchor="w", pady=(0, 5))

            tk.Label(self.frame, text=q['question'], wraplength=1000, justify="left",
                     font=("Arial", 18), bg="#000000", fg="#ffffff").pack(anchor="w", pady=(0, 10))

            self.answer_entry = tk.Entry(self.frame, width=30, font=("Arial", 16))
            self.answer_entry.pack(anchor="w", pady=(0, 10))

            tk.Button(self.frame, text="Submit", command=self.check_answer,
                      font=("Arial", 16)).pack(anchor="w", pady=(0, 5))

            self.hint_btn = tk.Button(self.frame, text="Hint", command=self.show_hint,
                                      font=("Arial", 16))
            self.hint_btn.pack(anchor="w")

            self.hint_counter_label = tk.Label(self.frame,
                                               text=f"Hints used: {self.hint_count}/{self.max_hints}",
                                               font=("Arial", 14), bg="#000000", fg="#ffcc00")
            self.hint_counter_label.pack(anchor="w", pady=(5, 0))
        else:
            self.prompt_code_entry()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.questions[self.current_question]["answer"]

        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Correct!", f"Code segment received: "
                                            f"{self.questions[self.current_question]['code']}")
            self.collected_codes.append({
                'code': self.questions[self.current_question]['code'],
                'order': self.questions[self.current_question]['order']
            })
            self.current_question += 1
            self.progress_bar["value"] = self.current_question
            self.show_question()
        else:
            messagebox.showwarning("Try Again", "Incorrect answer. Please try again.")

    def show_hint(self):
        if self.hint_count >= self.max_hints:
            messagebox.showwarning("Hint Limit Reached", "You have used all your hints for this level.")
            return

        if self.hint_window and self.hint_window.winfo_exists():
            return

        self.hint_count += 1
        hint = self.questions[self.current_question]["hint"]

        self.hint_window = tk.Toplevel(self.root)
        self.hint_window.title("Hint")
        self.hint_window.geometry("400x250")  # Increased from 300x200
        self.hint_window.configure(bg="#000000")

        tk.Label(self.hint_window, text=f"HINT ({self.hint_count}/{self.max_hints})",
                 font=("Arial", 18, "bold"), bg="#000000", fg="white").pack(pady=(20, 10))

        tk.Label(self.hint_window, text=hint, wraplength=350, justify="center",
                 font=("Arial", 16), bg="#000000", fg="white").pack(pady=(0, 20))

        tk.Button(self.hint_window, text="Got it", command=self.hint_window.destroy,
                  font=("Arial", 16), bg="white", fg="black").pack()

        self.hint_counter_label.config(text=f"Hints used: {self.hint_count}/{self.max_hints}")

    def prompt_code_entry(self):
        self.clear_window()
        self.frame = tk.Frame(self.canvas, bg="#000000", bd=0)
        self.frame.place(x=20, y=40)

        tk.Label(self.frame, text=f"Level {self.level} Complete!\n\n"
                                  f"Enter the 6-character access code to continue:",
                 font=("Arial", 20), bg="#000000", fg="#ffffff").pack(anchor="w", pady=(0, 10))

        self.code_entry = tk.Entry(self.frame, width=20, font=("Arial", 18))
        self.code_entry.pack(anchor="w", pady=(0, 10))

        tk.Button(self.frame, text="Enter Code", command=self.verify_code,
                  font=("Arial", 18)).pack(anchor="w")
        self.add_quit_button()

    def verify_code(self):
        entered_code = self.code_entry.get().strip()
        self.code_segments = [c['code'] for c in sorted(self.collected_codes, key=lambda x: x['order'])]
        correct_code = ''.join(self.code_segments)

        if entered_code.lower() == correct_code.lower():
            if self.level == 3:
                messagebox.showinfo("🏁 Game Complete!", "You have escaped for now!\nYour project is next...")
                self.root.destroy()
            else:
                messagebox.showinfo("Access Granted", f"Welcome to Level {self.level + 1}!")
                self.level += 1
                self.start_level()
        else:
            messagebox.showerror("Access Denied", "Incorrect code. Please try again.")

    def start_timer(self):
        if self.timer_id is None:  # Only start if no timer is running
            self.update_timer()

    def update_timer(self):
        if self.time_left is None:
            return

        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f"Time left: {mins:02d}:{secs:02d}")

        if self.time_left <= 0:
            messagebox.showinfo("Time's Up", "You have run out of time! Game over.")
            self.root.destroy()
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def cleanup_and_exit(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()

    # Question methods unchanged...
    def get_level1_questions(self):
        return load_questions_from_file(1)

    def get_level2_questions(self):
        return load_questions_from_file(2)

    def get_level3_questions(self):
        return load_questions_from_file(3)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    def start_game(difficulty):
        root.deiconify()
        Game(root, difficulty)

    def show_instructions():
        InstructionScreen(root, on_start=start_game)

    splash = SplashScreen(root, on_close=show_instructions)
    splash.mainloop()