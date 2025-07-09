import streamlit as st
import streamlit.components.v1 as components


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
        st.switch_page("general_overview_page.py")



st.markdown('<h1 style="text-align: center;">Energy Consumption of GenAI</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;font-weight: normal;">You and your organization can directly impact your AI-related energy consumption during usage. Energy consumption from the AI infrastructure and training can be reduced by sustainable procurement choices made by you and your organization.</h4>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<h5 style="text-align: left;font-weight: bold;">Generated research questions</h5>', unsafe_allow_html=True)


def change_button_style(
    wgt_txt,
    bg_hex="#f5f5f5",
    txt_hex="#333",
    border_radius="10px",
    font_size="16px",
    padding="12px 20px",
    width="100%",
    height="auto"
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
                elements[i].style.border = "1px solid #ddd";
                elements[i].style.width = "{width}";
                elements[i].style.height = "{height}";
                elements[i].style.textAlign = "left";
                elements[i].style.lineHeight = "1.4";
            }}
        }}
        </script>
    """
    components.html(htmlstr, height=0, width=0)


col1, col2, col3 = st.columns(3)

with col1:
    energy_query = st.button("Are there standard benchmarks for evaluating energy efficiency in GenAI systems?")
    change_button_style("Are there standard benchmarks for evaluating energy efficiency in GenAI systems?", bg_hex="#FFFFFF", txt_hex="black", height="120px")
    
    st.button("What proportion of GenAI energy usage comes from training vs. deployment at scale?")
    change_button_style("What proportion of GenAI energy usage comes from training vs. deployment at scale?", bg_hex="#FFFFFF", txt_hex="black", height="120px")

with col2:
    st.button("What are current best practices for reducing energy consumption in GenAI workflows?")
    change_button_style("What are current best practices for reducing energy consumption in GenAI workflows?", bg_hex="#FFFFFF", txt_hex="black", height="120px")

    st.button("What are the main factors that influence the energy cost of training GenAI models (e.g., model size, dataset, hardware)?")
    change_button_style("What are the main factors that influence the energy cost of training GenAI models (e.g., model size, dataset, hardware)?", bg_hex="#FFFFFF", txt_hex="black", height="120px")


with col3:
    st.button("What are the current best practices for measuring energy consumption of GenAI systems?")
    change_button_style("What are the current best practices for measuring energy consumption of GenAI systems?", bg_hex="#FFFFFF", txt_hex="black", height="120px")
    
    st.button("What role does regional energy mix (e.g., coal vs renewables) play in the total environmental impact of GenAI?")
    change_button_style("What role does regional energy mix (e.g., coal vs renewables) play in the total environmental impact of GenAI?", bg_hex="#FFFFFF", txt_hex="black", height="120px")


# button navigation
if energy_query:
    st.session_state["selected_question"] = "Are there standard benchmarks for evaluating energy efficiency in GenAI systems?"  # will not be hardcoded in the future
    st.session_state.pop("user_question", None)  # clear previous custom input
    st.switch_page("energy_result_page.py")


st.markdown('<p style="text-align: left; font-weight: bold; margin-bottom: -5px; font-size: 16px;">I have my own research question</p>', unsafe_allow_html=True)
research_query = st.text_input(label="", placeholder="Enter your own research question here")

if research_query:
    st.session_state["user_question"] = research_query
    st.session_state.pop("selected_question", None)  # clear previous custom input
    st.switch_page("energy_result_page.py")

