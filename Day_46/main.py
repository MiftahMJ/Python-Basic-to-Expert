# from bs4 import BeautifulSoup
# import requests
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Scraping Billboard 100
# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
# response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
# soup = BeautifulSoup(response.text, 'html.parser')
# song_names_spans = soup.select("li ul li h3")
# song_names = [song.getText().strip() for song in song_names_spans]
#
# #Spotify Authentication
# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="http://localhost:8888/callback"
# ,
#         client_id="6d29eceba2b741b7ae1d8f358b370923",
#         client_secret="b65e7f1a71a94b698e39f5a8bf37e84c",
#         show_dialog=True,
#         cache_path="token.txt"
#     )
# )
# user_id = sp.current_user()["id"]
# print(user_id)
#
# #Searching Spotify for songs by title
# song_uris = []
# year = date.split("-")[0]
# for song in song_names:
#     result = sp.search(q=f"track:{song} year:{year}", type="track")
#     print(result)
#     try:
#         uri = result["tracks"]["items"][0]["uri"]
#         song_uris.append(uri)
#     except IndexError:
#         print(f"{song} doesn't exist in Spotify. Skipped.")
#
# #Creating a new private playlist in Spotify
# playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
#
# #Adding songs found into the new playlist
# sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id="6d29eceba2b741b7ae1d8f358b370923",
        client_secret="b65e7f1a71a94b698e39f5a8bf37e84c",
        show_dialog=True,
        cache_path="token.txt"
    )
)

# Check Token
token_info = sp.auth_manager.get_cached_token()
if token_info:
    print("Token successfully retrieved:", token_info['access_token'])
else:
    print("No token retrieved.")

user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
