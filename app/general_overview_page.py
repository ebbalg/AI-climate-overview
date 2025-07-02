import streamlit as st


# There is currently no back button


buttons = [
    "Energy usage",
    "Water consumption",
    "GHG emissions",
    "Raw material consumption",
    "Electronic waste",
    "Environmental contamination"
]


for btn in buttons:
    if btn not in st.session_state:
        st.session_state[btn] = False



def toggle(button_name):
    st.session_state[button_name] = not st.session_state[button_name]



categ_col1, categ_col2, categ_col3 = st.columns([1, 1, 1])

with categ_col1:
    st.button("Energy usage", on_click=toggle, args=("Energy usage",))
    st.button("Water consumption", on_click=toggle, args=("Water consumption",))

with categ_col2:
    st.button("GHG emissions", on_click=toggle, args=("GHG emissions",))
    st.button("Raw material consumption", on_click=toggle, args=("Raw material consumption",))

with categ_col3:
    st.button("Electronic waste", on_click=toggle, args=("Electronic waste",))
    st.button("Environmental contamination", on_click=toggle, args=("Environmental contamination",))


go_button = st.button("Go!")

if go_button:
    st.switch_page("result_dashboard_page.py")
