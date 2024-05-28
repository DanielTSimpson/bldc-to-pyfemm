import requests
import json
import base64
import os

d_id = "1904c992d834db0627d33fe5"
wid = "5a63fb112dff50914a14f290"
eid = "ba92c1952bea766f0601ac2e"

api_url = "https://cad.onshape.com/api/documents/{did}/w/{wid}/elements/{eid}/parasolid"
params = {}
access_key = "PlCZDgCx5HK7PrLn7nk45ZAA"
secret_key = "AIg1yWPoEm2MkyHVA8Yw4S5GQ5HXlJLp39rdwr4LNq6xMZ5H"
credentials = access_key + ":" + secret_key
api_key = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


# Get the directory path where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create a subfolder named "exports" within the script directory
export_dir = os.path.join(script_dir, "test_exports")
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Specify the file path within the "exports" subfolder
#to do: figure out how to grab the file name and make it the export name
file_path = os.path.join(export_dir, "exported_file.par")


# Define the header for the request
headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
           'Content-Type': 'application/json',
           'Authorization': api_key}

# Put everything together to make the API request
response = requests.get(api_url,
                        params=params,
                        headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Write the response content to the specified file path
    with open(file_path, "wb") as f:
        f.write(response.content)
    print("Exported file saved successfully.")
else:
    # Print the error message
    print(f"Error: {response.status_code} - {response.text}")