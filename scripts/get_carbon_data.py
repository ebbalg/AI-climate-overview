import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

def get_carbon_factor(country):
    """Get the carbon intensity factor and which date the value is from (according to Nowtricity).

    Args:
        country (string): the country which the user has inputted.

    Returns:
        _dict_: a dictorinary with the current carbon intensity in the country [g Co2eq / kWh] and the date in UTC time.
    """
    
    country = country.strip().lower()  # ensure standardized format
    
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
        date_utc = response["emissions"]["dateUTC"]
        
        return {
            "carbon_intensity": carbon_intensity,
            "date_utc": date_utc
        }
        
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return None


def get_carbon_factor_pjm():
    """
    Retrieve real-time carbon intensity [gCO₂/kWh] for the PJM Interconnection region 
    using the Electricity Maps API.

    Returns:
        dict: Dictionary with 'carbon_intensity' (gCO₂eq/kWh) and 'datetime_utc'.
    """
    
    api_key = os.getenv("ELECTRICITY_MAPS_API_KEY")
    
    url = "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=US-MIDA-PJM"
    
    headers = {
        "auth-token": api_key
    }
    
    response = requests.get(url, headers=headers)
    
    data = response.json()
    return {
        "carbon_intensity": data["carbonIntensity"],
        "date_utc": data["datetime"]
    }
        
        
def get_codecarbon_estimate():
    df = pd.read_csv('emissions.csv')
    
    emissions = df['emissions'].sum() * 1000    # g CO2eq
    energy_consumed = df['energy_consumed'].sum() * 1000   # Wh, sum of cpu_energy, gpu_energy and ram_energy
    timestamp = df['timestamp'].iloc[-1]
    
    # print(emissions)
    
    return {"emissions": emissions, "energy_consumed": energy_consumed, "timestamp":timestamp}



if __name__== "__main__":
    # response_dict = get_carbon_factor("Sweden")
    # if response_dict:
    #     print(f"{response_dict["carbon_intensity"]} g CO₂eq/Wh")
    #     print(f"UTC Date: {response_dict["date_utc"]}")
        
    # else:
    #     print("Failed to fetch data.")
    
    codecarbon_data = get_codecarbon_estimate()
    print(f"Emissions: {codecarbon_data["emissions"]}")
    print(f"Energy: {codecarbon_data["energy_consumed"]}")
    print(f"Time of calculation: {codecarbon_data["timestamp"]}")
    # print(get_codecarbon_estimate()["emissions"])
    # print(get_codecarbon_estimate()["energy_consumed"])
    # print(get_codecarbon_estimate()["timestamp"])
    
