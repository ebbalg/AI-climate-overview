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

        /* Custom styling for summary card */
        .summary-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: left;
            margin-bottom: 20px;
        }

        /* Custom styling for references card */
        .references-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: left;
            margin-bottom: 20px;
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
        st.switch_page("GHG_emissions_page.py")


st.markdown('<h1 style="text-align: center;"> GHG Emissions from GenAI </h1>', unsafe_allow_html=True)


st.markdown("**Research Question**")

if "GHG_user_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_user_question"] + "**")
elif "GHG_selected_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_selected_question"] + "**")


    
st.markdown("**Search Query**")


col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 style="text-align: left;"> Summary </h2>', unsafe_allow_html=True)
    st.markdown("""
        <div class="summary-card">
            <p>Summary text goes here.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<h2 style="text-align: left;"> References </h2>', unsafe_allow_html=True)
    st.markdown("""
        <div class="references-card">
            <p>Summary text goes here.</p>
        </div>
    """, unsafe_allow_html=True)
