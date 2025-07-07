import streamlit as st

st.set_page_config(layout="centered")
st.markdown(body='<h1 style="text-align: center"> Climate Impact of AI Overview </h1> '
'<p <h2 style="text-align: center"> Discover AI solution for your organization while understanding their <br> ' \
'environmental impact </p> </h2>', 
            
            unsafe_allow_html=True)



space = st.empty()
space.markdown("<br><br><br>", unsafe_allow_html=True)

categ_col1, categ_col2, = st.columns([1, 1])

with categ_col1:
        st.text_input(
        label="Organization", placeholder="Your organization name"
    )
        
with categ_col2:
        st.text_input(
        label="Location", placeholder="Your country"
    )
space = st.empty()
space.markdown("<br><br><br>", unsafe_allow_html=True)

query_challenge = st.text_input(
        label="What is your challenge?", placeholder="Describe the challenge or issue your organization is facing where AI might help")
