import tkinter as tk
from tkinter import messagebox
import pandas as pd

def validate_lat_long(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except ValueError:
        return False

def generate_excel(name, description, valid_data):
    data = [(name, description, lon, lat) for lon, lat in valid_data]
    df = pd.DataFrame(data, columns=['Name', 'Description', 'Longitude', 'Latitude'])
    df.to_excel('coordinates.xlsx', index=False)

def on_submit():
    data = text_box.get("1.0", tk.END).strip()
    name = name_entry.get().strip()
    description = description_entry.get().strip()

    if not data:
        messagebox.showerror("Error", "Input data cannot be empty.")
        return
    if not name:
        messagebox.showerror("Error", "Name cannot be empty.")
        return
    if not description:
        messagebox.showerror("Error", "Description cannot be empty.")
        return

    valid_data = []
    for row in data.split():
        if ',' in row:
            lon, lat = map(str.strip, row.split(',', 1))
            if validate_lat_long(lat, lon):
                valid_data.append((lon, lat))

    if valid_data:
        generate_excel(name, description, valid_data)
        messagebox.showinfo("Success", "Excel file has been generated successfully!")
    else:
        messagebox.showwarning("Warning", "No valid data to save.")

# Create the main window
root = tk.Tk()
root.title("Coordinate Processor")

# Create and place widgets
tk.Label(root, text="Enter data (Longitude, Latitude):").pack(padx=10, pady=10)
text_box = tk.Text(root, height=10, width=40)
text_box.pack(padx=10, pady=5)

tk.Label(root, text="Enter Name:").pack(padx=10, pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack(padx=10, pady=5)

tk.Label(root, text="Enter Description:").pack(padx=10, pady=5)
description_entry = tk.Entry(root, width=40)
description_entry.pack(padx=10, pady=5)

tk.Button(root, text="Generate Excel", command=on_submit).pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
