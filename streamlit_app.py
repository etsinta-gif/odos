import os

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="ODOS", layout="wide")

app_url = os.getenv("ODOS_FRONTEND_URL", "http://localhost:3001").rstrip("/")
login_url = f"{app_url}/login"

st.title("ODOS")
st.link_button("Open ODOS admin login in a new tab", login_url)
components.iframe(login_url, height=900, scrolling=True)