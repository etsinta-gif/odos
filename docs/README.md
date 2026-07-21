# ODOS Documentation

This folder contains project documentation, reference architecture, and implementation pack artifacts.

## Structure
- `docs/reference/` — frozen architecture/reference documents and ADRs
- `docs/implementation/` — sprint IMP documents and implementation guidance
- `docs/guides/` — developer guides, onboarding, and process documentation

## Usage
- Add all `DOC-*.md` and `ADR-*.md` files under `docs/reference/`
- Add all `IMP-*.md` files under `docs/implementation/`
- Keep `docs/reference/` documents read-only unless a new ADR or revision is formally approved
- Update `docs/reference/index.md` when new reference docs are added
- Link each `IMP-*.md` to the relevant reference documents that support its requirements
