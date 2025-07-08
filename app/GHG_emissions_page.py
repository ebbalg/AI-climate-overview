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



st.markdown('<h1 style="text-align: center;"> GHG Emissions from GenAI </h1>', unsafe_allow_html=True)
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


col1, col2, col3 = st.columns(3)

with col1:
    GHG_query = st.button("How does the development of GenAI produce emissions?")
    change_button_style("How does the development of GenAI produce emissions?", bg_hex="#FFFFFF", txt_hex="black", height="120px")
    
    st.button("Can techniques like model pruning, quantization, or distillation meaningfully reduce emissions without compromising output quality?")
    change_button_style("Can techniques like model pruning, quantization, or distillation meaningfully reduce emissions without compromising output quality?", bg_hex="#FFFFFF", txt_hex="black", height="120px")

with col2:
    st.button("What stage of the lifecycle is the most carbon intense?")
    change_button_style("What stage of the lifecycle is the most carbon intense?", bg_hex="#FFFFFF", txt_hex="black", height="120px")

    st.button("How does model architecture (e.g., transformer vs. diffusion models) impact carbon emissions during training and inference?")
    change_button_style("How does model architecture (e.g., transformer vs. diffusion models) impact carbon emissions during training and inference?", bg_hex="#FFFFFF", txt_hex="black", height="120px")


with col3:
    st.button("What are some commonly used methods for measuring carbon emissions from GenAI systems?")
    change_button_style("What are some commonly used methods for measuring carbon emissions from GenAI systems?", bg_hex="#FFFFFF", txt_hex="black", height="120px")
    
    st.button("To what extent can carbon-aware workload scheduling reduce emissions from GenAI usage?")
    change_button_style("To what extent can carbon-aware workload scheduling reduce emissions from GenAI usage?", bg_hex="#FFFFFF", txt_hex="black", height="120px")


# button navigation
if GHG_query:
    st.switch_page("GHG_result_page.py")


st.markdown('<h5 style="text-align: left;font-weight: bold;">I have my own research question</h5>', unsafe_allow_html=True)
research_query = st.text_input(label="text", placeholder="Enter your own research question here")

if research_query:
    st.switch_page("GHG_result_page.py")
