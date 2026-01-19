import os 
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv("sandbox.env")


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

access_token = token_data["access_token"]

    
print("Status Code: ", response.status_code)