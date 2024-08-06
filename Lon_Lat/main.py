from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def validate_lat_long(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
        else:
            return False
    except ValueError:
        return False

def process_coordinates(data):
    valid_data = []
    invalid_data = []

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
    file_path = 'coordinates.xlsx'
    df.to_excel(file_path, index=False)
    return file_path

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/seo_tool', methods=['GET', 'POST'])
def seo_tool():
    if request.method == 'POST':
        data = request.form.get('coordinates')
        if not data:
            flash("Input data cannot be empty.", "error")
            return redirect(url_for('seo_tool'))

        valid_data, invalid_data = process_coordinates(data)
        if valid_data:
            file_path = generate_excel(valid_data)
            return send_file(file_path, as_attachment=True, download_name='coordinates.xlsx')
        else:
            flash("No valid data to save.", "warning")

    return render_template('seo_tool.html')

if __name__ == '__main__':
    app.run(debug=True)
