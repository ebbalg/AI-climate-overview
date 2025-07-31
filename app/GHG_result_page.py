import streamlit as st
import sys 
import os
import sqlite3
import json
from langchain_tavily import TavilySearch, TavilyExtract
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langgraph.graph import END
from pydantic import BaseModel
from typing import List, Dict
from codecarbon import OfflineEmissionsTracker
from dotenv import load_dotenv

from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.get_carbon_data import get_codecarbon_estimate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

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

        /* Custom styling for summary card */
        .summary-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: left;
            margin-bottom: 20px;
        }

        /* Custom styling for references card */
        .references-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: left;
            margin-bottom: 20px;
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

class ResearchState(BaseModel):
    query: str
    search_results: List[Dict] = []
    extracted_docs: List[Dict] = []
    # summaries: str = ""
    summaries: List[Dict] = []
    sources: List[Dict] = []

# SQLite Notebook
db = sqlite3.connect('notebook.db')
c = db.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS notebook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        summary TEXT,
        title TEXT,
        url TEXT,
        timestamp TEXT,
        UNIQUE(question, title, url)
    )
''')
db.commit()

llm_model = "gpt-4.1-nano"

# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.session_state.pop("GHG_selected_question", None)
        st.switch_page("GHG_emissions_page.py")


st.markdown('<h1 style="text-align: center;"> GHG Emissions from AI </h1>', unsafe_allow_html=True)

research_topic_col, codecarbon_col = st.columns(2)

with research_topic_col:
    st.markdown("**Research Topic**")

    if "GHG_user_question" in st.session_state:
        st.markdown("> **" + st.session_state["GHG_user_question"] + "**")
    elif "GHG_selected_question" in st.session_state:
        st.markdown("> **" + st.session_state["GHG_selected_question"] + "**")
        
    st.markdown("**Research Domains**")
    included_domains = ["ieeexplore.ieee.org", "springeropen.com", "scienceopen.com", "nature.com", "arxiv.org"]    # Peer-reviewed domains for Tavily search.
    # markdown_domains = ( "\n".join(f"- {domain}" for domain in included_domains)
    st.markdown("\n".join(f"- {domain}" for domain in included_domains))

with codecarbon_col: #from Codecarbon emissions in kg Co2eq , energy in kWh, this will be converted
    codecarbon_data = get_codecarbon_estimate()
    
    emissions = codecarbon_data["emissions"]
    energy_consumed = codecarbon_data["energy_consumed"]
    timestamp = codecarbon_data["timestamp"]
    
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    data_retrieval_time = dt.strftime("%B %d, %Y at %I:%M %p")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("**What is the environmental impact of this service?**"):
        st.markdown(f"Sources are retrieved with Tavily Search and Tavily Extract, using only the trusted domains stated under 'Research Domains'. This service also uses ChatOpenAI from Langchain with the model {llm_model} to generate research topics and generate a summarization of each article.")
        st.markdown(f"To estimate the energy consumed (sum of cpu_energy, gpu_energy and ram_energy) and carbon emissions on a local machine, the summarization step with the help of {llm_model} was tracked with CodeCarbon, and the values are displayed below:")
        st.markdown(f'**Energy use of LLM summarization of this service: {energy_consumed:.4f} Wh.**')
        st.markdown(f'**Carbon emissions of LLM summarization of this service: {emissions:.4f} g CO2eq.**')
        st.markdown(f'These values were calculated on the {data_retrieval_time} Swedish time, on an Apple M1 Pro and is just an estimation.')
            

# SUMMARY SECTION

@st.cache_data(show_spinner="Searching Tavily...")
def cached_search(query):
    result = search_tool.invoke({"query": query})
    return result["results"]


@st.cache_data(show_spinner="Extracting content...")
def cached_extract(url):
    return extract_tool.invoke({"urls": [url]})


@st.cache_data(show_spinner="Summarizing content...")
def cached_summarize(prompt_input):
    return llm.invoke(prompt_input)

llm = ChatOpenAI (
# model="gpt-4o",
# model="gpt-4o-mini",
model=llm_model,
# temperature=0.7,       
temperature = 0       # reduce randomness and wasted tokens
)

# Tavily tools
search_tool = TavilySearch(
    max_results=6,
    include_domains=included_domains  
)
extract_tool = TavilyExtract(include_images=False)

graph = StateGraph(ResearchState)
    

def search_node(state):
    query = state.query
    search_results = cached_search(query)
    
    return {"search_results": search_results}

graph.add_node("search", search_node)

def extract_node(state: ResearchState):
    url_to_title = {result['url']: result.get('title', '') for result in state.search_results}
    url_to_content = {result['url']: result.get('content', '') for result in state.search_results}
    extracted = []
    for url in url_to_title.keys():
        extracted_doc = cached_extract(url)
        # print("Extracted doc:", extracted_doc)
        
        # TavilyExtract returns a list under "results"
        if isinstance(extracted_doc, dict) and "results" in extracted_doc:
            raw_content = extracted_doc["results"][0]["raw_content"]       # shorten content?
        else:
            raw_content = str(extracted_doc)
            
        if not raw_content:  # If extraction is empty, get short content from TavilySearch
            raw_content = url_to_content.get(url, "")
            
        extracted.append({
            "url": url,
            "title": url_to_title.get(url, "Untitled"),  
            "text": raw_content  
        })
    return {"extracted_docs": extracted}

graph.add_node("extract", extract_node)

def summarize_node(state):
    
    summary_prompt = PromptTemplate.from_template(
        """ Research topic: {query}
            Name of article: {article_title}
            Extracted text from research article: {research_text}
            
            You are a helpful research assistant that aims to summarize research papers to someone who wants to understand the main point of the article, based on the given research topic. 
            Write a summary according to the instructions below. 
            - Write a short summary of the article, about 2-3 sentences.
            - If quantified data is included in the research paper, include this data in the summary.
            - Be specific in the summary rather than vague.
            - Do NOT make up any new information, make sure that you stick to information in the extracted text.
    """
    )
    
    # tracker = OfflineEmissionsTracker(country_iso_code="SWE")
    # tracker.start()
    summaries = []
    for source in state.extracted_docs:
        url = source["url"]
        article_title = source["title"]
        # research_text = source["text"][:3000]
        research_text = source["text"]
        
        create_summary_chain = summary_prompt | llm | StrOutputParser()
        
        tokens = create_summary_chain.invoke(  # Replace with stream for streamed text generation
                        {"query": state.query, "article_title": article_title, "research_text": research_text}
                    )
        
        summaries.append({
            "title": article_title,
            "url": url,
            "summary": tokens
        })
        
    # code_carbon_data = tracker.stop()
    
    sources = []
    for i, doc in enumerate(state.extracted_docs, start=1):
        sources.append({
            "index": i,
            "url": doc["url"],
            "title": doc.get("title", f"Source {i}")
        })

    return {
        "summaries": summaries,
        "sources": sources,
        # "code_carbon_data": code_carbon_data
    }
    
    
graph.add_node("summarize", summarize_node)
    
# Edges
graph.add_edge("search", "extract")
graph.add_edge("extract", "summarize")
graph.add_edge("summarize", END)

graph.set_entry_point("search")

# Graph: (search) → (extract) → (summarize) → END
app = graph.compile()

selected_question = st.session_state.get("GHG_user_question") or st.session_state.get("GHG_selected_question")

inputs = {"query": selected_question}

if "GHG_result" not in st.session_state or st.session_state["GHG_result"]["query"] != selected_question:
    result = app.invoke(inputs)  
    st.session_state["GHG_result"] = result  
    
else:
    result = st.session_state["GHG_result"]

final_state = ResearchState(
    query = result["query"],
    search_results = result["search_results"],
    extracted_docs = result["extracted_docs"],
    summaries = result["summaries"],
    # code_carbon_data = result["code_carbon_data"],
    sources = result["sources"]
)

st.markdown('<h2 style="text-align: left;"> Research Articles </h2>', unsafe_allow_html=True)

for source in final_state.summaries:
    st.markdown(f"[🔗 {source["title"]}]({source["url"]})", unsafe_allow_html=True)
    st.markdown(source["summary"])
    st.markdown("---")
    

save_research, clear_research = st.columns(2)
with save_research:
    if st.button("Save to Research Notebook"):
        for s in final_state.summaries:
            c.execute('''
                INSERT OR IGNORE INTO notebook (question, summary, title, url, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (final_state.query, s["summary"], s["title"], s["url"], datetime.now().isoformat()))
        db.commit()
        st.success("Saved to your notebook!")
    
with clear_research:  
    if st.button("Clear Research Notebook"):
        c.execute('DELETE FROM notebook')
        db.commit()
        st.success("Your Research Notebook has been cleared!")
    
# View notebook 
st.markdown('<h2 style="text-align: left;"> Research Notebook </h2>', unsafe_allow_html=True)


search_term = st.text_input("Search Notebook")
if search_term:
    c.execute('''
        SELECT question, summary, title, url, timestamp 
        FROM notebook 
        WHERE question LIKE ? OR summary LIKE ?
        ORDER BY timestamp DESC
    ''', (f'%{search_term}%', f'%{search_term}%'))
else:
    c.execute('SELECT question, summary, title, url, timestamp FROM notebook ORDER BY timestamp DESC')
    
    
rows = c.fetchall()
if rows:
    for row in rows:
        st.markdown(f"**{row[0]}**  \n_Saved: {row[4]}_", unsafe_allow_html=True)
        st.markdown(f"[🔗 {row[2]}]({row[3]})", unsafe_allow_html=True)
        st.markdown(row[1])
        st.markdown("---")
else:
    st.info("No entries yet. Save some research!")


c.execute('SELECT question, summary, title, url, timestamp FROM notebook')
rows = c.fetchall()
export = [
    {"question": r[0], "summary": r[1], "title": r[2], "url": r[3], "timestamp": r[4]}
    for r in rows
]
st.download_button(
    "⬇ Download Notebook JSON",
    json.dumps(export, indent=2),
    file_name="notebook.json",
    mime="application/json"
)
    
