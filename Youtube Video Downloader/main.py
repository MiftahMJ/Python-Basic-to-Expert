
# API AIzaSyC0Ccg1TZExTxZKPreq_Q4xU3aY7NAELik
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import webbrowser
import json
from pytube import YouTube

# API Key and other constants
API_KEY = 'AIzaSyC0Ccg1TZExTxZKPreq_Q4xU3aY7NAELik'
SEARCH_HISTORY_FILE = 'search_history.json'

def load_search_history():
    try:
        with open(SEARCH_HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_search_history(query):
    history = load_search_history()
    if query not in history:
        history.append(query)
        with open(SEARCH_HISTORY_FILE, 'w') as file:
            json.dump(history, file)

def extract_video_id(url):
    # Extract video ID from YouTube URL
    if 'youtube.com/watch?v=' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1]
    return None

def search_videos(query, page_token=None):
    # Search YouTube for videos matching the query
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={API_KEY}&maxResults=20'
    if page_token:
        url += f'&pageToken={page_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Failed to fetch data from YouTube")
        return {'items': [], 'nextPageToken': None}

def get_video_by_id(video_id):
    # Get video details by video ID
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Failed to fetch data from YouTube")
        return {'items': []}

def display_videos(videos, first_load=True):
    if first_load:
        for widget in results_frame.winfo_children():
            widget.destroy()

    for i, video in enumerate(videos):
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        thumbnail_url = video['snippet']['thumbnails']['default']['url']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Fetch the thumbnail image
        img_data = requests.get(thumbnail_url).content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((160, 90), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Create a frame for each video
        video_frame = tk.Frame(results_frame, bg="#f9f9f9", relief="raised", bd=2)
        video_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky='nsew')

        # Thumbnail
        label_img = tk.Label(video_frame, image=img, bg="#f9f9f9")
        label_img.image = img
        label_img.pack(side='left', padx=5)

        # Title and play & download buttons
        details_frame = tk.Frame(video_frame, bg="#f9f9f9")
        details_frame.pack(side='left', fill='both', expand=True, padx=5)

        label_title = tk.Label(details_frame, text=title, wraplength=160, justify='left', bg="#f9f9f9", font=("Arial", 10))
        label_title.pack(side='top', anchor='w')

        btn_play = tk.Button(details_frame, text="Play", command=lambda url=video_url: play_video(url), bg="#ff0000", fg="#ffffff", relief="flat", font=("Arial", 10, "bold"))
        btn_play.pack(side='left', anchor='w', pady=5, padx=5)

        btn_download = tk.Button(details_frame, text="Download", command=lambda url=video_url: download_video(url), bg="#00ff00", fg="#ffffff", relief="flat", font=("Arial", 10, "bold"))
        btn_download.pack(side='right', anchor='w', pady=5, padx=5)

    # Update grid weights
    results_frame.update_idletasks()
    for i in range(3):
        results_frame.grid_columnconfigure(i, weight=1)

def on_search():
    query = search_entry.get().strip()
    if not query:
        messagebox.showerror("Error", "Please enter a search query or URL")
        return

    # Check if the query is a URL or keyword
    if 'youtube.com/watch?v=' in query or 'youtu.be/' in query:
        video_id = extract_video_id(query)
        if video_id:
            video_data = get_video_by_id(video_id)
            videos = video_data.get('items', [])
            if videos:
                display_videos(videos)
            else:
                messagebox.showinfo("No Results", "No video found with the provided URL.")
        else:
            messagebox.showerror("Error", "Invalid YouTube URL.")
    else:
        save_search_history(query)
        videos_data = search_videos(query)
        display_videos(videos_data['items'])
        global next_page_token
        next_page_token = videos_data.get('nextPageToken')

def load_more_videos(event):
    global next_page_token
    if next_page_token:
        videos_data = search_videos(search_entry.get().strip(), next_page_token)
        display_videos(videos_data['items'], first_load=False)
        next_page_token = videos_data.get('nextPageToken')

def play_video(url):
    # Open the video URL in the default web browser
    webbrowser.open(url)

def download_video(url):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        file_path = video_stream.download()
        messagebox.showinfo("Success", f"Video downloaded successfully: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

# Set up the main application window
app = tk.Tk()
app.title("YouTube Video Downloader")
app.geometry("1200x800")
app.configure(bg="#ffffff")

header_label = tk.Label(app, text="YouTube Video Downloader", font=("Arial", 16, "bold"), bg="#ff0000", fg="#ffffff", pady=10)
header_label.pack(fill='x')

search_frame = tk.Frame(app, pady=10, bg="#ffffff")
search_frame.pack(fill='x')

search_entry = tk.Entry(search_frame, width=60)
search_entry.pack(side='left', padx=5)

search_button = tk.Button(search_frame, text="Search", command=on_search, bg="#ff0000", fg="#ffffff", font=("Arial", 12, "bold"))
search_button.pack(side='left', padx=5)

# Scrollable Frame
scrollbar = tk.Scrollbar(app, orient="vertical")
scrollbar.pack(side='right', fill='y')

canvas = tk.Canvas(app, yscrollcommand=scrollbar.set, bg="#ffffff")
canvas.pack(side='left', fill='both', expand=True)

scrollbar.config(command=canvas.yview)

# Create a frame inside the canvas
results_frame = tk.Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=results_frame, anchor='nw')

# Update canvas scroll region
results_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

# Bind mouse wheel event for scrolling
canvas.bind_all("<MouseWheel>", load_more_videos)

# Initialize variables
next_page_token = None

# Run the application
app.mainloop()
