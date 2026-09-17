from __future__ import annotations

import os
from urllib.parse import urlparse

import streamlit as st


st.set_page_config(page_title="ODOS", layout="wide")


def _configured_frontend_url() -> str:
    configured_url = os.getenv("ODOS_FRONTEND_URL", "").strip()
    if not configured_url:
        try:
            configured_url = str(st.secrets.get("ODOS_FRONTEND_URL", "")).strip()
        except Exception:
            configured_url = ""
    return configured_url.rstrip("/")


frontend_url = _configured_frontend_url()
parsed_url = urlparse(frontend_url)
valid_url = parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)

if not valid_url:
    st.title("ODOS")
    st.error("ODOS_FRONTEND_URL is not configured with the public ODOS frontend URL.")
    st.markdown(
        "Add `ODOS_FRONTEND_URL` to Streamlit Cloud Secrets. It must be the deployed "
        "React frontend URL, not localhost or the Streamlit URL."
    )
    st.stop()

st.title("ODOS")
st.caption("Opening the ODOS admin frontend")
st.link_button("Open admin frontend in a new tab", f"{frontend_url}/login")
st.iframe(f"{frontend_url}/login", height=900, scrolling=True)
