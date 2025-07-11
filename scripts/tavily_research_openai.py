from langchain_tavily import TavilySearch, TavilyExtract
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph import END
from pydantic import BaseModel
from typing import List, Dict
from langchain.globals import set_verbose
from dotenv import load_dotenv

load_dotenv()

set_verbose(False)

# TODO: Implement caching?

class ResearchState(BaseModel):
    query: str
    search_results: List[Dict] = []
    extracted_docs: List[Dict] = []
    summary: str = ""
    sources: List[Dict] = []

llm = ChatOpenAI(
    # model="gpt-4o",
    model="gpt-4o-mini",
    temperature=0,       # reduce randomness and wasted tokens
)

# Tavily tools
search_tool = TavilySearch(
    max_results=10,
    include_domains=["ieeexplore.ieee.org"]  # Peer-reviewed domains. "sciencedirect.com"
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
    Provide your summary as a bullet point list, each bullet point referencing the relevant sources by their numbers.
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

inputs = {"query": "What is the climate impact of training large AI models?"}
result = app.invoke(inputs)    # new state

final_state = ResearchState(
    query = result["query"],
    search_results = result["search_results"],
    extracted_docs = result["extracted_docs"],
    summary = result["summary"],
    sources = result["sources"]
)

print("\nFINAL SUMMARY:")
print(final_state.summary)
print("\nSOURCES:")
for s in final_state.sources:
    print(f"{s['index']}. {s['title']} — {s['url']}")
    
