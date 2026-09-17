import os

import streamlit as st

from src.core.deployment_config import public_http_url


st.set_page_config(page_title="ODOS", layout="wide")

configured_url = os.getenv("ODOS_FRONTEND_URL", "").strip()
if not configured_url:
	configured_url = st.secrets.get("ODOS_FRONTEND_URL", "").strip()

app_url = public_http_url(configured_url)
if app_url is None:
	st.title("ODOS")
	st.error("ODOS_FRONTEND_URL is not configured with a public frontend URL.")
	st.markdown(
		"Set `ODOS_FRONTEND_URL` in Streamlit Cloud secrets or environment variables "
		"to the deployed ODOS frontend, for example `https://odos.example.com`."
	)
	st.stop()

login_url = f"{app_url}/login"

st.title("ODOS")
st.link_button("Open ODOS admin login in a new tab", login_url)
st.iframe(login_url, height=900, scrolling=True)