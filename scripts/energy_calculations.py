#!/usr/bin/env python
import os
import pandas as pd
from codecarbon import EmissionsTracker

# tracker = EmissionsTracker()

# tracker.start()

energy_score_dir = "../AI-climate-overview/data/AI-energy-leaderboard/"

def get_all_models_for_task(task_file):
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)
    return df['model']
    

def calculate_average_gpu_energy(task_file):
    """Calculate the estimated energy consumption per query for a specific task.

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
        avg_energy (float): The average energy across all models in Wh per query - converted from KWh/1000 queries.
    """
    
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)
    avg_energy = df['total_gpu_energy'].mean()
    return (avg_energy * 1000) / 1000


def find_lowest_energy_model(task_file):
    """Find the model with the lowest GPU energy of the models on the AI Energy Score Leaderboard and return its object.

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
    best_model (object): an object with the values of the row in the dataframe with the lowest total GPU energy.
    """
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)
    best_model = df.loc[df['total_gpu_energy'].idxmin()]
    
    return best_model


def compare_with_average(model_obj, avg_gpu_energy):
    model_gpu_energy = (model_obj['total_gpu_energy'] * 1000) / 1000
    
    return round(avg_gpu_energy / model_gpu_energy)


def get_comparison_df(model_obj, avg_gpu_energy):
    comparison_data = pd.DataFrame({
            "Model": [model_obj["model"], "Average"],
            "Energy (Wh)": [model_obj["total_gpu_energy"], avg_gpu_energy]
    })
    
    return comparison_data
    

def calculate_average_emissions_per_energy(carbon_intensity, avg_energy_Wh):
    """Calculates the average g Co2eq for the given consumption of energy

    Args:
        carbon_factor (_type_): Carbon intensity factor [g Co2eq / kWh]
        avg_energy_Wh (_type_): Average energy for a specific task [Wh]

    Returns:
        average_emissions (float): Average emissions [g Co2eq].
    """
    carbon_factor_per_Wh = carbon_intensity / 1000        # Convert to g Co2eq / Wh
    average_emissions = carbon_factor_per_Wh * avg_energy_Wh
    
    return average_emissions

 
if __name__=='__main__':
    # try:
    
    # tracker.start()
    best_model_obj = find_lowest_energy_model("text_generation.csv")
    # print(best_model_obj)

    avg_gpu_energy = calculate_average_gpu_energy("text_generation.csv")
    print("Best energy: ", best_model_obj["total_gpu_energy"])
    print("Average energy: ", avg_gpu_energy)
    
    print(compare_with_average(best_model_obj, avg_gpu_energy))
    
    print(get_comparison_df(best_model_obj, avg_gpu_energy))
    
    for model in get_all_models_for_task("text_generation.csv"):
        print(model)
        
        
    # tracker.stop()


    # finally:
    #     _ = tracker.stop()
    
    



