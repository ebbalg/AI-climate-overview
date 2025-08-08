import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""   
    <style>
    .block-container {
            padding-top: 2rem;
    }

     /* Style back button */
        div.stButton > button:first-child {
            background-color: #66ccff; 
            color: black;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1.25rem;
            font-size: 1rem;
            cursor: pointer;
        }
        div.stButton > button:first-child:hover {
            background-color: #4dc3ff;
        }
    </style>
""", unsafe_allow_html=True)


# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.switch_page("start_page.py")


st.markdown("<br>", unsafe_allow_html=True)


st.subheader("About this service")

st.markdown("""The AI Footprint aims to provide an interface and playground for anyone that wants learn about the environmental impact of using an AI model, by quantifying environmental impact for different AI use cases and providing users a digital research-assistant specialized in this topic.
            You can compare the impact of different models, locations for inference (data centers and cloud provider services) and AI functionalities. In the AI Use Case Explorer, we focus only on AI inference, i.e. the usage of an AI functionality. Other parts of the AI lifecycle are overlooked as they are harder for a individual or an organization to control, 
            and can be harder to understand and trust. For the Research Overview, you can save relevant research to a research notebook on a specific generated research topic focusing on energy and carbon emissions. To promote transparency regarding this topic, we have added information throughout the application and acknowledged the environmental impact of this service itself through CodeCarbon tracking.
                """)

st.markdown("""This project was developed as a part of AI Sweden's Public Innovation Summer Program 2025, a national initiative supporting innovation in the public sector and civil society through applied AI.""")
st.markdown("<br>", unsafe_allow_html=True)


st.subheader("Contact")
    
url_ebba = "https://se.linkedin.com/in/ebba-lepp%C3%A4nen-gr%C3%B6ndal-910529170"
url_kajsa = "https://www.linkedin.com/in/kajsa-lidin-6288ba205/"
url_isabella = "https://se.linkedin.com/in/isabellafu001"
st.markdown(f"""Do you have any questions or feedback? Reach out to us at 
                [Kajsa Lidin]({url_kajsa}), [Ebba Leppänen Gröndal]({url_ebba}), or [Isabella Fu]({url_isabella}).""")
