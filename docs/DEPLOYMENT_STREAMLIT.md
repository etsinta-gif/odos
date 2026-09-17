# Streamlit Deployment

The Streamlit app provides a native login and read-only data pages. It does not embed the React frontend, use Supabase, connect to Docker, or write to a database. It reads the existing `odos.db` snapshot committed with the repository.

## Required hosted services

- The existing `odos.db` file committed with the repository.

## Streamlit configuration

In Streamlit Cloud, add these secrets:

```toml
ODOS_USERNAME = "admin"
ODOS_PASSWORD = "choose-a-strong-password"
```

The password is stored only in Streamlit Secrets. Do not commit it to GitHub. A SHA-256 value may also be used with `ODOS_PASSWORD_HASH = "sha256:<digest>"`.

The native login is available directly at:

```text
https://odosv0.streamlit.app
```

## Backend configuration

The old FastAPI/Docker deployment remains optional and is not used by this Streamlit-only app. Its configuration below applies only if that separate deployment is used:

```text
APP_ENV=production
DATABASE_URL=postgresql+psycopg://<user>:<password>@<postgres-host>:5432/<database>
REDIS_URL=redis://<redis-host>:6379/0
SECRET_KEY=<long-random-secret>
CORS_ALLOW_ORIGINS=https://frontend.example.com
BACKUP_DIR=/var/backups/odos
```

Production and staging refuse to start without `DATABASE_URL`; they never silently create or use `./odos.db`.

## Optional Docker deployment

From the repository root, build the images with the same commands used by CI:

```powershell
docker build -f docker/Dockerfile -t ghcr.io/odos/backend:<tag> .
docker build -f frontend/Dockerfile -t ghcr.io/odos/frontend:<tag> frontend
```

Publish both images, configure the production environment variables, and start `docker-compose.prod.yml`. The frontend image serves the Vite single-page application and proxies `/api/` to the `backend` service. If the frontend and API are hosted separately, build the frontend with `VITE_API_BASE_URL` set to the public API base URL instead.

## GitHub push behavior

Pushes to `main` run the tests and publish these images automatically to GitHub Container Registry:

```text
ghcr.io/<github-owner>/odos-backend:<commit-sha>
ghcr.io/<github-owner>/odos-frontend:<commit-sha>
```

The workflow also publishes the `latest` tag. A remote deployment host must be configured to pull these images and restart its services when a new image is available. GitHub Container Registry stores the images; it does not run them, provide PostgreSQL/Redis, or replace the deployment host.

The remote host should set `VERSION=<commit-sha>` and use images matching the owner namespace. Update the image names in `docker-compose.prod.yml` if the repository owner is different from `odos`.

## Verify from another computer

1. Stop Docker Desktop and local backend/frontend processes on the development laptop.
2. Open the Streamlit URL from a different computer or a private browser window.
3. Confirm the login page loads and browser network requests use the public frontend/API hostname.
4. Confirm the backend liveness and readiness endpoints succeed.
5. Log in, upload a document, generate an export, and verify the data remains after restarting or redeploying the hosted services.
6. Confirm no browser request targets `localhost`, `127.0.0.1`, or a Docker service name.
