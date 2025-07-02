import streamlit as st

# Define the pages
start_page = st.Page("start_page.py", title="Start page")
project_query_page = st.Page("project_query_page.py", title="New project")
general_overview_page = st.Page("general_overview_page.py", title="General overview")
result_dashboard_page = st.Page("result_dashboard_page.py", title="Result dashboard")

# Set up navigation
pg = st.navigation([start_page, project_query_page, general_overview_page, result_dashboard_page])

pg.run()
