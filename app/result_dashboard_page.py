from datetime import datetime, timezone
import streamlit as st
import os 
import sys
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from codecarbon import OfflineEmissionsTracker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.energy_calculations import (calculate_average_gpu_energy, find_lowest_energy_model, compare_with_average, get_comparison_df, calculate_average_emissions_per_energy, get_all_models_for_task)
from scripts.get_carbon_data import get_carbon_factor, get_carbon_factor_pjm

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

# container for AI lifecycle
st.markdown("""
    <style>
    .bordered-container {
        border: 2px solid #000;
        border-radius: 8px;
        padding: 16px;
        width: 100%;
        box-sizing: border-box;
        max-width: 500px;
        margin: 0 auto;
        background-color: #f9f9f9;
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
    
    
# if "tracker" not in st.session_state:
#     st.session_state.tracker = OfflineEmissionsTracker(project_name="AI-climate-overview", output_dir="codecarbon_logs",
#         output_file="emissions.csv")
    
#     st.session_state.tracker.start()

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
data_retrieval_time_utc = country_emissions_data["date_utc"]
dt = datetime.strptime(data_retrieval_time_utc, "%Y-%m-%dT%H:%M:%S%z")
data_retrieval_time_utc = dt.strftime("%B %d, %Y at %I:%M %p UTC")
    
col1, col2 = st.columns([1, 3])

with col1:
    custom_metric(
        f"Estimated energy consumption per query in {st.session_state['location']}",
        f"{avg_gpu_energy:.4g} Wh",
        "This number is an average of the GPU Energy field of all models from the AI energy score leaderboard, formulated as watt-hours per query and rounded to four significant digits. This energy is just for using the model and does not account for manufacture or training. A LED light consumes 5-12 Wh."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # For faked API data:
    # custom_metric(
    #     "Estimated CO₂ Emissions per query",
    #     f"{estimated_emissions:.4g} g CO2eq",
    #     "This number is estimated based on the latest carbon intensity factor in Sweden, times the average GPU energy, rounded to four significant digits. The carbon intensity factor value is from retrieved from Nowtricity, data from UTC date 2025-07-09. Note that this is a simplification and that an AI model's energy use can depend on where its data center is located. "
    # )
    
    custom_metric(
        f"Estimated CO₂ Emissions per query in {st.session_state['location']}",
        f"{estimated_emissions:.4g} g CO₂eq",
        f"This number is estimated based on the latest carbon intensity factor in {st.session_state["location"]}, times the average GPU energy, rounded to four significant digits. The carbon intensity factor value is from retrieved from Nowtricity, data from {data_retrieval_time_utc}. Note that this is a simplification and that an AI model's energy use can depend on where its data center is located. "
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    queries = st.slider("How many user interactions with your AI model do you expect per user and day on average?", 1, 100, 1, help="An interaction could be a written prompt, uploading an image, document or sound file, or generating a new result.")
    # total_emission = queries*estimated_emissions
    f"Your chosen AI functionality usage is expected to generate {queries*estimated_emissions:.4g} g CO₂ per day and user"
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("Which AI models are included for calculation in these average values?"):
        st.write("These values are averages over all models from the AI Energy Score Leaderboard: ")
        models = get_all_models_for_task(csv_file)
        st.write(", ".join(models))

with col2:
    with st.container(border=True):
        st.markdown("## Scenario Dashboard ##")
        global_intensity_data = "data/Ember/ember_monthly_carbon-intensity-world.csv"
        us_intensity_data = "data/Ember/ember_monthly_carbon-intensity-us.csv"
        europe_intensity_data = "data/Ember/ember_monthly_carbon-intensity-europe.csv"
        
        # Estimated emissions calculation:
        global_df = pd.read_csv(global_intensity_data)
        global_df['emissions_per_query'] = global_df['emissions_intensity_gco2_per_kwh'].apply(
        lambda x: calculate_average_emissions_per_energy(x, avg_gpu_energy))
        
        us_df = pd.read_csv(us_intensity_data)
        us_df['emissions_per_query'] = us_df['emissions_intensity_gco2_per_kwh'].apply(
        lambda x: calculate_average_emissions_per_energy(x, avg_gpu_energy))
        
        europe_df = pd.read_csv(europe_intensity_data)
        europe_df['emissions_per_query'] = europe_df['emissions_intensity_gco2_per_kwh'].apply(
        lambda x: calculate_average_emissions_per_energy(x, avg_gpu_energy))
        
        st.markdown(f"Running your model on a cloud server or datacenter in {st.session_state['location']} would yield around {estimated_emissions:.4g} g CO₂eq per query according to Nowtricity data retreved on {data_retrieval_time_utc}.")
        st.markdown("Comparing the corresponding estimated emissions of the model with a European context to that with a global average carbon intensity factor or a US factor over time:")

        global_df['source'] = 'Global'
        us_df['source'] = 'US'
        europe_df['source'] = 'Europe'

        # Combine dataframes
        combined_df = pd.concat([global_df, us_df, europe_df], ignore_index=True)
        
        combined_df['date'] = pd.to_datetime(combined_df['date']).dt.strftime('%Y-%m')
        
        # Base line chart with color encoding for legend
        line = alt.Chart(combined_df).mark_line().encode(
            x=alt.X('date:O', title='Date', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('emissions_per_query:Q', title='Emissions per Query (gCO₂)'),
            color=alt.Color('source:N', title='Source')
        )

        # Create a nearest point selector on 'date' for hover
        nearest = alt.selection_point(
            nearest=True,
            on='mouseover',
            fields=['date'],
            empty='none'
        )

        # Invisible selectors for hover
        selectors = alt.Chart(combined_df).mark_point().encode(
            x='date:O',
            opacity=alt.value(0),
        ).add_params(
            nearest
        )

        # Points that become visible on hover
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Text labels for the points on hover
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'emissions_per_query:Q', alt.value(' '))
        )

        # Vertical rule at hover location
        rules = alt.Chart(combined_df).mark_rule(color='gray').encode(
            x='date:O',
        ).transform_filter(
            nearest
        )
        
        # Constant line for the chosen location’s current factor
        highlight_line = alt.Chart(pd.DataFrame({
            'y': [estimated_emissions],
            'label': [f'{st.session_state["location"]} Now: {estimated_emissions:.4g} gCO₂/query']
        })).mark_rule(color='red').encode(y='y:Q')

        text_label = highlight_line.mark_text(align='left', dx=5, dy=-5).encode(
            text='label:N'
        )

        # Combine all layers
        chart = alt.layer(
            line, selectors, points, rules, text, highlight_line, text_label
        ).properties(
            title='Estimated Emissions per AI Query Over Time (Europe vs Global vs US carbon intensity)'
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
        
        carbon_factor_data_pjm = get_carbon_factor_pjm()
        carbon_intensity_pjm = carbon_factor_data_pjm["carbon_intensity"]
        data_retrieval_time_utc_pjm = carbon_factor_data_pjm["date_utc"]   
        dt_pjm = datetime.strptime(data_retrieval_time_utc_pjm, "%Y-%m-%dT%H:%M:%S.%f%z")
        data_retrieval_time_utc_pjm = dt_pjm.strftime("%B %d, %Y at %I:%M %p UTC")
        estimated_emissions_pjm = calculate_average_emissions_per_energy(carbon_intensity_pjm, avg_gpu_energy) 
        
        st.markdown("A common datacenter location for cloud providers like Azure and Amazon Web Services is East US region, where the PJM grid region is one of the largest power grid operators.")
        st.markdown(f"Running the model on a datacenter in East US might produce around {estimated_emissions_pjm:.4g} g CO₂eq, according to data from the Electricity Maps API retrieved {data_retrieval_time_utc_pjm}.")
        
        percent_diff = ((estimated_emissions_pjm - estimated_emissions) / estimated_emissions_pjm) * 100
        st.markdown(f"""
        Running your AI service in **{st.session_state['location']}** is currently approximately **{percent_diff:.2g}% cleaner** per query than the current US East grid. 
        """)
        
        with st.expander("Data sources"):
            st.write("""
            - **Energy per query**: From the AI Energy Score Leaderboard.
            - **Local carbon intensity**: Retrieved from Nowtricity for your selected region.
            - **US and Global averages**: Monthly carbon intensity data from Ember Climate Reports.
            - **Carbon intensity for the PJM grid region**: Retrieved from Electricity Map for the PJM region.
            
            Note that these different data sources might have slightly different methodologies.
            """)
        

st.markdown("<br><br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Environmental impact", "AI Lifecycle", "About This Service"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(body='<h3 style="text-align: center"> Energy Score Leaderboard </h3>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"According to AI Energy Score, the most energy efficient model for {ai_functionality_choice.lower()} is {best_model_obj['model']}. \n \
                Compared to the average GPU energy on the AI Energy Score Leaderboard, this model is around {compare_with_average(best_model_obj, avg_gpu_energy)}x more energy efficient \
                    <a href='https://huggingface.co/spaces/AIEnergyScore/Leaderboard'>[See the leaderboard here]</a>", unsafe_allow_html=True)
        
        
        st.markdown(body='<h3 style="text-align: center"> Best Model VS Leaderboard Average </h3>', unsafe_allow_html=True)
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
        with st.container(border=True):
            with st.container(border=True):
                st.markdown(f"With around 10 queries a day per user and 10 users, your selected AI functionality might generate approximately {estimated_emissions*10*10*365:.4g} g CO₂eq per year.")
                
            with st.container(border=True):
                st.markdown("""Running a model inference consumes compute, so it uses electricity and produces CO₂ depending on the energy mix.
                            Key factors include the model and number of characters in the prompt, the hardware (GPU/TPU efficiency and utilization), and system overhead (power used by cooling, CPUs, networking, etc, often expressed by the data center's PUE - Power Usage). 
                            Software factors like caching responses can also affect energy per query.
                            Carbon emissions depend on the data center location and its grid's carbon intensity, so the location of the data center and its energy grid mix are crucial. 
                            Since this data is often complex to get access to, this service considers the country average carbon factor for your selected country. """)

with tab2:
    st.markdown(body= '<h3 style= "text-align: center"> The Lifecycle of GenAI models </h3>', unsafe_allow_html = True)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True, height=200):
            st.markdown(body='<h3 style="text-align: center"> Development  </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'Building AI infrastructure, such as hardware components and grid connection, requires natural resources and transportation.'
            '</p>', unsafe_allow_html = True)
    
    with col2:
        with st.container(border=True, height=200):
            st.markdown(body='<h3 style="text-align: center"> Training </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">''Data centers consumes energy during the training stage of GenAI. The emissions produced by this stage varies with the carbon intensity of the local energy mix'
            '</p>', unsafe_allow_html = True)
    

    with col3:
        with st.container(border=True, height=200):
            st.markdown(body='<h3 style="text-align: center"> Inference </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'When using GenAI, the energy consumed and emission produce varies depending on the size of the model and the type of utilization, such as a simple text prompt or video generation.'
            '</p>', unsafe_allow_html = True)
    
    


    with col4:
        with st.container(border=True, height=200):
            st.markdown(body='<h3 style="text-align: center"> Retirement </h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; font-size: 14px; font-weight: normal;">'
            'GenAI models retire when newer versions are developed or when the model can not be maintained. During its end-of-life stage, the hardware must be properly disposed to avoid environmental contamination.'
            '</p>', unsafe_allow_html = True)
            
            
with tab3:
    st.subheader("About This Service")
    with st.container(border=True):
        st.markdown("""The Climate Impact Overview aims to provide a simplified interface and playground for anyone that wants to reflect on the negative climate impact of using an AI model for solving an organizational issue.
                    Here you can compare the impact of different models, locations for inference (data centers and cloud provider services) and get actionable ideas for how to use AI in the most energy and carbon efficient way possible. 
                    On this dashboard, we focus only on AI inference, i.e. the usage of an AI functionality. Other parts of the AI lifecycle are overlooked as they are harder for a individual or an organization to control, and can be harder to understand and trust.
                    """)
    
    st.subheader("Real-time Emissions Tracking of This Service")
    
    # emissions_placeholder = st.empty()
    
    # emissions_log_file = "codecarbon_logs/emissions.csv"
    
    # if os.path.exists(emissions_log_file):
    #     emissions_df = pd.read_csv(emissions_log_file)
    #     # Show last CO₂ value
    #     last_co2 = emissions_df["emissions"].iloc[-1]
    #     emissions_placeholder.metric(
    #         "Estimated CO₂ Emissions",
    #         f"{last_co2:.4f} kg CO₂eq"
    #     )
    #    
    #     
    # else:
    #     st.info("Tracking will appear here once measurements are logged.")
    
    st.subheader("Contact")
    
    

