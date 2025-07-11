import streamlit as st
import sys 
import os
from langchain_tavily import TavilySearch, TavilyExtract
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph import END
from pydantic import BaseModel
from typing import List, Dict
from langchain.globals import set_verbose
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.tavily_research_openai import ResearchState

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


# Back button
top_col1, _, _ = st.columns([0.1, 0.8, 0.1])
with top_col1:
    if st.button("Back", key="back"):
        st.session_state.pop("GHG_selected_question", None)
        st.switch_page("GHG_emissions_page.py")


st.markdown('<h1 style="text-align: center;"> GHG Emissions from GenAI </h1>', unsafe_allow_html=True)


st.markdown("**Research Question**")

if "GHG_user_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_user_question"] + "**")
elif "GHG_selected_question" in st.session_state:
    st.markdown("> **" + st.session_state["GHG_selected_question"] + "**")


    
st.markdown("**Search Query**")


col1, col2 = st.columns(2)

# SUMMARY SECTION
with col1:
    llm = ChatOpenAI (
    # model="gpt-4o",
    # model="gpt-4o-mini",
    model="gpt-4.1-nano",
    temperature=0.7,       # reduce randomness and wasted tokens
    )

    # Tavily tools
    search_tool = TavilySearch(
        max_results=6,
        include_domains=["ieeexplore.ieee.org", "springeropen.com", "scienceopen.com", "nature.com", "scholar.google.com"]  # Peer-reviewed domains. 
    )
    extract_tool = TavilyExtract()

    graph = StateGraph(ResearchState)


    def search_node(state):
        query = state.query
        result = search_tool.invoke({"query": query})
        search_results = result["results"]
        
        return {"search_results": search_results}

    graph.add_node("search", search_node)

    def extract_node(state: ResearchState):
        urls = [result['url'] for result in state.search_results]     # only extract from top 3 docs? [:3]
        extracted = []
        for url in urls:
            extracted_doc = extract_tool.invoke({"urls": [url]})     
            print("Extracted doc:", extracted_doc)
            
            # TavilyExtract returns a list under "results"
            if isinstance(extracted_doc, dict) and "results" in extracted_doc:
                raw_content = extracted_doc["results"][0]["raw_content"]       # shorten content?
            else:
                raw_content = str(extracted_doc)
                
            extracted.append({
                "url": url,
                "title": "",  # fallback
                "text": raw_content  
            })
        return {"extracted_docs": extracted}

    graph.add_node("extract", extract_node)


    def summarize_node(state):
        docs = "\n\n".join([doc["text"] for doc in state.extracted_docs])    # limit amount of character? E.g. to first [:3000]?
        summary_prompt = f"""
        Research question: {state.query}
        Sources:
        {docs}
        
        You are a helpful research assistant that aims to summarize research clearly and concisely, without too much technical jargon.
        When summarizing, cite your sources by using their reference number in brackets immediately after a statement, e.g., [1], [2].
        After a statement, reference to the relevant source supporting that statement by its number.
        Summary should help guide a decision-maker that wants an overview of the negative impact of using GenAI related to the given research question.
        Limit the summary to a maximum of 500 words.
        """
        
        response = llm.invoke(summary_prompt)
        
        sources = []
        for i, doc in enumerate(state.extracted_docs, start=1):
            sources.append({
                "index": i,
                "url": doc["url"],
                "title": doc.get("title", f"Source {i}")
            })

        return {
            "summary": response.content,
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
    
    selected_question = st.session_state["GHG_selected_question"]

    inputs = {"query": selected_question}
    result = app.invoke(inputs)    # new state

    final_state = ResearchState(
        query = result["query"],
        search_results = result["search_results"],
        extracted_docs = result["extracted_docs"],
        summary = result["summary"],
        sources = result["sources"]
    )

    # print("\nFINAL SUMMARY:")
    # print(final_state.summary)
    # print("\nSOURCES:")
    # for s in final_state.sources:
    #     print(f"{s['index']}. {s['title']} — {s['url']}")
    
    
    st.markdown('<h2 style="text-align: left;"> Summary </h2>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="summary-card">
            <p>{final_state.summary}</p>
        </div>
    """, unsafe_allow_html=True)


# REFERENCES SECTION
with col2:
    st.markdown('<h2 style="text-align: left;"> References </h2>', unsafe_allow_html=True)
    refs_html = ""
    for s in final_state.sources:
        refs_html += f"<p>{s['index']}. {s['title']} — <a href='{s['url']}' target='_blank'>{s['url']}</a></p>"
        
    st.markdown(f"""
        <div class="references-card">
            <p>{refs_html}</p>
        </div>
    """, unsafe_allow_html=True)
