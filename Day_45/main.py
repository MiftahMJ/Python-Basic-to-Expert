# from bs4 import BeautifulSoup
# #
# # with open("website.html") as file:
# #     contents = file.read()
# # soup = BeautifulSoup(contents, "html.parser")
# #
# # all_tags=soup.find_all(name="p")
# # for tag in all_tags:
# #  # print(tag.getText())
# # heading=soup.find_all(name="h1", id="name")
# #
# #
# import requests
# response=requests.get("https://news.ycombinator.com/news")
# yc_web_page=response.text
# soup=BeautifulSoup(yc_web_page,"html.parser")
#
#
#
# article_tag=soup.find_all(name="a", class_="storylink")
# article_text=article_tag.getText()
# article_link=article_tag.getText("href")
#
# article_upvote=soup.find_all(name="span",class_="score").getText()
# print(article_text)
# print(article_link)
# print(article_upvote)

import requests
from bs4 import BeautifulSoup

URL = "https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(URL)
website_html = response.text

# Print the first 500 characters of the HTML to check if the request was successful
print(website_html[:500])

soup = BeautifulSoup(website_html, "html.parser")
all_movies = soup.find_all(name="h3", class_="title")

# Print the number of movies found
print(f"Number of movies found: {len(all_movies)}")

# Print the titles to verify they are correct
for movie in all_movies:
    print(movie.getText())

movie_titles = [movie.getText() for movie in all_movies]
movies = movie_titles[::-1]

with open("movie.txt", mode="w") as file:
    for movie in movies:
        file.write(movie + "\n")
