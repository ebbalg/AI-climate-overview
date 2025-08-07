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
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 0.125rem 0.625rem rgba(0,0,0,0.05);
            text-align: left;
            height: 11.25rem;
            width: 90%;
        }
        .info-card h4 {
            margin-bottom: 0.625rem;
        }
        .info-card p {
            margin-bottom: 1.25rem;
        }

        /* Style Streamlit buttons */
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

        .small-card {
            background-color: #f9f9f9;
            border-radius: 0.625rem;
            padding: 1.25rem;
            height: 10rem;
        }
        .small-card h5 {
            margin: 0 0 0.625rem 0;
        }

        /* Back button styling */
        .stButton>button.back {
            background-color: #66ccff;
            color: black;
            border: none;
            border-radius: 0.375rem;
            padding: 0.375rem 0.938rem;
            font-size: 1rem;
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
    <h1 style="text-align: center">Climate Impact of AI Overview</h1>
    <h5 style="text-align: center">
        Discover AI solutions for your organization while understanding their <br>
        environmental impact
    </h5>
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
    
with st.form("my_form"):

    st.markdown("**Describe your organzation**") #Describe your challenge
    st.write("Fill in the information and we'll help you understand the AI solutions and their climate impact") #Summarize your organization's needs and we'll help you understand the AI solutions and their climate impact")


    categ_col1, categ_col2 = st.columns([1, 1])

    with categ_col1:
        # organization = st.text_input(
        #     label="Organization",
        #     placeholder="Your organization name",
        #     value=st.session_state.organization
        # )

        org_people = st.number_input(
            label="How many people work in your organization?",
            min_value=0,
            step=1,
            value=st.session_state.get('org_people', 0),  # fallback to 0 if not set
        )

    with categ_col2:
        countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
        "Germany", "Greece", "Hungary", "Italy", "Latvia", "Lithuania", "Netherlands", "Norway", "Poland", "Portugal", 
        "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden","United Kingdom"]
        location = st.selectbox(
            "Location of the data center",
            help = "The country where your AI model will run, usually where the provided cloud server or datacenter is placed.", 
            options=countries,
            placeholder="Country",
            index=countries.index(st.session_state.location) if st.session_state.location in countries else 24,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    
    # challenge = st.text_input(
    #     label="What is your challenge?",
    #     placeholder="Describe the challenge or issue your organization is facing where AI might help",
    #     value=st.session_state.challenge
    # )


    ai_options = ["Text generation", "Text classification", "Speech recognition", "Image generation", "Image classification", "Object detection", "Summarization", "Image captioning"] 
    ai_function = st.radio(
    "Which AI functionalities would you like to use for your project?",   #Which AI functionalities might help tackle this problem?
    ai_options,
    index=ai_options.index(st.session_state.ai_function or "Text generation"),
    horizontal=True,
    )   
    
    with st.expander("What does AI functionality mean and what should I choose?"):
        st.markdown("""AI functionality here refers to the main task that the AI model will perform. The options are: <br><br>
        <b>Text generation</b>: Generating human-like text from a prompt, can be e.g. a chatbot <br>
        <b>Text classification</b>: Categorizing text into predefined labels, can be e.g. spam detection for emails <br>
        <b>Speech recognition</b>: Converting spoken language into text, for example for transcription <br>
        <b>Image generation</b>: Generating images from a description <br>
        <b>Image classification</b>: Assigning labels to objects or scenes in an image, e.g. detecting which animal is in an image <br>
        <b>Object detection</b>: Identifying and locating objects in images and video, e.g. detecting anomalies in medical scans <br>
        <b>Summarization</b>: Identifying key information and generate concise versions that retain the original meaning in text, documents etc <br>
        <b>Image captioning</b>: Automatically generating textual descriptions for images
        """, 
        unsafe_allow_html=True)
        

    submitted = st.form_submit_button("Analyze Climate Impact")

    if submitted:
       # st.session_state.organization = organization
        st.session_state.location = location
       # st.session_state.challenge = challenge
        st.session_state.org_people = org_people
        st.session_state.ai_function = ai_function
        st.session_state.form_submitted = True
        st.success("Form submitted!")
        

if st.session_state.form_submitted:
    st.session_state.form_submitted = False  # Reset for next time
    st.switch_page("result_dashboard_page.py")
        
