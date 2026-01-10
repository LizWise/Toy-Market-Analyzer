import os 
from dotenv import load_dotenv

load_dotenv("mysecrets.env")

key = os.getenv("EBAY_CLIENT_ID")
secret = os.getenv("EBAY_CLIENT_SECRET")

    
print(key, secret)