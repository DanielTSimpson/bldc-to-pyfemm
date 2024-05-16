

import requests
import json

#tutorial: https://onshape-public.github.io/docs/api-intro/quickstart/


d_id = "4833676df7d2a808ac4b52b7"  #public document ID that works
d_id = "1904c992d834db0627d33fe5" #my document ID that doesn't permit access

# Assemble the URL for the API call
api_url = "https://cad.onshape.com/api/documents/" + d_id

# Optional query parameters can be assigned
params = {}

# Use the encoded authorization string you created from your API Keys.
api_key = ""

# Define the header for the request
headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
           'Content-Type': 'application/json',
           'Authorization': api_key}

# Put everything together to make the API request
response = requests.get(api_url,
                        params=params,
                        headers=headers)


print(response.json())
print(json.dumps(response.json()["name"], indent=4))