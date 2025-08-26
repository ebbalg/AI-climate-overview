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
- Langchain OpenAI for large language model interaction
- Langchain Tavily Search and Tavily Extract API for retrieving web content
- LangGraph for chaining multiple workflows
- SQLite3 for simple data persistance 
- Data from AI Energy Score from HuggingFace (https://huggingface.co/AIEnergyScore)
- Historic location-specific carbon intensity data from Ember (https://ember-energy.org/)
- Real-time carbon intensity data from Nowtricity (https://www.nowtricity.com/)
- Real-time carbon intensity data from Electricity Maps (https://www.electricitymaps.com/)

## Project Structure

```
app/
├── app.py                          # main app entry file
├── start_page.py                   # landing page
├── prompts/                        # prompt files
├── about_page.py                   # page with information about the application
├── project_query_page.py           # lets users input their organization’s AI use case for tailored analysis
├── result_dashboard_page.py        # dashboard with calculations and visualizations based on the form filled in in the project_query_page
├── research_topic_page.py          # generate topics for research with OpenAI
├── research_result_page.py         # page with sources, research summaries, a research notebook field and a search field

data/                               
├── AI-energy-leaderboard/          # AI Energy Score CSV files 
├── Ember                           # Ember CSV files from 2024-06 to 2025-06

scripts/
├── energy_calculations.py          # calculates energy usage based on model and location
├── get_carbon_data.py              # uses Nowtricity to pull and process emissions data per country or model

codecarbon_logs/                    # CSV files for estimations of environmental impact of API calls
```

## Authors:
Ebba Leppänen Gröndal, Isabella Fu and Kajsa Lidin.

