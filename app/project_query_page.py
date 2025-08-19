import streamlit as st

st.set_page_config(layout="wide")    

def set_background_gradient():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom right, #F7FFF7, #C1E1C1);
        }
        </style>
    """, unsafe_allow_html=True)

set_background_gradient()

st.markdown("""
    <style>
        body {
            background-color: #F7FFF7;
        }
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

        /* targets only the Analyze Climate Impact form submit button */
        div[data-testid="stFormSubmitButton"] > button:first-child {
        background-color: #66ccff !important;
        color: black      !important;

        }
        div[data-testid="stFormSubmitButton"] > button:first-child:hover {
        background-color: #4dc3ff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.switch_page("start_page.py")

st.markdown(
    body="""
    <h1 style="text-align: center">AI Use Case Explorer</h1>
    <h5 style="text-align: center">
        Choose a use case (organisation information, location and AI functionality) to explore
    </h5>
    <br><br>
    """,
    unsafe_allow_html=True
)

# Initialize session state defaults
defaults = {
    "organization": "",
    "location": "",
    "challenge": "",
    "ai_function": "Text generation"  
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
    
# Form for organization information, location and AI functionality
with st.form("my_form"):

    categ_col1, categ_col2 = st.columns([1, 1])

    with categ_col1:

        org_people = st.number_input(
            label="How many people work in your organisation?",
            min_value=0,
            step=1,
            value=st.session_state.get('org_people', 0),  # fallback to 0 if not set
        )

    with categ_col2:
        countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
        "Germany", "Greece", "Hungary", "Italy", "Latvia", "Lithuania", "Netherlands", "Norway", "Poland", "Portugal", 
        "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "United Kingdom"]
        location = st.selectbox(
            "Location of the data center",
            help = "The country where your AI model will run, usually where the provided cloud server or datacenter is placed.", 
            options=countries,
            placeholder="Country",
            index=countries.index(st.session_state.location) if st.session_state.location in countries else 24,
        )

    st.markdown("<br>", unsafe_allow_html=True)


    ai_options = ["Text generation", "Text classification", "Speech recognition", "Image generation", "Image classification", "Object detection", "Summarization", "Image captioning"] 
    ai_function = st.radio(
    "Which AI functionality would you like to use for your project?",  
    ai_options,
    index=ai_options.index(st.session_state.ai_function or "Text generation"),
    horizontal=True,
    )   
    
    with st.expander("**What does AI functionality mean and what should I choose?**"):
        st.markdown("""AI functionality here refers to the main task that the AI model will perform. The options are: <br><br>
        <b>Text generation</b>: Generating human-like text from a prompt, can be e.g. a chatbot <br>
        <b>Text classification</b>: Categorizing text into predefined labels, can be e.g. spam detection for emails <br>
        <b>Speech recognition</b>: Converting spoken language into text, for example for transcription <br>
        <b>Image generation</b>: Generating images from a description <br>
        <b>Image classification</b>: Assigning labels to objects or scenes in an image, e.g. detecting which animal is in an image <br>
        <b>Object detection</b>: Identifying and locating objects in images and video, e.g. detecting anomalies in medical scans <br>
        <b>Summarization</b>: Identifying key information and generate concise versions that retain the original meaning in text, documents etc. <br>
        <b>Image captioning</b>: Automatically generating textual descriptions for images
        """, 
        unsafe_allow_html=True)
        

    col1, spacer, col2, col3 = st.columns([1, 0.5,  1, 1])
    with col2:
        submitted = st.form_submit_button("Analyze climate impact")

    if submitted:
        st.session_state.location = location
        st.session_state.org_people = org_people
        st.session_state.ai_function = ai_function
        st.session_state.form_submitted = True
        st.success("Form submitted!")
        

if st.session_state.form_submitted:
    st.session_state.form_submitted = False  # Reset for next time
    st.switch_page("result_dashboard_page.py")
        