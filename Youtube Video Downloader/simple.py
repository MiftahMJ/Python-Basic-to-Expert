# import tkinter as tk
# from tkinter import messagebox
# from yt_dlp import YoutubeDL
#
# def download_video():
#     url = url_entry.get().strip()
#
#     if not url:
#         messagebox.showerror("Error", "Please enter a valid YouTube URL")
#         return
#
#     try:
#         print("Attempting to download video from URL:", url)
#         ydl_opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}
#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=True)
#             video_title = info.get('title', 'Video')
#             messagebox.showinfo("Success", f"Downloaded: {video_title}")
#     except Exception as e:
#         print("An error occurred:", str(e))
#         messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
#
# # Set up the GUI
# app = tk.Tk()
# app.title("YouTube Video Downloader")
#
# # URL Label and Entry
# url_label = tk.Label(app, text="YouTube URL:")
# url_label.pack()
#
# url_entry = tk.Entry(app, width=50)
# url_entry.pack()
#
# # Download Button
# download_button = tk.Button(app, text="Download", command=download_video)
# download_button.pack()
#
# # Run the application
# app.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from yt_dlp import YoutubeDL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import json

# Path to store download history
HISTORY_FILE = 'download_history.json'


def load_history():
    """Load download history from a JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_history(history):
    """Save download history to a JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)


def download_video():
    url = url_entry.get().strip()
    file_type = file_type_var.get()
    quality = quality_var.get()
    download_path = filedialog.askdirectory(title="Select Download Location")

    if not url or not download_path:
        messagebox.showerror("Error", "Please enter a valid YouTube URL and select a download location.")
        return

    # Define format options based on selected file type
    format_options = {
        "MP4": f"bestvideo[height<={quality.split('p')[0]}]+bestaudio/best" if file_type == "MP4" else None,
        "MP3": "bestaudio/best",
        "GIF": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
    }

    ydl_opts = {
        'format': format_options.get(file_type, 'best'),
        'outtmpl': os.path.join(download_path, f'%(title)s.{"mp3" if file_type == "MP3" else "mp4"}'),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if file_type == "MP3" else []
    }

    progress_bar['value'] = 0
    progress_bar.update()

    try:
        print("Attempting to download video from URL:", url)
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Video')

            # Save video info to history
            history = load_history()
            history.append({
                'title': video_title,
                'path': os.path.join(download_path, f'{video_title}.{"mp3" if file_type == "MP3" else "mp4"}'),
                'thumbnail': info.get('thumbnail')
            })
            save_history(history)

            messagebox.showinfo("Success", f"Downloaded: {video_title}")
    except Exception as e:
        print("An error occurred:", str(e))
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def fetch_video_info():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Video')
            thumbnail_url = info.get('thumbnail')
            show_thumbnail(thumbnail_url)
            title_label.config(text=video_title)
    except Exception as e:
        print("An error occurred while fetching video info:", str(e))
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def show_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.thumbnail((150, 150))  # Resize the image to fit in the label
    img_tk = ImageTk.PhotoImage(img)

    thumbnail_label.config(image=img_tk)
    thumbnail_label.image = img_tk


def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').strip()
        progress_bar['value'] = float(p.strip('%'))
        progress_bar.update()
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        progress_bar.update()


def show_history():
    history_window = tk.Toplevel(app)
    history_window.title("Download History")
    history_window.geometry("500x500")
    history_window.configure(bg="#2E2E2E")

    history_list = load_history()

    if not history_list:
        tk.Label(history_window, text="No download history found", font=("Helvetica", 12), bg="#2E2E2E",
                 fg="#E2DAD6").pack(pady=20)
        return

    for entry in history_list:
        frame = tk.Frame(history_window, bg="#F5EDED", borderwidth=1, relief="solid")
        frame.pack(pady=10, padx=10, fill='x')

        title_label = tk.Label(frame, text=entry['title'], font=("Helvetica", 12), bg="#F5EDED", fg="#6482AD")
        title_label.pack(side='left', padx=10)

        thumbnail_response = requests.get(entry['thumbnail'])
        thumbnail_img = Image.open(BytesIO(thumbnail_response.content))
        thumbnail_img.thumbnail((50, 50))
        thumbnail_tk = ImageTk.PhotoImage(thumbnail_img)

        thumbnail_label = tk.Label(frame, image=thumbnail_tk, bg="#F5EDED")
        thumbnail_label.image = thumbnail_tk
        thumbnail_label.pack(side='left')

        re_download_button = tk.Button(frame, text="Re-download", command=lambda path=entry['path']: re_download(path),
                                       bg="#4caf50", fg="white", relief="flat", padx=5, pady=2)
        re_download_button.pack(side='right', padx=10)


def re_download(path):
    try:
        os.startfile(path)  # Opens the file in default application, modify if needed
        messagebox.showinfo("Re-download", f"Re-downloading from path: {path}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# Set up the GUI
app = tk.Tk()
app.title("Cozy YouTube Video Downloader")
app.geometry("450x550")
app.configure(bg="#2E2E2E")  # Dark background color for the app window

# Card Frame
card_frame = tk.Frame(app, bg="#F5EDED", padx=20, pady=20, relief="solid", borderwidth=2, width=400)
card_frame.pack(padx=10, pady=10, fill='none', expand=False)

# URL Label and Entry
url_label = tk.Label(card_frame, text="YouTube URL:", font=("Helvetica", 12), bg="#F5EDED", fg="#6482AD")
url_label.pack(pady=(20, 5))

url_entry = tk.Entry(card_frame, width=50, font=("Helvetica", 10), relief="solid", borderwidth=2, bg="#E2DAD6",
                     fg="#6482AD")
url_entry.pack(pady=5)

# Fetch Info Button
fetch_button = tk.Button(card_frame, text="Fetch Info", command=fetch_video_info, font=("Helvetica", 10), bg="#6482AD",
                         fg="white", relief="flat", padx=10, pady=5)
fetch_button.pack(pady=5)

# Video Title
title_label = tk.Label(card_frame, text="", font=("Helvetica", 12), bg="#F5EDED", fg="#6482AD", wraplength=350)
title_label.pack(pady=10)

# Thumbnail Display
thumbnail_label = tk.Label(card_frame, bg="#F5EDED")
thumbnail_label.pack(pady=10)

# File Type Selection
file_type_var = tk.StringVar(value="MP4")
file_type_label = tk.Label(card_frame, text="Select File Type:", font=("Helvetica", 12), bg="#F5EDED", fg="#6482AD")
file_type_label.pack(pady=(10, 5))

file_type_menu = ttk.Combobox(card_frame, textvariable=file_type_var, state="readonly", width=10,
                              font=("Helvetica", 10))
file_type_menu['values'] = ("MP4", "MP3", "GIF")
file_type_menu.pack(pady=5)

# Quality Selection
quality_var = tk.StringVar(value="1080p")
quality_label = tk.Label(card_frame, text="Select Quality:", font=("Helvetica", 12), bg="#F5EDED", fg="#6482AD")
quality_label.pack(pady=(10, 5))

quality_menu = ttk.Combobox(card_frame, textvariable=quality_var, state="readonly", width=10, font=("Helvetica", 10))
quality_menu['values'] = ("360p", "480p", "720p", "1080p")
quality_menu.pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(card_frame, orient='horizontal', length=360, mode='determinate')
progress_bar.pack(pady=20)

# Download Button
download_button = tk.Button(card_frame, text="Download", command=download_video, font=("Helvetica", 12), bg="#4caf50",
                            fg="white", relief="flat", padx=10, pady=5)
download_button.pack(pady=10)

# History Button
history_button = tk.Button(card_frame, text="History", command=show_history, font=("Helvetica", 12), bg="#ff9800",
                           fg="white", relief="flat", padx=10, pady=5)
history_button.pack(pady=10)

app.mainloop()

