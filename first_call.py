import os

import requests 
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv("OODS_API_KEY")

url = 'https://api.the-odds-api.com/v4/sports'

api_key = API_KEY


def first_api_call():
    
    

    response = requests.get(
        f"{url}", 
        params = {
        "apiKey": api_key,
        
        
        },

    )

    #response object contains servers responset to our requests. it has status code, headers, and content of the response. 


    



    # Check if the request was successful --> a successful request will have a status code of 200

    if response.status_code == 200:
        
        #get status code
        print(response.status_code)
        print("API call successful!")
        print("Response content:", response.json()[:2])  # Assuming the response is in JSON format
        print("sports available:" , len(response.json()))
        print("First one:", response.json()[0]["title"], "->", response.json()[0]["key"])

    else:
        print("API call failed with status code:", response.status_code)

    

def check_api_usage():

    

    response = requests.get(
        f"{url}",
        params = {
        "apiKey": api_key,
        },  

    )
    
    usage = response.headers.get("x-requests-remaining")

    if response.status_code == 200:
        print("API usage check successful!")
        print("API calls remaining:", usage)

    else:
        
        print("API usage check failed with status code:", response.status_code)


    #run
if __name__ == "__main__":
    first_api_call()
    check_api_usage()



        