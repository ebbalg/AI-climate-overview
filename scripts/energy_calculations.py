#!/usr/bin/env python
import os
import pandas as pd
from codecarbon import EmissionsTracker

# tracker = EmissionsTracker()

# tracker.start()

energy_score_dir = "../AI-climate-overview/data/AI-energy-leaderboard/"

def load_energy_data(task_file):
    """Load all models from file and make sure total GPU energy is Wh per query.
    """
    file_path = os.path.join(energy_score_dir, task_file)
    df = pd.read_csv(file_path)

    df["gpu_energy_Wh_per_query"] = (df["total_gpu_energy"] * 1000) / 1000  

    return df

def get_all_models_for_task(task_file):
    # file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)
    return df['model']

import os
import pandas as pd

def split_csv_by_provider(task_file):
    input_dir = os.path.dirname(task_file)
    
    task_name = os.path.splitext(os.path.basename(task_file))[0]
    
    # Build output folder path inside the same directory as the CSV
    output_dir = os.path.join(input_dir, task_name)
    os.makedirs(output_dir, exist_ok=True)

    # df = pd.read_csv(task_file)
    df = load_energy_data(task_file)

    # Extract provider (everything before the first '/')
    df["provider"] = df["model"].str.extract(r'^([^/]+)/')

    df = df.dropna(subset=["provider"])

    # Group by provider and write a CSV for each, including header
    for provider, group in df.groupby("provider"):
        provider_file = os.path.join(output_dir, f"{provider}.csv")
        group.drop(columns=["provider"]).to_csv(provider_file, index=False, header=True)


def get_all_models_from_provider(task_file, provider_name):
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)

    # Boolean mask of whether a model contains a provider_name string
    mask = df["model"].str.contains(provider_name, case=False, regex=False)
    return df.loc[mask]



def get_best_model_for_provider(task_file, provider_name):
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)

    # Filter models by provider name
    df_provider = df[df["model"].str.contains(f"{provider_name}/", case=False, regex=False)]

    if df_provider.empty:
        return None 
    
    # Get the row with the lowest energy
    best_model = df_provider.loc[df_provider['gpu_energy_Wh_per_query'].idxmin()]
    return best_model


def get_avg_energy_for_provider(task_file, provider_name):
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)

    # Filter models by provider name
    df_provider = df[df["model"].str.contains(f"{provider_name}/", case=False, regex=False)]

    if df_provider.empty:
        return None

    # Get average
    avg_energy = df_provider["gpu_energy_Wh_per_query"].mean()
    return avg_energy


def get_all_unique_providers(task_file):
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)

    # Match provider names 
    df["provider"] = df["model"].str.extract(r'^([^/]+)/')

    # Sort list with providers
    return sorted(df["provider"].dropna().unique())
    

def calculate_average_gpu_energy(task_file):
    """Calculate the estimated energy consumption per query for a specific task.

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
        avg_energy (float): The average energy across all models in Wh per query - converted from KWh/1000 queries.
    """
    
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)
    avg_energy = df['gpu_energy_Wh_per_query'].mean()
    return (avg_energy * 1000) / 1000


def find_lowest_energy_model(task_file):
    """Find the model with the lowest GPU energy of the models on the AI Energy Score Leaderboard and return its object.

    Args:
        task_file (string): a csv file path specific for the AI task.

    Returns:
    best_model (object): an object with the values of the row in the dataframe with the lowest total GPU energy.
    """
    file_path = os.path.join(energy_score_dir, task_file)
    # df = pd.read_csv(file_path)
    df = load_energy_data(task_file)
    best_model = df.loc[df['gpu_energy_Wh_per_query'].idxmin()]
    
    return best_model


def compare_with_average(model_obj, avg_gpu_energy):
    model_gpu_energy = model_obj['gpu_energy_Wh_per_query']
    
    return round(avg_gpu_energy / model_gpu_energy)


def get_comparison_df(model_obj, avg_gpu_energy):
    comparison_data = pd.DataFrame({
                 "Model": [model_obj["model"], "Average"],
                 "Energy (Wh)": [model_obj["gpu_energy_Wh_per_query"], avg_gpu_energy],
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
    # best_model_obj = find_lowest_energy_model("text_generation.csv")
    # # print(best_model_obj)

    # avg_gpu_energy = calculate_average_gpu_energy("text_generation.csv")
    # print("Best energy: ", best_model_obj["total_gpu_energy"])
    # print("Average energy: ", avg_gpu_energy)
    
    # print(compare_with_average(best_model_obj, avg_gpu_energy))
    
    # print(get_comparison_df(best_model_obj, avg_gpu_energy))
    
    # for model in get_all_models_for_task("text_generation.csv"):
    #     print(model)
    
    print(get_all_models_from_provider("text_generation.csv", "openai"))
    
    # for file in os.listdir("../AI-climate-overview/data/AI-energy-leaderboard/"):
    #     if file.endswith(".csv"):
    #         full_path = os.path.join("../AI-climate-overview/data/AI-energy-leaderboard/", file)
    #         print(f"Processing: {full_path}")
    #         split_csv_by_provider(full_path)
        
    # tracker.stop()


    # finally:
    #     _ = tracker.stop()
    
    



