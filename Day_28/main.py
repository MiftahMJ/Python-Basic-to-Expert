from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
session_history = []

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        record_session()
        start_timer()
        update_check_marks()

def record_session():
    if reps % 8 == 0:
        session_history.append(("Long Break", LONG_BREAK_MIN))
    elif reps % 2 == 0:
        session_history.append(("Short Break", SHORT_BREAK_MIN))
    else:
        session_history.append(("Work", WORK_MIN))

def update_check_marks():
    marks = ""
    work_sessions = math.floor(reps / 2)
    for _ in range(work_sessions):
        marks += "✔"
    check_marks.config(text=marks)

# ------------------------ SETTINGS MENU -----------------------------------
def open_settings():
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.config(padx=20, pady=20, bg=YELLOW)

    work_label = Label(settings_window, text="Work Duration (min):", bg=YELLOW, font=(FONT_NAME, 12))
    work_label.grid(row=0, column=0)
    work_entry = Entry(settings_window)
    work_entry.grid(row=0, column=1)
    work_entry.insert(0, WORK_MIN)

    short_break_label = Label(settings_window, text="Short Break Duration (min):", bg=YELLOW, font=(FONT_NAME, 12))
    short_break_label.grid(column=0, row=1)
    short_break_entry = Entry(settings_window)
    short_break_entry.grid(column=1, row=1)
    short_break_entry.insert(0, SHORT_BREAK_MIN)

    long_break_label = Label(settings_window, text="Long Break Duration (min):", bg=YELLOW, font=(FONT_NAME, 12))
    long_break_label.grid(column=0, row=2)
    long_break_entry = Entry(settings_window)
    long_break_entry.grid(column=1, row=2)
    long_break_entry.insert(0, LONG_BREAK_MIN)

    def save_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
        WORK_MIN = int(work_entry.get())
        SHORT_BREAK_MIN = int(short_break_entry.get())
        LONG_BREAK_MIN = int(long_break_entry.get())
        settings_window.destroy()

    save_button = Button(settings_window, text="Save", command=save_settings)
    save_button.grid(column=0, row=3, columnspan=2)

# ---------------------------- SESSION HISTORY ---------------------------------
def show_history():
    history_window = Toplevel(window)
    history_window.title("Session History")
    history_window.config(padx=20, pady=20, bg=YELLOW)

    history_label = Label(history_window, text="Session History", font=(FONT_NAME, 20), bg=YELLOW)
    history_label.grid(column=0, row=0, columnspan=2)

    row = 1

    for session, duration in session_history:
        session_label = Label(history_window, text=f"{session}: {duration} min", bg=YELLOW, font=(FONT_NAME, 12))
        session_label.grid(column=0, row=row)
        row += 1

    total_work_time = sum(duration for session, duration in session_history if session == "Work")
    total_break_time = sum(duration for session, duration in session_history if session != "Work")
    total_sessions = len([session for session, duration in session_history if session == "Work"])

    summary_label = Label(
        history_window,
        text=f"Total work time: {total_work_time} min\nTotal break time: {total_break_time} min\nTotal sessions: {total_sessions}",
        bg=YELLOW,
        font=(FONT_NAME, 12)
    )
    summary_label.grid(column=0, row=row, columnspan=2)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50), bg=YELLOW)
timer_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

settings_button = Button(text="Settings", highlightthickness=0, command=open_settings)
settings_button.grid(column=1, row=3)

history_button = Button(text="History", highlightthickness=0, command=show_history)
history_button.grid(column=1, row=4)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=5)

window.mainloop()
