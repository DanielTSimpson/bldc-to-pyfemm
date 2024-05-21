

#document URL ID:1904c992d834db0627d33fe5
# QS guide: https://onshape-public.github.io/docs/api-intro/quickstart/
#API key PlCZDgCx5HK7PrLn7nk45ZAA and the secret key is AIg1yWPoEm2MkyHVA8Yw4S5GQ5HXlJLp39rdwr4LNq6xMZ5H

#base-64 encoded string: UGxDWkRnQ3g1SEs3UHJMbjduazQ1WkFBOklnMXlXUG9FbTJNa3lIVkE4WXc0UzVHUTVIWGxKTHAzOXJkd3I0TE5xNnhNWjVI

# import requests 
# import json

# # Assemble the URL for the API call 
# api_url = "https://cad.onshape.com/api/documents/e60c4803eaf2ac8be492c18e"

# # Optional query parameters can be assigned 
# params = {}

# # Use the encoded authorization string you created from your API Keys.
# api_keys = ("UGxDWkRnQ3g1SEs3UHJMbjduazQ1WkFBOklnMXlXUG9FbTJNa3lIVkE4WXc0UzVHUTVIWGxKTHAzOXJkd3I0TE5xNnhNWjVI")

# # Define the header for the request 
# headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
#           'Content-Type': 'application/json'}


# # Put everything together to make the API request 
# response = requests.get(api_url, 
#                        params=params, 
#                        auth=api_keys, 
#                        headers=headers)

# # Convert the response to formatted JSON and print the `name` property
# print(json.dumps(response.json()["name"], indent=4))

import requests
import json


d_id = "1904c992d834db0627d33fe5"

# Assemble the URL for the API call
api_url = "https://cad.onshape.com/api/documents/" + d_id

# Optional query parameters can be assigned
params = {}

# Use the encoded authorization string you created from your API Keys.
api_key = "UGxDWkRnQ3g1SEs3UHJMbjduazQ1WkFBOklnMXlXUG9FbTJNa3lIVkE4WXc0UzVHUTVIWGxKTHAzOXJkd3I0TE5xNnhNWjVI"

# Define the header for the request
headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
           'Content-Type': 'application/json',
           'Authorization': api_key}

# Put everything together to make the API request
response = requests.get(api_url,
                        params=params,
                        headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     # Convert the response to formatted JSON and print the `name` property
#     print(json.dumps(response.json()["name"], indent=4))
# else:
#     # Print error message if the request was unsuccessful
#     print(f"Error: {response.status_code}")
#     print(response.text)

#print(response.json())

print(json.dumps(response.json()["name"], indent=4))