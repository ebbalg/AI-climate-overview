import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_carbon_factor(country):
    country = country.strip().lower()  # ensure correct format
    
    url = f"https://www.nowtricity.com/api/current-emissions/{country}/"
    
    api_key = os.getenv("NOWTRICITY_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Make sure NOWTRICITY_API_KEY is set in your .env file.")
    
    headers = {
    "X-Api-Key": api_key
    }
    
    try:
        # GET request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        response = response.json()
        
        carbon_intensity = response["emissions"]["value"]
        unit = response["emissions"]["unit"]
        date_utc = response["emissions"]["dateUTC"]
        
        return {
            "carbon_intensity": carbon_intensity,
            "unit": unit,
            "date_utc": date_utc
        }
        
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return None
        

if __name__== "__main__":
    response_dict = get_carbon_factor("Sweden")
    if response_dict:
        print(f"{response_dict["carbon_intensity"]} {response_dict["unit"]}")
        print(f"UTC Date: {response_dict["date_utc"]}")
        
    else:
        print("Failed to fetch data.")