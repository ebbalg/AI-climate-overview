import streamlit as st
import os 
import sys
import altair as alt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.energy_calculations import (calculate_average_gpu_energy, find_lowest_energy_model, compare_with_average, get_comparison_df, calculate_average_emissions_per_energy)
from scripts.get_carbon_data import get_carbon_factor

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #F7FFF7;
        }
        .block-container {
            padding-top: 2rem;
        }
        .info-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: left;
            height: 180px;
            width: 90%;
        }
        .info-card h4 {
            margin-bottom: 10px;
        }
        .info-card p {
            margin-bottom: 20px;
        }

        /* Style Streamlit buttons */
        div.stButton > button:first-child {
            background-color: #66ccff;
            color: black;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        div.stButton > button:first-child:hover {
            background-color: #4dc3ff;
        }

        .small-card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            height: 160px;
        }
        .small-card h5 {
            margin: 0 0 10px 0;
        }

        /* Back button styling */
        .stButton>button.back {
            background-color: #66ccff;
            color: black;
            border: none;
            border-radius: 6px;
            padding: 6px 15px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.switch_page("project_query_page.py")

if "ai_function" not in st.session_state:
    st.error("No AI functionality selected. Please go back and complete the form.")
    st.stop()

st.markdown(body='<h1 style="text-align: center"> Climate Impact Overview </h1>', unsafe_allow_html=True)
space = st.empty()
space.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    challenge = st.text_input("Your challenge", f"{st.session_state['challenge']}")
    
    ai_function = st.text_input("Chosen functionality", f"{st.session_state['ai_function']}")

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
    
ai_functionality_choice = st.session_state["ai_function"] 

if ai_functionality_choice == "Text generation":
    csv_file = "text_generation.csv"
    
elif ai_functionality_choice == "Text classification":
    csv_file = "text_classification.csv"
    
elif ai_functionality_choice == "Speech recognition":
    csv_file = "asr.csv"
    
elif ai_functionality_choice == "Image generation":
    csv_file = "image_generation.csv"
    
elif ai_functionality_choice == "Image classification":
    csv_file = "image_classification.csv"


avg_gpu_energy = calculate_average_gpu_energy(csv_file)
best_model_obj = find_lowest_energy_model(csv_file)

country_emissions_data = get_carbon_factor(st.session_state["location"])

estimated_emissions = calculate_average_emissions_per_energy(country_emissions_data["carbon_intensity"], avg_gpu_energy)  
    
col1, col2 = st.columns([1, 3])

with col1:
    custom_metric(
        "Estimated energy consumption per query",
        f"{avg_gpu_energy:.4g} Wh",
        "This number is an average of the GPU Energy field of all models from the AI energy score leaderboard, formulated as watt-hours per query and rounded to four significant digits. This energy is just for using the model and does not account for manufacture or training"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # For faked API data:
    # custom_metric(
    #     "Estimated CO₂ Emissions per query",
    #     f"{estimated_emissions:.4g} g CO2eq",
    #     "This number is estimated based on the latest carbon intensity factor in Sweden, times the average GPU energy, rounded to four significant digits. The carbon intensity factor value is from retrieved from Nowtricity, data from UTC date 2025-07-09. Note that this is a simplification and that an AI model's energy use can depend on where its data center is located. "
    # )
    
    custom_metric(
        "Estimated CO₂ Emissions per query",
        f"{estimated_emissions:.4g} g CO2eq",
        f"This number is estimated based on the latest carbon intensity factor in {st.session_state["location"]}, times the average GPU energy, rounded to four significant digits. The carbon intensity factor value is from retrieved from Nowtricity, data from UTC date {country_emissions_data["date_utc"]}. Note that this is a simplification and that an AI model's energy use can depend on where its data center is located. "
    )
    
with col2:
    with st.container(border=True):
        st.markdown("**Real-time emissions tracker of using our service**", unsafe_allow_html=True)
        

st.markdown("<br><br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Environmental impact", "AI Lifecycle", "Resources & Recommendatioms"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(body='<h3 style="text-align: center"> Energy Score Leaderboard </h3>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"According to AI Energy Score, the most energy efficient model for {ai_functionality_choice.lower()} is {best_model_obj['model']}. \n \
                Compared to the average GPU energy on the AI Energy Score Leaderboard, this model is around {compare_with_average(best_model_obj, avg_gpu_energy)}x more energy efficient \
                    <a href='https://huggingface.co/spaces/AIEnergyScore/Leaderboard'>[See the leaderboard here]</a>", unsafe_allow_html=True)
        
        
        st.markdown(body='<h3 style="text-align: center"> Comparisons </h3>', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        comparison_data = get_comparison_df(best_model_obj, avg_gpu_energy)
        
        bar_chart = (
            alt.Chart(comparison_data)
            .mark_bar()
            .encode(
                x=alt.X("Energy (Wh):Q", title="Total Energy (Wh)"),     # Q for quantitative
                y=alt.Y("Model:N", sort="-x", title=""),                 # N for nominal
                color=alt.Color("Model:N", legend=None),
                tooltip=["Model", "Energy (Wh)"]
            )
            .properties(height=200, width=300)
        )

        st.altair_chart(bar_chart, use_container_width=True)
        
        
    with col2:
        st.markdown(body='<h3 style="text-align: center"> Impact estimation </h3>', unsafe_allow_html=True)

with tab2:
    col1, col2, col3, col4 = st.columns(4)

    st.markdown(body= '<h3 style= "text-align: center"> The Lifecycle of GenAI models </h3>', unsafe_allow_html = True)
    
    with col1:
        with st.container(border=True):
            st.markdown(body='<h3 style="text-align: center"> Development </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'Building AI infrastructure, such as hardware components and grid connection, requires natural resources and transportation.'
            '</p>', unsafe_allow_html = True)
    
    with col2:
        with st.container(border=True):
            st.markdown(body='<h3 style="text-align: center"> Training </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'Building AI infrastructure, such as hardware components and grid connection, requires natural resources and transportation.'
            '</p>', unsafe_allow_html = True)
    

    with col3:
        with st.container(border=True):
            st.markdown(body='<h3 style="text-align: center"> Inference </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'Building AI infrastructure, such as hardware components and grid connection, requires natural resources and transportation.'
            '</p>', unsafe_allow_html = True)

    with col4:
        with st.container(border=True):
            st.markdown(body='<h3 style="text-align: center"> Retirement </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'Building AI infrastructure, such as hardware components and grid connection, requires natural resources and transportation.'
            '</p>', unsafe_allow_html = True)
    
    

