import streamlit as st

st.set_page_config(layout="centered")

st.markdown(body='<h1 style="text-align: center"> Climate Impact of AI Overview </h1>', unsafe_allow_html=True)


space = st.empty()
space.markdown("<br><br><br>", unsafe_allow_html=True)

query = st.text_input(
    label="", placeholder="What is your project idea?", label_visibility="collapsed"
)