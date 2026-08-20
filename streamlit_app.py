import os

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="ODOS", layout="wide")

app_url = os.getenv("ODOS_APP_URL", "http://localhost:8000").rstrip("/")

st.title("ODOS")
st.link_button("Open ODOS in a new tab", app_url)
components.iframe(app_url, height=900, scrolling=True)