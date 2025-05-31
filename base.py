import tkinter as tk
from tkinter import messagebox, ttk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.parent = parent
        self.on_close = on_close

        self.overrideredirect(True)
        self.geometry("500x200+500+300")
        self.configure(bg="#2c3e50")

        self.label = tk.Label(self, text="Welcome to Python Escape Room",
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

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Escape Room")
        self.root.geometry("800x600")
        self.level = 1
        self.questions = []
        self.create_level1()

    def create_level1(self):
        self.clear_window()
        self.level = 1
        self.questions = [
            {
                "question": "Fix the error in this code:\n\ndef divide(a, b):\n    return a / b\n\nprint(divide(10, 0))",
                "answer": "ZeroDivisionError",
                "hint": "Think about what happens when you divide a number by zero in Python."
            },
            {
                "question": "What will this print?\n\nclass Dog:\n    def bark(self):\n        return 'Woof!'\n\nd = Dog()\nprint(d.bark())",
                "answer": "Woof!",
                "hint": "The bark method returns a string. What does the last line print?"
            },
            {
                "question": "What will this print?\n\nclass Animal:\n    def sound(self):\n        raise NotImplementedError\n\nclass Dog(Animal):\n    def sound(self):\n        return 'Bark!'\n\na = Dog()\nprint(a.sound())",
                "answer": "Bark!",
                "hint": "Dog overrides the method in the Animal class. What gets printed?"
            }
        ]
        self.current_question = 0
        self.show_question()

    def create_level2(self):
        self.clear_window()
        self.level = 2
        self.questions = [
            {
                "question": "What will this print?\n\nclass Animal:\n    def speak(self): return '...'\n\nclass Dog(Animal):\n    def speak(self): return 'Bark'\n\nclass Cat(Animal):\n    def speak(self): return 'Meow'\n\nanimals = [Dog(), Cat()]\nfor a in animals:\n    print(a.speak())",
                "answer": "Bark Meow",
                "hint": "Each object calls its own version of `speak()`."
            },
            {
                "question": "Which regular expression matches most email addresses?",
                "answer": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
                "hint": "Include username, @, domain, and TLD using regex symbols like +, ., and []."
            },
            {
                "question": "What does this print?\n\nimport re\ntext = 'My phone number is 0803-456-7890'\nprint(re.findall(r'\\d+', text))",
                "answer": "['0803', '456', '7890']",
                "hint": "The pattern \\d+ finds groups of digits."
            }
        ]
        self.current_question = 0
        self.show_question()

    def create_level3(self):
        self.clear_window()
        self.level = 3
        self.questions = [
            {
                "question": "What widget does this code create?\n\nimport tkinter as tk\nroot = tk.Tk()\nentry = tk.Entry(root)\nentry.pack()\nroot.mainloop()",
                "answer": "Entry",
                "hint": "It's a single-line text input field."
            },
            {
                "question": "What shape does this code draw?\n\nimport turtle\nt = turtle.Turtle()\nt.circle(50)",
                "answer": "Circle",
                "hint": "The turtle draws a round shape with the specified radius."
            },
            {
                "question": "What happens when the button is clicked?\n\nimport tkinter as tk\ndef say_hello():\n    print('Hello')\n\nroot = tk.Tk()\nbtn = tk.Button(root, text='Click me', command=say_hello)\nbtn.pack()\nroot.mainloop()",
                "answer": "Prints Hello",
                "hint": "Check the function triggered by the button."
            }
        ]
        self.current_question = 0
        self.show_question()

    def show_question(self):
        self.clear_window()
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.label = tk.Label(self.root, text=f"Level {self.level} - Question {self.current_question + 1}\n\n{q['question']}", wraplength=700, justify="left", font=("Arial", 12))
            self.label.pack(pady=10)

            self.entry = tk.Entry(self.root, width=80, font=("Arial", 12))
            self.entry.pack(pady=5)

            self.submit_btn = tk.Button(self.root, text="Submit", command=self.check_answer, font=("Arial", 12))
            self.submit_btn.pack(pady=10)

            self.hint_btn = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Arial", 12))
            self.hint_btn.pack()
        else:
            self.show_success()

    def check_answer(self):
        user_answer = self.entry.get().strip()
        correct_answer = self.questions[self.current_question]["answer"]
        # Compare ignoring case and spaces, allow \n in answers
        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Correct!", "Nice job!")
            self.current_question += 1
            self.show_question()
        else:
            messagebox.showwarning("Try Again", "Incorrect answer. Please try again.")

    def show_hint(self):
        hint = self.questions[self.current_question]["hint"]
        messagebox.showinfo("Hint", hint)

    def show_success(self):
        if self.level == 1:
            messagebox.showinfo("Level 1 Complete", "You passed Level 1!")
            self.create_level2()
        elif self.level == 2:
            messagebox.showinfo("Level 2 Complete", "You passed Level 2!")
            self.create_level3()
        elif self.level == 3:
            messagebox.showinfo("🏁 Game Complete!", "Well done! You completed all 3 levels!\n\nThanks for playing!")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def start_game():
    root.deiconify()
    Game(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window at start

    splash = SplashScreen(root, start_game)
    root.mainloop()