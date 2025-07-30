import streamlit as st

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
            margin: 0 0 5px 0;
        }

        .small-card p {
            margin: 0 0 0 0; 
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
        st.switch_page("start_page.py")

# Header + subheading
st.markdown('<h1 style="text-align: center;">Understanding AI’s Environmental Impact</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;font-weight: normal;">Learn more about the environmental aspects of AI usage that you and your organization can directly impact, and understand the broader context of AI’s environmental footprint.</h4>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<h3 style="text-align: center;">Environmental aspects you can impact</h3>', unsafe_allow_html=True)

spacer, col1, gap, col2, spacer2 = st.columns([0.25, 1, 0.1, 1, 0.2])

with col1:
    st.markdown("""
        <div class="info-card">
            <h4>Energy Consumption</h4>
            <p>Learn about the energy consumption of AI systems and the impact of your usage.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Learn more", key="energy"):
        st.switch_page("energy_use_page.py")

with col2:
    st.markdown("""
        <div class="info-card">
            <h4>GHG Emissions</h4>
            <p>Understand how AI systems contribute to greenhouse gas emissions and strategies for reduction.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Learn more", key="ghg"):
        st.switch_page("GHG_emissions_page.py")

# Section: Other considerations
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Other Environmental Considerations")

st.markdown("""
<p>While this navigator focuses on directly actionable aspects, it’s important to acknowledge that AI’s environmental impact extends beyond energy and carbon emissions. \n Some other examples are listed below.</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
        <div class="small-card">
            <h5>Water Usage</h5>
            <p>Data centers require significant water for cooling, but this varies greatly by location and provider.</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="small-card">
            <h5>Biodiversity</h5>
            <p>AI infrastructure requires significant land use, although it is difficult to quantify its impact on wildlife.</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="small-card">
            <h5>Electronic Waste</h5>
            <p>Hardware lifecycle and disposal impacts are challenging to quantify at the usage level.</p>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
        <div class="small-card">
            <h5>Environmental Contamination</h5>
            <p style="position: relative; top: -5px; z-index: 10;" > Building AI infrastructure carries the risk of releasing harmful substances into the environment.</p>
        </div>
    """, unsafe_allow_html=True)
