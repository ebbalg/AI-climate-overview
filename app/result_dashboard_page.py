import streamlit as st
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.energy_calculations import (calculate_average_gpu_energy, find_lowest_energy_model, calculate_average_emissions_per_energy)

st.set_page_config(layout="centered")

st.markdown(body='<h1 style="text-align: center"> Result dashboard </h1>', unsafe_allow_html=True)
space = st.empty()
space.markdown("<br>", unsafe_allow_html=True)

def custom_metric(label, value, tooltip_text):
    html = f"""
    <style>
    .tooltip-container {{
        position: relative;
        display: inline-block;
    }}

    .tooltip-container .tooltip-text {{
        visibility: hidden;
        width: 300px;
        background-color: #f0f0f0;
        text-align: left;
        border-radius: 6px;
        color: black;
        padding: 8px;
        position: absolute;
        bottom: -5px;
        left: 25px;
        z-index: 1;
        transform: translateY(100%);
        font-size: 12px;
    }}

    .tooltip-container:hover .tooltip-text {{
        visibility: visible;
    }}
    </style>

    <div style="border: 1px solid #DDD; border-radius: 10px; width:250px; padding: 12px; background-color: #FAFAFA; text-align: left;">
        <div style="font-weight: 600; font-size: 16px;">
            {label}
        </div>
        <div style="font-size: 20px; color: green; margin-top: 4px; text-align: center;">{value}
        <span class="tooltip-container">
                <span style="cursor: pointer;">{"💡"}</span>
                <span class="tooltip-text">{tooltip_text}</span>
            </span>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
    
    
# TODO: replace with real user chosen technologies
ai_functionality_choice = "text_generation"

if ai_functionality_choice == "text_generation":
    avg_gpu_energy = calculate_average_gpu_energy("text_generation.csv")
    
elif ai_functionality_choice == "text_classification":
    avg_gpu_energy = calculate_average_gpu_energy("text_classification.csv")
    
elif ai_functionality_choice == "speech_recognition":
    avg_gpu_energy = calculate_average_gpu_energy("asr.csv")


estimated_emissions = calculate_average_emissions_per_energy(16, avg_gpu_energy)    # TODO: retrieve real-time carbon intensity data?   
    
    
spacer1, col1, gap, col2 , spacer2 = st.columns([0.1, 1, 0.1, 1, 0.01])

with col1:
    custom_metric(
        "Estimated energy consumption per query",
        f"{avg_gpu_energy} Wh",
        "This number is an average of the GPU Energy field of all models from the AI energy score leaderboard, formulated as watt-hours per query and rounded to four decimals. This energy is just for using the model and does not account for manufacture or training"
    )
    
with col2:
    custom_metric(
        "Estimated CO₂ Emissions per query",
        f"{estimated_emissions} g CO2eq",
        "This number is estimated based on the latest carbon intensity factor in the country you have selected, times the average GPU energy that can be found on this page and rounded to four decimals. Note that this is a simplification and that an AI model's energy use can depend on where its data center is located. "
    )

# col1.metric("Estimated energy consumption per query", f"{avg_gpu_energy} Wh", border=True, help="This number is an average of the GPU Energy field of all models from the AI energy score leaderboard, formulated as watt-hours per query.")
# col2.metric("Estimated CO₂ Emissions per query", "0.2 g CO2eq", border=True)