import os
from dotenv import load_dotenv
import requests
import pandas as pd
import sys
from codecarbon import EmissionsTracker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.energy_calculations import (calculate_average_gpu_energy, find_lowest_energy_model, compare_with_average, get_comparison_df, calculate_average_emissions_per_energy, get_all_models_for_task)

# tracker = EmissionsTracker()

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
        
        
def get_codecarbon_estimate(filename):
    df = pd.read_csv(filename)
    
    emissions = df['emissions'].sum() * 1000    # g CO2eq
    energy_consumed = df['energy_consumed'].sum() * 1000   # Wh, sum of cpu_energy, gpu_energy and ram_energy
    timestamp = df['timestamp'].iloc[-1]
    
    # print(emissions)
    
    return {"emissions": emissions, "energy_consumed": energy_consumed, "timestamp":timestamp}



if __name__== "__main__":
    # tracker.start()
    response_dict_swe = get_carbon_factor("Sweden")
        
    response_dict_pjm = get_carbon_factor_pjm()
    
    
    best_model_obj = find_lowest_energy_model("text_generation.csv")
    # print(best_model_obj)

    avg_gpu_energy = calculate_average_gpu_energy("text_generation.csv")
    print("Best energy: ", best_model_obj["total_gpu_energy"])
    print("Average energy: ", avg_gpu_energy)
    
    print(compare_with_average(best_model_obj, avg_gpu_energy))
    
    print(get_comparison_df(best_model_obj, avg_gpu_energy))
        
        
    print(calculate_average_emissions_per_energy(response_dict_swe["carbon_intensity"], avg_gpu_energy))
    print(calculate_average_emissions_per_energy(response_dict_pjm["carbon_intensity"], avg_gpu_energy))
    
    for model in get_all_models_for_task("text_generation.csv"):
        print(model)
        
        
    # tracker.stop()
        
    
    # codecarbon_data = get_codecarbon_estimate()
    # print(f"Emissions: {codecarbon_data["emissions"]}")
    # print(f"Energy: {codecarbon_data["energy_consumed"]}")
    # print(f"Time of calculation: {codecarbon_data["timestamp"]}")
    # print(get_codecarbon_estimate()["emissions"])
    # print(get_codecarbon_estimate()["energy_consumed"])
    # print(get_codecarbon_estimate()["timestamp"])
    
