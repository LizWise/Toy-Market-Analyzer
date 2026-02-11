import os 
import base64
import requests
import json
import glob
import sqlite3
from datetime import date, datetime, timedelta, timezone
from dotenv import load_dotenv

### Retrieve Client Credentials from Hidden .env ###

load_dotenv("production.env")

### Get Access Token from Authorization Server ###

def get_token():

    key = os.getenv("EBAY_CLIENT_ID")
    secret = os.getenv("EBAY_CLIENT_SECRET")

    token_url = "https://api.ebay.com/identity/v1/oauth2/token"

    scopes = "https://api.ebay.com/oauth/api_scope" 

    creds = f"{key}:{secret}"
    encoded_creds = base64.b64encode(creds.encode()).decode()

    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_creds}"
        }

    data = {
            "grant_type": "client_credentials",
            "scope": scopes
        }

    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json() 
    print("Your status code: ", response.status_code)

    access_token = token_data["access_token"]
   
    return access_token

x = get_token()

### Import Image Data from Image Directory ###
### Files Must be JPG, Names Should Reflect Name of Product ###

b64image_list = []

for images in glob.glob("./images/*.jpg"):
    with open(images, "rb") as f:
        data = f.read()

    b64_image = base64.b64encode(data).decode("utf-8")
    b64image_list.append(b64_image)

### Create Time Variables for Time Filter Parameter ###
et = datetime.now(timezone.utc)
st = et - timedelta(days = 2)
end = et.strftime('%Y-%m-%dT%H:%M:%SZ')
start = st.strftime('%Y-%m-%dT%H:%M:%SZ')

### POST to Resource Server Function (Calls API) ###

def get_items(image):
    uri = "https://api.ebay.com/buy/browse/v1/item_summary/search_by_image"

    headers = {
        "Authorization": f"Bearer {x}",
        "Accept": "application/json"
    }

    data = {
        "image" : image
    }

    params = {
       #"limit" : 1,
       "filter" : f"itemCreationDate:[{start}..{end}]"
    }

    response = requests.post(uri, headers=headers, json=data, params=params)
    items = response.json()
    return items

### Loops through Encoded Image List with POST Function and Adds Retrieved JSON to Listing Array ###

listings = []

for image in b64image_list:
    package = get_items(image)
    name = package["itemSummaries"]
    listings.append(name)

### Print Results ### 

print(json.dumps(listings, indent=4))
print(len(listings))

# package = get_items()
# print(package["categories"])







    


