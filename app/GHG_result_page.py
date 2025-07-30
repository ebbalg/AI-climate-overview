import streamlit as st
import sys 
import os
from langchain_tavily import TavilySearch, TavilyExtract
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langgraph.graph import END
from pydantic import BaseModel
from typing import List, Dict
from langchain.globals import set_verbose
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from scripts.tavily_research_openai import ResearchState

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


# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.session_state.pop("GHG_selected_question", None)
        st.switch_page("GHG_emissions_page.py")


st.markdown('<h1 style="text-align: center;"> GHG Emissions from GenAI </h1>', unsafe_allow_html=True)


st.markdown("**Research Topic**")

if "GHG_user_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_user_question"] + "**")
elif "GHG_selected_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_selected_question"] + "**")
    
    
st.markdown("**Research Domains**")
included_domains = ["ieeexplore.ieee.org", "springeropen.com", "scienceopen.com", "nature.com"]    # Peer-reviewed domains for Tavily search.
# markdown_domains = ( "\n".join(f"- {domain}" for domain in included_domains)
st.markdown("\n".join(f"- {domain}" for domain in included_domains))


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
model="gpt-4.1-nano",
temperature=0.7,       # reduce randomness and wasted tokens
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

    
    sources = []
    for i, doc in enumerate(state.extracted_docs, start=1):
        sources.append({
            "index": i,
            "url": doc["url"],
            "title": doc.get("title", f"Source {i}")
        })

    return {
        "summaries": summaries,
        "sources": sources
    }
    
    
graph.add_node("summarize", summarize_node)
    
# Edges
graph.add_edge("search", "extract")
graph.add_edge("extract", "summarize")
graph.add_edge("summarize", END)

graph.set_entry_point("search")

# Graph: (search) → (extract) → (summarize) → END
app = graph.compile()

# selected_question = st.session_state["GHG_selected_question"]
selected_question = st.session_state.get("GHG_user_question") or st.session_state.get("GHG_selected_question")

inputs = {"query": selected_question}
result = app.invoke(inputs)    # new state

final_state = ResearchState(
    query = result["query"],
    search_results = result["search_results"],
    extracted_docs = result["extracted_docs"],
    summaries = result["summaries"],
    sources = result["sources"]
)

st.markdown('<h2 style="text-align: left;"> Research Articles </h2>', unsafe_allow_html=True)

for source in final_state.summaries:
    st.markdown(f"[🔗 {source["title"]}]({source["url"]})", unsafe_allow_html=True)
    st.markdown(source["summary"])
    st.markdown("---")
    
