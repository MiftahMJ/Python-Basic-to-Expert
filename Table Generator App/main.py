import tkinter as tk
from tkinter import messagebox
import random


class TableGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Generator App")

        # Set window size and background color
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f5")  # Light gray background for the root window

        # Variables
        self.table_number = tk.IntVar(value=10)
        self.start_point = tk.IntVar(value=1)
        self.end_limit = tk.IntVar(value=10)

        # Create frames for different screens with background colors
        self.screen1 = tk.Frame(root, bg="#f0f0f5")  # Light gray
        self.screen2 = tk.Frame(root, bg="#e6e6fa")  # Lavender
        self.screen3 = tk.Frame(root, bg="#ffe4e1")  # Misty rose

        self.create_screen1()
        self.create_screen2()
        self.create_screen3()

        # Display the first screen
        self.screen1.pack(fill='both', expand=True)

    def create_screen1(self):
        # Widgets for screen 1
        tk.Label(self.screen1, text="Table Number", bg="#f0f0f5", fg="#444", font=("Arial", 12)).pack(pady=5)
        tk.Scale(self.screen1, from_=1, to=100, orient='horizontal', variable=self.table_number, bg="#dcdcdc",
                 troughcolor="#77b6ea", activebackground="#007acc", highlightthickness=0).pack()

        tk.Label(self.screen1, text="Table Starting Point", bg="#f0f0f5", fg="#444", font=("Arial", 12)).pack(pady=5)
        tk.Scale(self.screen1, from_=1, to=100, orient='horizontal', variable=self.start_point, bg="#dcdcdc",
                 troughcolor="#77b6ea", activebackground="#007acc", highlightthickness=0).pack()

        tk.Label(self.screen1, text="Table Ending Limit", bg="#f0f0f5", fg="#444", font=("Arial", 12)).pack(pady=5)
        tk.Scale(self.screen1, from_=1, to=100, orient='horizontal', variable=self.end_limit, bg="#dcdcdc",
                 troughcolor="#77b6ea", activebackground="#007acc", highlightthickness=0).pack()

        tk.Button(self.screen1, text="Generate Table", command=self.generate_table, bg="#2196F3", fg="#fff",
                  font=("Arial", 10), relief="raised").pack(pady=10)
        tk.Button(self.screen1, text="Next", command=self.show_screen2, bg="#2196F3", fg="#fff", font=("Arial", 10),
                  relief="raised").pack(pady=10)

    def create_screen2(self):
        # Widgets for screen 2
        self.table_display = tk.Text(self.screen2, height=10, width=30, bg="#ffffff", fg="#333", font=("Courier", 10),
                                     relief="sunken", borderwidth=2)
        self.table_display.pack(pady=10)

        tk.Button(self.screen2, text="Generate Quiz", command=self.generate_quiz, bg="#4CAF50", fg="#fff",
                  font=("Arial", 10), relief="raised").pack(pady=10)
        tk.Button(self.screen2, text="Refresh", command=self.refresh_screen2, bg="#FF5722", fg="#fff",
                  font=("Arial", 10), relief="raised").pack(pady=10)
        tk.Button(self.screen2, text="Back", command=self.show_screen1, bg="#FF5722", fg="#fff", font=("Arial", 10),
                  relief="raised").pack(side='left', padx=10)
        tk.Button(self.screen2, text="Next", command=self.show_screen3, bg="#FF5722", fg="#fff", font=("Arial", 10),
                  relief="raised").pack(side='right', padx=10)

    def create_screen3(self):
        # Widgets for screen 3
        self.quiz_label = tk.Label(self.screen3, text="", bg="#ffe4e1", fg="#000", font=("Arial", 12))
        self.quiz_label.pack(pady=10)

        self.quiz_buttons = []  # To store option buttons

        tk.Button(self.screen3, text="Back", command=self.show_screen2, bg="#FF5722", fg="#fff", font=("Arial", 10),
                  relief="raised").pack(side='left', padx=10)
        tk.Button(self.screen3, text="Refresh", command=self.refresh_screen3, bg="#FF5722", fg="#fff",
                  font=("Arial", 10), relief="raised").pack(side='right', padx=10)

    def show_screen1(self):
        self.screen2.pack_forget()
        self.screen3.pack_forget()
        self.screen1.pack(fill='both', expand=True)

    def show_screen2(self):
        self.screen1.pack_forget()
        self.screen3.pack_forget()
        self.screen2.pack(fill='both', expand=True)

    def show_screen3(self):
        self.screen1.pack_forget()
        self.screen2.pack_forget()
        self.screen3.pack(fill='both', expand=True)

    def generate_table(self):
        num = self.table_number.get()
        start = self.start_point.get()
        end = self.end_limit.get()

        self.table_display.delete(1.0, tk.END)
        for i in range(start, end + 1):
            self.table_display.insert(tk.END, f"{num} * {i} = {num * i}\n")

    def refresh_screen2(self):
        self.table_display.delete(1.0, tk.END)

    def generate_quiz(self):
        num = self.table_number.get()
        start = self.start_point.get()
        end = self.end_limit.get()

        if start > end:
            messagebox.showerror("Error", "Starting point should be less than or equal to ending limit.")
            return

        question_num = random.randint(start, end)
        self.correct_answer = num * question_num
        options = [self.correct_answer, self.correct_answer + 10, self.correct_answer - 10]
        random.shuffle(options)

        self.quiz_label.config(text=f"{num} * {question_num} = ?\nOptions: {options}")

        # Clear previous buttons
        for btn in self.quiz_buttons:
            btn.destroy()

        self.quiz_buttons = []  # Reset buttons list

        # Create new buttons for the options
        for option in options:
            button = tk.Button(self.screen3, text=str(option), command=lambda opt=option: self.check_answer(opt),
                               bg="#2196F3", fg="#fff", font=("Arial", 10), relief="raised")
            button.pack(pady=5)
            self.quiz_buttons.append(button)

    def check_answer(self, selected):
        if selected == self.correct_answer:
            messagebox.showinfo("Correct", "That's the right answer!")
        else:
            messagebox.showerror("Incorrect", f"Wrong answer. The correct answer was {self.correct_answer}.")

    def refresh_screen3(self):
        self.quiz_label.config(text="")
        for btn in self.quiz_buttons:
            btn.destroy()
        self.quiz_buttons = []  # Reset buttons list


if __name__ == "__main__":
    root = tk.Tk()
    app = TableGeneratorApp(root)
    root.mainloop()
