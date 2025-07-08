import streamlit as st

st.set_page_config(layout="centered")

st.markdown(body='<h1 style="text-align: center"> Climate Impact of AI Overview </h1>', unsafe_allow_html=True)

space = st.empty()
space.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown(body='<h3 style="text-align: center"> What are you using the AI Climate Overview for? </h3>', unsafe_allow_html=True)

space = st.empty()
space.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
    <style> 
    div.stButton > button:first-child {
        background-color: #66ccff;
        border-radius: 10px;
        width: 240px;
        height: 170px;
        padding: 0.75em 1.5em;
        cursor: pointer;
        text-align: center;
        white-space: normal;
        font-size: clamp(0.7rem, 2vw, 1rem);
        display: flex; 
        color: black;
        justify-content: center;
        align-items: center;
    }
    div.stButton > button:first-child:hover {
        background-color: #85d8ff;
        color: black;
        border: 1px solid #66ccff;
    }   
    </style>
    """, unsafe_allow_html=True)

spacer1, col1, gap, col2 , spacer2 = st.columns([0.17, 1, 0.1, 1, 0.01])
with col1:
    project_query_option = st.button("I have an AI project idea and want to weigh the benefits with the environmental costs")
with col2:
    general_overview_option = st.button("I want to get an overview of AI’s negative impact on the climate")


if project_query_option:
    st.switch_page("project_query_page.py")

if general_overview_option:
    st.switch_page("general_overview_page.py")
    