import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk
from tkcalendar import DateEntry
from datetime import datetime
from playsound import playsound
import sqlite3
import threading
import time

# Initialize the database
def setup_database():
    conn = sqlite3.connect('alarm_scheduler.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alarms ( 
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            comment TEXT,
            due_date TEXT,
            audio_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add a new alarm to the database
def add_alarm(name, description, comment, due_date, audio_path):
    conn = sqlite3.connect('alarm_scheduler.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO alarms (name, description, comment, due_date, audio_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, comment, due_date, audio_path))
    conn.commit()
    conn.close()

# Fetch all alarms from the database
def get_alarms():
    conn = sqlite3.connect('alarm_scheduler.db')
    c = conn.cursor()
    c.execute('SELECT * FROM alarms')
    alarms = c.fetchall()
    conn.close()
    return alarms

# Notify user
def notify_alarm(alarm_name, message, audio_path):
    if audio_path:
        try:
            playsound(audio_path)
        except Exception as e:
            print(f"Error playing sound: {e}")
    print(f"Alarm: {alarm_name}\nMessage: {message}")

# Alarm thread
def alarm_thread(alarm_id, due_date, audio_path):
    alarm_triggered = False
    while not alarm_triggered:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if current_time == due_date:
            alarm = [alarm for alarm in get_alarms() if alarm[0] == alarm_id]
            if alarm:
                notify_alarm(alarm[0][1], alarm[0][2], audio_path)
                alarm_triggered = True
        time.sleep(0.5)  # Check every half second

# GUI
class StylishAlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Scheduler")
        self.root.geometry("500x600")
        self.root.config(bg="#f0f0f0")  # Background color

        self.title_font = font.Font(size=16, weight='bold')

        # Title Label
        self.title_label = tk.Label(root, text="Alarm Scheduler", bg="#f0f0f0", font=self.title_font)
        self.title_label.pack(pady=20)

        # Alarm Name
        self.name_label = tk.Label(root, text="Alarm Name", bg="#f0f0f0", font=self.title_font)
        self.name_label.pack(pady=(20, 5))
        self.name_entry = tk.Entry(root, width=50, borderwidth=2, relief="groove", bg="#ffffff")
        self.name_entry.pack(pady=5)

        # Description
        self.desc_label = tk.Label(root, text="Description", bg="#f0f0f0", font=self.title_font)
        self.desc_label.pack(pady=(10, 5))
        self.desc_entry = tk.Entry(root, width=50, borderwidth=2, relief="groove", bg="#ffffff")
        self.desc_entry.pack(pady=5)

        # Comment
        self.comment_label = tk.Label(root, text="Comment", bg="#f0f0f0", font=self.title_font)
        self.comment_label.pack(pady=(10, 5))
        self.comment_entry = tk.Entry(root, width=50, borderwidth=2, relief="groove", bg="#ffffff")
        self.comment_entry.pack(pady=5)

        # Due Date
        self.due_date_label = tk.Label(root, text="Due Date", bg="#f0f0f0", font=self.title_font)
        self.due_date_label.pack(pady=(10, 5))
        self.due_date_picker = DateEntry(root, width=47, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.due_date_picker.pack(pady=5)
        self.due_time_entry = tk.Entry(root, width=50, borderwidth=2, relief="groove", bg="#ffffff")
        self.due_time_entry.pack(pady=5)
        self.due_time_entry.insert(0, "HH:MM:SS")

        # Audio File
        self.audio_path = None
        self.audio_button = tk.Button(root, text="Select Audio", command=self.select_audio, bg="#4CAF50", fg="#ffffff", borderwidth=0, relief="raised")
        self.audio_button.pack(pady=20)
        self.audio_label = tk.Label(root, text="No Audio File Selected", bg="#f0f0f0")
        self.audio_label.pack(pady=5)

        # Add Alarm Button
        self.add_alarm_button = tk.Button(root, text="Add Alarm", command=self.add_alarm, bg="#2196F3", fg="#ffffff", borderwidth=0, relief="raised")
        self.add_alarm_button.pack(pady=20)

        # Refresh Alarm List
        self.refresh_alarm_list()

    def select_audio(self):
        self.audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if self.audio_path:
            self.audio_label.config(text=f"Audio File: {self.audio_path}")
        else:
            self.audio_label.config(text="No Audio File Selected")

    def add_alarm(self):
        name = self.name_entry.get()
        description = self.desc_entry.get()
        comment = self.comment_entry.get()
        due_date = self.due_date_picker.get() + " " + self.due_time_entry.get()
        audio_path = self.audio_path

        if not name or not description or not comment or not due_date:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format")
            return

        add_alarm(name, description, comment, due_date, audio_path)
        self.refresh_alarm_list()

        threading.Thread(target=alarm_thread, args=(self.get_last_alarm_id(), due_date, audio_path)).start()

    def get_last_alarm_id(self):
        return get_alarms()[-1][0]

    def refresh_alarm_list(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget not in [self.title_label, self.name_label, self.desc_label, self.comment_label, self.due_date_label, self.audio_label]:
                widget.destroy()

        alarms = get_alarms()
        for idx, alarm in enumerate(alarms):
            tk.Label(self.root, text=f"Name: {alarm[1]}", bg="#f0f0f0").pack(pady=(5, 0))
            tk.Label(self.root, text=f"Due Date: {alarm[4]}", bg="#f0f0f0").pack(pady=(0, 10))

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = StylishAlarmApp(root)
    root.mainloop()
