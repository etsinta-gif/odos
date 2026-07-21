# ODOS Repository

This repository contains the ODOS starter pack, source code, documentation, and implementation packs.

## Repository layout
- `src/` — Source code for the application modules
- `tests/` — Test suite
- `docs/` — Project documentation and implementation packs
- `docker/` — Docker container definitions and Compose files
- `scripts/` — Utility scripts and starter pack packaging
- `Starter_Pack_1.1/`…`Starter_Pack_1.5/` — Sprint starter pack scaffolds and handoff files

## Documentation
- `docs/reference/` — Frozen architecture and reference documentation
- `docs/implementation/` — Sprint implementation pack documents
- `docs/guides/` — Developer guides and onboarding content

## Quick start
1. Copy `.env.example` to `.env` and update values.
2. Install `uv` and sync dependencies:
   ```powershell
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   ```
3. Start the development environment:
   ```powershell
   docker-compose -f docker/docker-compose.yml up -d
   ```
4. Open `http://localhost:8000`.

## Notes
- Use `docs/reference/index.md` to locate architecture and standard documents.
- Use `docs/implementation/index.md` to locate sprint implementation packs.
- Keep `docs/reference/` stable; update it only through formal document revision or ADR.
