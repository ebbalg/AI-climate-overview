# AI-climate-overview
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%E2%9C%94%EF%B8%8F-brightgreen)](https://streamlit.io/)
<!-- [![License](https://img.shields.io/badge/# license-MIT-green.svg)](LICENSE) -->

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
- [Run the application](#run-the-application)
- [Managing dependencies](#managing-dependences)
- [Development](#development)
- [Project structure](#project-structure)
- [Authors](#authors)



## Project overview
This application aims to provide
 a tool for research and decision-making regarding AI technologies, by providing an overview of research topics and credible sources about the environmental impacts of AI where generative AI currently has the most established research. The project was made by a student team in collaboration with WWF, for AI Sweden's Public Innovation Summer Program 2025.

## Requirements
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
NOWTRICITY_API_KEY=your_nowtricity_api_key
ELECTRICITY_MAPS_API_KEY=your_electricity_maps_api_key
```

## Run the Application 
```bash
streamlit run app/app.py
```

## Managing Dependences
```bash
uv pip install <dependency>
uv add <dependency>
```

## Development

This project uses:
- Streamlit as the build tool and frontend framework
- Langchain OpenAI for language model interaction
- Langchain Tavily Search and Tavily Extract API for retrieving web content
- LangGraph for chaining multiple workflows
- SQLite3 for simple data persistance 
- Data from AI Energy Score from HuggingFace (https://huggingface.co/AIEnergyScore)
- Data from Nowtricity (https://www.nowtricity.com/)
- Data from Electricity Maps (https://www.electricitymaps.com/)

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
├── data/                           # AI Energy Score csv files used for carbon or energy calculations, from AI Energy Score and Ember
├── scripts/
│   └── energy_calculations.py      # calculates energy usage based on model and compute assumptions
│   └── get_carbon_data.py          # Uses Nowtricity to pull and process emissions data per country or model
│   └── tavily_research_openai.py   # defines the LangGraph and logic for searching, extracting, and summarizing using Tavily and OpenAI
```

## Authors:
Ebba Leppänen Gröndal, Isabella Fu and Kajsa Lidin.

