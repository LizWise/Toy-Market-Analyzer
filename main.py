import os 
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv("sandbox.env")

def get_token():

    key = os.getenv("EBAY_CLIENT_ID")
    secret = os.getenv("EBAY_CLIENT_SECRET")

    token_url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

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

def get_items():
    uri = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"

    headers = {
        "Authorization": f"Bearer {x}",
        "Accept": "application/json"
    }

    params = {
        "q" : "pokemon",
        "limit" : 1,
        }

    response = requests.get(uri, headers=headers, params=params)
    items = response.json()
    return items

package = get_items()
item = package["itemSummaries"]

list = " "

for title in item:
    list += title["title"]


print(title)







    


