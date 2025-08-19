import streamlit as st
import streamlit.components.v1 as components

# st.set_page_config(layout="centered")
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

st.markdown(body='<h1 style="text-align: center"> AI Footprint </h1>', unsafe_allow_html=True)

space = st.empty()

st.markdown(body='<h5 style="text-align: center"> Helping researchers and decision-makers understand AI’s environmental cost </h5>', unsafe_allow_html=True)

space = st.empty()
space.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown("""
    <style> 
    div.stButton > button:first-child {
        background-color: #a4dffc;
        border-radius: 0.625rem;
        width: 17rem;
        height: 8.625rem;   
        padding: 0.5em 1em;
        cursor: pointer;
        text-align: center;
        white-space: normal;
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        display: flex; 
        color: black;
        justify-content: center;
        align-items: center;
    }
    div.stButton > button:first-child:hover {
        background-color: #85d8ff;
        color: black;
        border: 0.063rem solid #66ccff;
    }   

    </style>
    """, unsafe_allow_html=True)


# Create columns for the buttons
spacer, col1, gap, col2, spacer = st.columns([1.7, 1, 0.5, 1, 1.95]) 
with col1: 
    project_query_option = st.button("**AI Use Case Explorer**")
with col2:
    general_overview_option = st.button("**Research Overview**")


if project_query_option:
    st.switch_page("project_query_page.py")

if general_overview_option:
    st.switch_page("research_topic_page.py")

  
def change_button_style(
    wgt_txt,
    bg_hex="#f5f5f5",
    txt_hex="#333",
    border_radius="0.625rem",
    font_size="1rem",
    padding="0.75rem 1.25rem",
    cursor= "pointer",
    border= "none",
    width="10rem",
    height= "5rem",
    hover_txt="#000"
):
    htmlstr = f"""
        <script>
        const elements = window.parent.document.querySelectorAll('button');
        for (let i = 0; i < elements.length; i++) {{
            if (elements[i].innerText === `{wgt_txt}`) {{
                elements[i].style.backgroundColor = "{bg_hex}";
                elements[i].style.color = "{txt_hex}";
                elements[i].style.borderRadius = "{border_radius}";
                elements[i].style.padding = "{padding}";
                elements[i].style.fontSize = "{font_size}";
                elements[i].style.border = "{border}";
                elements[i].style.width = "{width}";
                elements[i].style.height = "{height}";
                elements[i].style.textAlign = "center";
                elements[i].style.lineHeight = "1.4";

                elements[i].onmouseover = function() {{
                    this.style.color = "{hover_txt}";
                }};
                elements[i].onmouseout = function() {{
                    this.style.backgroundColor = "{bg_hex}";
                    this.style.color = "{txt_hex}";
                }};
            }}
        }}
        </script>
    """
    components.html(htmlstr, height=0, width=0)



bottom_col1, _, _ = st.columns([0.01, 0.98, 0.01])
with bottom_col1:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    change_button_style("About this service", bg_hex="rgba(255, 255, 255, 0.1)", txt_hex="black", height="2.5rem")
    if st.button("About this service", key="about"):
        st.switch_page("about_page.py")
