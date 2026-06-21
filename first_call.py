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
        'regions': "us",  # Specify the regions you want odds for (e.g., 'us', 'eu', 'au')

        },

    )

    #response object contains servers responset to our requests. it has status code, headers, and content of the response. 


    

    result = response.json()  # Assuming the response is in JSON format, this will parse it into a Python dictionary or list depending on the structure of the JSON data.

    # Check if the request was successful --> a successful request will have a status code of 200

    if response.status_code == 200:
        
        #get status code
        print(response.status_code)
        print("API call successful!")
        print("Response content:", result)  # Assuming the response is in JSON format
        print("sports available:" , len(result))
        #print("First one:", result[0]["title"], "->", result[0]["key"])

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






def specific_sport_results():
    
    """
    when using 'odds' at end of url, you will get the odds for the specific sport.
    but you must include region param in the request, otherwise you will get an error.
    
    """
    key_for_url = 'mma_mixed_martial_arts'
    
    response = requests.get(
        f"{url}/{key_for_url}/odds", 
        params = {
        "apiKey": api_key,
        'regions': "us",  # Specify the regions you want odds for (e.g., 'us', 'eu', 'au')

        },

    )
    if response.status_code == 200:
        print("API call for specific sport successful!")
        result = response.json()
        print("Specific sport Response content:", result)  # Assuming the response is in JSON format
        print("Number of events available for this sport:", len(result))

    else:
        print("API call for specific sport failed with status code:", response.status_code)


   
   
   
   
   
   
    #run
if __name__ == "__main__":
    first_api_call()
    check_api_usage()
    specific_sport_results()