# import requests
# from datetime import datetime
#
# USERNAME = "miftah"
# TOKEN = "hxsskgjcfhafxcgaghxd"
# pixela_endpoint = "https://pixe.la/v1/users"
# GRAPH_ID = "graph1"
#
# user_params = {
#     "token": TOKEN,
#     "username": USERNAME,
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes",
# }
#
# # Uncomment and run this line once to create the user
# # response = requests.post(url=pixela_endpoint, json=user_params)
# # print(response.text)
#
# graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
#
# graph_config = {
#     "id": GRAPH_ID,
#     "name": "Cycling Graph",
#     "unit": "KM",
#     "type": "float",
#     "color": "ajisai"
# }
#
# headers = {
#     "X-USER-TOKEN": TOKEN
# }
#
# # Uncomment and run this line once to create the graph
# # response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# # print(response.text)
#
# today = datetime.now()
#
# pixer_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
# pixel_data = {
#     "date": today.strftime("%Y%m%d"),
#     "quantity": input("How many kilometers did you cycle today?")
# }
#
# response = requests.post(url=pixer_creation_endpoint, json=pixel_data, headers=headers)
# print(response.text)  # Check if this returns a success message
#
# # Update the pixel
# update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
# new_pixel_data = {
#     "quantity": "4.5"
# }
#
# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# print(response.text)  # Check if this returns a success message
#
# # Delete the pixel
# # response = requests.delete(url=update_endpoint, headers=headers)
# # print(response.text)  # Check if this returns a success message

import requests
from datetime import datetime

USERNAME = "miftah"
TOKEN = "hxsskgjcfhafxcgaghxd"
pixela_endpoint = "https://pixe.la/v1/users"
GRAPH_ID = "graph1"

headers = {
    "X-USER-TOKEN": TOKEN
}

# Function to retrieve current data for debugging
def get_graph_data():
    graph_data_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
    response = requests.get(url=graph_data_endpoint, headers=headers)
    print("Current graph data response:", response.text)

# Get current data to see what is on the graph
get_graph_data()

# Correct date entry for the 6th month
correct_date = "20240615"  # Example date for June 15, 2024

# Input for the correct month
correct_quantity = input("How many kilometers did you cycle on the correct date? ")

pixel_data = {
    "date": correct_date,
    "quantity": correct_quantity
}

# Add or update the pixel data for the correct date
pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
print("Pixel creation response for correct date:", response.text)
