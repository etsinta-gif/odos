from __future__ import annotations

import hashlib
import hmac
import sqlite3
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="ODOS", page_icon="O", layout="wide")
DATABASE_PATH = Path(__file__).with_name("odos.db")


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = default
    return str(value).strip()


def _password_matches(password: str, configured: str) -> bool:
    if configured.startswith("sha256:"):
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(digest, configured.removeprefix("sha256:"))
    return hmac.compare_digest(password, configured)


def _read_only_connection() -> sqlite3.Connection:
    uri = f"file:{DATABASE_PATH.as_posix()}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _table_names(connection: sqlite3.Connection) -> list[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [str(row[0]) for row in rows]


def _login() -> None:
    st.title("ODOS")
    st.subheader("Login")
    configured_username = _secret("ODOS_USERNAME")
    configured_password = _secret("ODOS_PASSWORD") or _secret("ODOS_PASSWORD_HASH")
    if not configured_username or not configured_password:
        st.error("ODOS_USERNAME and ODOS_PASSWORD must be configured in Streamlit Secrets.")
        st.code('ODOS_USERNAME = "admin"\nODOS_PASSWORD = "your-password"')
        st.stop()

    with st.form("odos_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)

    if submitted:
        if hmac.compare_digest(username.strip(), configured_username) and _password_matches(password, configured_password):
            st.session_state.authenticated = True
            st.rerun()
        st.error("Invalid username or password.")


def _data_pages() -> None:
    with st.sidebar:
        st.title("ODOS")
        st.caption("Read-only Streamlit edition")
        page = st.radio("Page", ["Dashboard", "Data browser"], label_visibility="collapsed")
        st.divider()
        if st.button("Log out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    if not DATABASE_PATH.exists():
        st.error("The existing odos.db data file is not present in this deployment.")
        return

    try:
        connection = _read_only_connection()
    except sqlite3.Error:
        st.error("The existing ODOS data file could not be opened read-only.")
        return

    try:
        tables = _table_names(connection)
        if page == "Dashboard":
            st.title("ODOS Dashboard")
            st.caption("Read-only view of the current data snapshot")
            columns = st.columns(4)
            for index, table in enumerate(tables[:4]):
                count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                columns[index].metric(table, f"{count:,}")
            st.subheader("Available data")
            st.dataframe({"Table": tables}, use_container_width=True, hide_index=True)
        else:
            st.title("Data browser")
            if not tables:
                st.info("No tables are available in the current data snapshot.")
                return
            selected = st.selectbox("Select a table", tables)
            limit = st.number_input("Rows to display", min_value=1, max_value=500, value=50, step=10)
            rows = connection.execute(f'SELECT * FROM "{selected}" LIMIT ?', (int(limit),)).fetchall()
            headers = [description[0] for description in connection.description or []]
            st.dataframe([dict(zip(headers, row)) for row in rows], use_container_width=True, hide_index=True)
    finally:
        connection.close()


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    _data_pages()
else:
    _login()
