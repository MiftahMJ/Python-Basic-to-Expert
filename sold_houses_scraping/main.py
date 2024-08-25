import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.compass.com/recently-sold/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container with the specific ID
    container = soup.find(id="browseNeighborhoodList-container")

    if container:
        # Extract and print text without HTML structure
        text_content = container.get_text(strip=True, separator="\n")
        print(text_content)
    else:
        print("Container with the specified ID not found.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")