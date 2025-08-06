import streamlit as st

# Define the pages
start_page = st.Page("start_page.py", title="Start page")
project_query_page = st.Page("project_query_page.py", title="New project")
research_topic_page = st.Page("research_topic_page.py", title="General overview")
result_dashboard_page = st.Page("result_dashboard_page.py", title="Result dashboard")
research_result_page = st.Page("research_result_page.py", title="Research emissions result")

# Set up navigation
pg = st.navigation([start_page, project_query_page, research_topic_page, result_dashboard_page, research_result_page])

pg.run()
