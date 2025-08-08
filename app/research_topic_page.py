import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# read prompt from a file
with open("app/prompts/research_prompt.txt", "r", encoding="utf-8") as f:
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
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 0.5rem 1.875rem rgba(0, 0, 0, 0.15);
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
            /*background-color: #b3bfb2;*/
            background-color: #a4dffc;
            /*background-color: #66ccff;*/
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
            background-color: #6BD0FF; 
            border-radius: 0.625rem;
            padding: 1.25rem;
            height: 10rem;
        }
        .small-card h5 {
            margin: 0 0 0.313rem 0;
        }

        .small-card p {
            margin: 0 0 0 0; 
        }

        /* Back button styling */
        .stButton>button.back {
            background-color: #b3bfb2;
            /*background-color: #66ccff;*/
            color: black;
            border: none;
            border-radius: 0.375rem;
            padding: 0.375rem 0.938rem;
            font-size: 1rem;
        }
    </style>
""", unsafe_allow_html=True)




# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.switch_page("start_page.py")

# Header + subheading
#st.markdown('<h1 style="text-align: center;">Understanding AI’s Environmental Impact</h1>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align: center;">Research Overview</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;font-weight: normal;">Click to search and learn about the environmental aspects of AI usage that your organization can directly impact, focusing on energy and greenhouse gas emissions</h4>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.spinner("Generating Research Topics..."):
    questions = get_questions(prompt, api_key)


st.markdown('<h5 style="text-align: left;font-weight: bold;">Generated research topics</h5>', unsafe_allow_html=True)


def change_button_style(
    wgt_txt,
    bg_hex="#f5f5f5",
    txt_hex="#333",
    border_radius="0.625rem",
    font_size="1rem",
    padding="0.75rem 1.25rem",
    width="100%",
    height="auto",
    hover_bg="#F8F8F8",
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
                elements[i].style.border = "0.063rem solid #ddd";
                elements[i].style.width = "{width}";
                elements[i].style.height = "{height}";
                elements[i].style.textAlign = "left";
                elements[i].style.lineHeight = "1.4";

                elements[i].onmouseover = function() {{
                    this.style.backgroundColor = "{hover_bg}";
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


cols = st.columns(3)

for i, question in enumerate(questions[:6]):  # Limit to 6
    with cols[i % 3]:  # Distribute across 3 columns
        if st.button(question, key=f"question_{i}"):
            st.session_state["GHG_selected_question"] = question
            st.session_state["navigate_to_result"] = True
        change_button_style(question, bg_hex="#FFFFFF", txt_hex="black", height="7.5rem")


if st.session_state.get("navigate_to_result"):
    st.session_state.pop("GHG_user_question", None)
    st.session_state.pop("navigate_to_result")
    st.switch_page("research_result_page.py")


input_box_col, _, _ = st.columns(3)

with input_box_col:
    st.markdown('<p style="text-align: left; font-weight: bold; margin-bottom: -0.313rem; font-size: 1rem;">I have my own research topic</p>', unsafe_allow_html=True)
    GHG_research_query = st.text_input(label="", placeholder="Enter your own research topic here")

if GHG_research_query:
    st.session_state["GHG_user_question"] = GHG_research_query
    st.session_state.pop("GHG_selected_question", None)  # clear previous selected topic
    st.switch_page("research_result_page.py")


# Section: Other considerations
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Other Environmental Considerations")

st.markdown("""
<p>While this navigator focuses on directly actionable aspects, it’s important to acknowledge that AI’s environmental impact extends beyond energy and carbon emissions. \n Some other examples are listed below.</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
        <div class="small-card">
            <h5>Water Usage</h5>
            <p>Data centers require significant water for cooling, but this varies greatly by location and provider.</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="small-card">
            <h5>Biodiversity</h5>
            <p>AI infrastructure requires significant land use, although it is difficult to quantify its impact on wildlife.</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="small-card">
            <h5>Electronic Waste</h5>
            <p>Hardware lifecycle and disposal impacts are challenging to quantify at the usage level.</p>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
        <div class="small-card">
            <h5>Environmental Contamination</h5>
            <p style="position: relative; top: -0.313rem; z-index: 10;" > Building AI infrastructure carries the risk of releasing harmful substances into the environment.</p>
        </div>
    """, unsafe_allow_html=True)
