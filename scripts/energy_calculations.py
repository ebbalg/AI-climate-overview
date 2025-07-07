#!/usr/bin/env python
import os
import pandas as pd

energy_score_dir = "../AI-climate-overview/data/AI-energy-leaderboard/"

def calculate_average_gpu_energy(task_file):
    """Calculates the estimated energy consumption per query for a specific task.

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
        avg_energy (float): The average energy across all models in Wh per query - converted from KWh/1000 queries 
        and rounded to four decimal places.
    """
    
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)
    avg_energy = df['total_gpu_energy'].mean()
    return round((avg_energy * 1000) / 1000, 4)


def find_lowest_energy_model(task_file):
    """_summary_

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
        _type_: _description_
    """
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)
    best_model = df.loc[df['total_gpu_energy'].idxmin()]
    
    return best_model
    

def calculate_average_emissions_per_energy(carbon_intensity, avg_energy_Wh):
    """_summary_

    Args:
        carbon_factor (_type_): Carbon energy factor [g Co2eq / kWh]
        avg_energy_Wh (_type_): Average energy for a specific task [Wh]

    Returns:
        average_emissions (float): Average emissions [g], rounded to four decimal places.
    """
    carbon_factor_per_Wh = carbon_intensity / 1000
    average_emissions = carbon_factor_per_Wh * avg_energy_Wh
    
    return round(average_emissions, 4)
 
 
if __name__=='__main__':
    print(find_lowest_energy_model("text_generation.csv"))

    print(calculate_average_gpu_energy("text_generation.csv"))



