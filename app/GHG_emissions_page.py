import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# reading prompt from a file
with open("app/prompts/emissions_research_prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

@st.cache_data(show_spinner=False)
def get_questions(prompt_text, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7
    )
    raw = response.choices[0].message.content
    return [line.strip("0123456789. ").strip() for line in raw.strip().split("\n") if line.strip()]

with st.spinner("Generating Research Topics..."):
    questions = get_questions(prompt, api_key)


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
            padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: left;
        }
        .info-card h4 {
            margin-bottom: 10px;
        }
        .info-card p {
            margin-bottom: 10px;
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



st.markdown('<h1 style="text-align: center;"> GHG Emissions from AI </h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;font-weight: normal;">Learn more about the environmental aspects of AI usage that you and your organization can directly impact, and understand the broader context of AI’s environmental footprint.</h4>', unsafe_allow_html=True)
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


cols = st.columns(3)

for i, question in enumerate(questions[:6]):  # Limit to 6
    with cols[i % 3]:  # Distribute across 3 columns
        if st.button(question, key=f"question_{i}"):
            st.session_state["GHG_selected_question"] = question
            st.session_state["navigate_to_result"] = True
        change_button_style(question, bg_hex="#FFFFFF", txt_hex="black", height="120px")


if st.session_state.get("navigate_to_result"):
    st.session_state.pop("GHG_user_question", None)
    st.session_state.pop("navigate_to_result")
    st.switch_page("GHG_result_page.py")


st.markdown('<p style="text-align: left; font-weight: bold; margin-bottom: -5px; font-size: 16px;">I have my own research question</p>', unsafe_allow_html=True)
GHG_research_query = st.text_input(label="", placeholder="Enter your own research question here")

if GHG_research_query:
    st.session_state["GHG_user_question"] = GHG_research_query
    st.session_state.pop("GHG_selected_question", None)  # clear previous selected question
    st.switch_page("GHG_result_page.py")
