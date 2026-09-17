import os

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError


def _configure_runtime_from_secrets() -> None:
	for name in ("APP_ENV", "DATABASE_URL", "SECRET_KEY", "ACCESS_TOKEN_EXPIRE_MINUTES", "REFRESH_TOKEN_EXPIRE_DAYS"):
		if os.getenv(name):
			continue
		try:
			value = st.secrets.get(name)
		except Exception:
			value = None
		if value:
			os.environ[name] = str(value)


_configure_runtime_from_secrets()

if not os.getenv("DATABASE_URL", "").strip():
	st.set_page_config(page_title="ODOS", layout="wide")
	st.title("ODOS")
	st.error("DATABASE_URL is not configured.")
	st.info("Add DATABASE_URL to Streamlit Cloud Secrets for the hosted PostgreSQL database.")
	st.stop()

from src.core.database import SessionLocal
from src.security.auth import authenticate_user


st.set_page_config(page_title="ODOS", layout="wide")


def _normalize_username(username: str | None) -> str:
	return str(username or "").strip()

if "odos_user" not in st.session_state:
	st.session_state.odos_user = None


def _sign_out() -> None:
	st.session_state.odos_user = None


if st.session_state.odos_user is None:
	st.title("ODOS")
	st.subheader("Admin login")

	with st.form("odos_login"):
		username = st.text_input("Username", autocomplete="username")
		password = st.text_input("Password", type="password", autocomplete="current-password")
		submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)

	if submitted:
		if not _normalize_username(username) or not password:
			st.error("Username and password are required.")
		else:
			db = SessionLocal()
			database_error = False
			try:
				user = authenticate_user(
					db,
					_normalize_username(username),
					password,
					source_ip=None,
					user_agent="Streamlit",
				)
			except SQLAlchemyError:
				user = None
				database_error = True
				st.error("The hosted database could not be reached.")
				st.info(
					"Check Streamlit Secrets: DATABASE_URL must use the database provider's "
					"external hostname, valid credentials, and SSL if required. Do not use "
					"localhost, 127.0.0.1, or a Docker service name."
				)
			finally:
				db.close()

			if database_error:
				pass
			elif user is None:
				st.error("Invalid username or password.")
			else:
				st.session_state.odos_user = {
					"user_id": user.user_id,
					"username": user.username,
					"roles": [role.role_name for role in user.roles],
					"password_change_required": bool(getattr(user, "must_change_password", False)),
				}
				st.rerun()
else:
	user = st.session_state.odos_user
	st.title("ODOS")
	st.success(f"Logged in as {user['username']}")
	st.write(f"Roles: {', '.join(user['roles']) or 'No assigned roles'}")
	if user["password_change_required"]:
		st.warning("Your password must be changed before using the application.")
	if st.button("Log out"):
		_sign_out()
		st.rerun()