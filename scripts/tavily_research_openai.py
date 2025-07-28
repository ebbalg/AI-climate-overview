from langchain_tavily import TavilySearch, TavilyExtract
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END
from pydantic import BaseModel
from typing import List, Dict
from langchain.prompts import PromptTemplate
from langchain.globals import set_verbose
from dotenv import load_dotenv

load_dotenv()

set_verbose(False)

class ResearchState(BaseModel):
    query: str
    search_results: List[Dict] = []
    extracted_docs: List[Dict] = []
    # summaries: str = ""
    summaries: List[Dict] = []
    sources: List[Dict] = []

llm = ChatOpenAI(
    # model="gpt-4o",
    model="gpt-4o-mini",
    temperature=0,       # reduce randomness and wasted tokens
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
        docs = state.extracted_docs
        
        summary_prompt = PromptTemplate.from_template(
            """ Research question: {query}
                Name of article: {article_title}
                Extracted text from research article: {research_text}
                
                You are a helpful research assistant that aims to summarize research papers clearly and concisely. 
                Write a summary according to the instructions below. Summary should help guide a decision-maker that wants an overview of the negative impact of using GenAI related to the given research question.
                - Write a short summary of the article, about 3-4 sentences.
                - Do NOT make up any new information, make sure that you stick to information in the extracted text.
                - If quantifiable data is included in the research paper, include this data in the summary.
        """
        )
        
    
        summaries = []
        for source in docs:
            url = source["url"]
            article_title = source["title"]
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

inputs = {"query": "What is the climate impact of training large AI models?"}
result = app.invoke(inputs)    # new state

final_state = ResearchState(
    query = result["query"],
    search_results = result["search_results"],
    extracted_docs = result["extracted_docs"],
    summaries = result["summaries"],
    sources = result["sources"]
)

print("\nFINAL SUMMARY:")
print(final_state.summaries)
print("\nSOURCES:")
for s in final_state.sources:
    print(f"{s['index']}. {s['title']} — {s['url']}")
    
