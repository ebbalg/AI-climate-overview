# AI-climate-overview


## Project overview
The applications aims to offer WW
 a tool for research and decision-making regarding GenAI, by providing an overview of research topics and credible sources about the environmental impacts of GenAI. The project was made by a student team in collaboration with WWF, for AI Sweden's Public Innovation Summer Program 2025.

## Prerequisites 
- Python 3.12 or higher
- `uv` package installer

## Environment Setup
```bash
uv sync
source .venv/bin/activate
```

Create a `.env` file in the root directory with the following API keys:

```bash
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run the Application 
```bash
streamlit run app/app.py
```

## Managing Dependences
```bash
uv add <dependency>
```

## Development

This project uses:
- Streamlit as the build tool and frontend framework
- OpenAI API for language model interaction
- Tavily Search API for retrieving web content
- LangGraph for chaining multiple workflows
- Data from AI Energy Score from HuggingFace (https://huggingface.co/AIEnergyScore)
- Data from Nowtricity (https://www.nowtricity.com/)

## Project Structure

```
app/
├── prompts/                        # prompt files
├── app.py                          # main app file
├── energy_result_page.py           # displays energy-related summaries and sources based on the selected question
├── energy_use_page.py              # lets users generate or input a research question related to energy usage
├── general_overview_page.py        # provides general context on AI's environmental footprint
├── GHG_emissions_page.py           # lets users generate or input a research question related to AI emissions
├── GHG_result_page.py              # displays emissions-related summaries and sources based on the selected question
├── project_query_page.py           # lets users input their organization’s AI use case for tailored analysis
├── result_dashboard_page.py        # shows outputs from the form filled in in the project_query_page
├── start_page.py                   # landing page
├── data/                           # AI Energy Score csv files used for carbon or energy calculations
├── scripts/
│   └── energy_calculations.py      # calculates energy usage based on model and compute assumptions
│   └── get_carbon_data.py          # Uses Nowtricity to pull and process emissions data per country or model
│   └── tavily_research_openai.py   # defines the LangGraph and logic for searching, extracting, and summarizing using Tavily and OpenAI
```

## Authors:
Ebba Leppänen Gröndal, Isabella Fu and Kajsa Lidin.

