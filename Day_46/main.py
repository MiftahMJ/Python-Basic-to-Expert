import requests
from bs4 import BeautifulSoup

# The URL of the webpage with historical song data
URL = "https://www.example.com/historical-top-songs?date=2001-08-01"

# Send a GET request to the URL
response = requests.get(URL)
website_html = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(website_html, "html.parser")

# Find all song entries (update the selector based on the actual site structure)
all_songs = soup.find_all(name="div", class_="song-entry")

# Extract text from each song element
songs = [song.get_text().strip() for song in all_songs]

# Write the song titles to a file
with open("top_100_songs.txt", mode="w") as file:
    for song in songs:
        file.write(song + "\n")

# Print number of songs found for verification
print(f"Number of songs found: {len(songs)}")
