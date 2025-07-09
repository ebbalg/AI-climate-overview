import streamlit as st

# Define the pages
start_page = st.Page("start_page.py", title="Start page")
project_query_page = st.Page("project_query_page.py", title="New project")
general_overview_page = st.Page("general_overview_page.py", title="General overview")
result_dashboard_page = st.Page("result_dashboard_page.py", title="Result dashboard")
energy_use_page = st.Page("energy_use_page.py", title="Energy use overview")
GHG_emissions_page = st.Page("GHG_emissions_page.py", title="GHG emissions overview")
GHG_result_page = st.Page("GHG_result_page.py", title="GHG emissions result")
energy_result_page = st.Page("energy_result_page.py", title="Energy use result")

# Set up navigation
pg = st.navigation([start_page, project_query_page, general_overview_page, result_dashboard_page, energy_use_page, GHG_emissions_page, GHG_result_page, energy_result_page])

pg.run()
