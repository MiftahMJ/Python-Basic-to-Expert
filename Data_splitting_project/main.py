import tkinter as tk
from tkinter import messagebox
import pandas as pd

def validate_lat_long(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        # Check if latitude and longitude are within valid ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
        else:
            return False
    except ValueError:
        return False

def process_coordinates(data):
    valid_data = []
    invalid_data = []

    # Split data into rows
    rows = data.strip().split(' ')
    for row in rows:
        if ',' in row:
            parts = row.split(',', 1)
            if len(parts) == 2:
                lon, lat = parts
                lon = lon.strip()
                lat = lat.strip()
                if validate_lat_long(lat, lon):
                    valid_data.append((lon, lat))
                else:
                    invalid_data.append((lon, lat))
        else:
            invalid_data.append(row.strip())

    return valid_data, invalid_data

def generate_excel(valid_data):
    df = pd.DataFrame(valid_data, columns=['Longitude', 'Latitude'])
    df.to_excel('coordinates.xlsx', index=False)

def on_submit():
    data = text_box.get("1.0", tk.END).strip()
    if not data:
        messagebox.showerror("Error", "Input data cannot be empty.")
        return

    valid_data, invalid_data = process_coordinates(data)
    if valid_data:
        generate_excel(valid_data)
        messagebox.showinfo("Success", "Excel file has been generated successfully!")
    else:
        messagebox.showwarning("Warning", "No valid data to save.")

# Create the main window
root = tk.Tk()
root.title("Coordinate Processor")

# Create and place widgets
tk.Label(root, text="Enter data (Longitude, Latitude):").pack(padx=10, pady=10)
text_box = tk.Text(root, height=20, width=80)
text_box.pack(padx=10, pady=10)

tk.Button(root, text="Generate Excel", command=on_submit).pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
